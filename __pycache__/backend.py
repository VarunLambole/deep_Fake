# backend.py
import io
import cv2
import torch
import torch.nn as nn
import torchvision.transforms as T
try:
    from facenet_pytorch import MTCNN  # optional
    _FACENET_AVAILABLE = True
except Exception as _e:
    MTCNN = None
    _FACENET_AVAILABLE = False
from torchvision import models
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import logging
import time
from PIL import Image
import tempfile
import numpy as np

# ---------------- Model Definition ---------------- #
class ResNet50BiLSTM(nn.Module):
    def __init__(self, hidden=256):
        super().__init__()
        base = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
        self.cnn = nn.Sequential(*list(base.children())[:-1])
        self.lstm = nn.LSTM(2048, hidden, batch_first=True, bidirectional=True)
        self.head = nn.Sequential(
            nn.Linear(hidden * 2, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        B, T, C, H, W = x.shape
        x = x.view(B * T, C, H, W)
        feats = self.cnn(x).view(B, T, -1)
        lstm_out, _ = self.lstm(feats)
        out = self.head(lstm_out[:, -1, :])
        return out

# ---------------- Initialization ---------------- #
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = ResNet50BiLSTM().to(DEVICE)
MODEL_LOADED = False

# Load trained weights (resolved relative to this file)
MODEL_PATH = (Path(__file__).resolve().parent / "model_epoch_47.pth").resolve()
try:
    state_dict = torch.load(str(MODEL_PATH), map_location=DEVICE)
    model.load_state_dict(state_dict)
    model.eval()
    MODEL_LOADED = True
except Exception as load_err:
    # Do not crash the server; proceed in degraded mode
    logging.getLogger("deepfake-backend").warning(
        "Model weights not loaded from '%s': %s. Running in degraded mode.",
        MODEL_PATH,
        load_err,
    )

# Face detectors (prefer MTCNN, fallback to OpenCV Haar)
mtcnn = None
haar_detector = None
if _FACENET_AVAILABLE:
    try:
        mtcnn = MTCNN(image_size=224, margin=20, keep_all=False, device=DEVICE)
    except Exception as e:
        mtcnn = None

if mtcnn is None:
    # Initialize OpenCV Haar cascade as fallback
    haar_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    haar_detector = cv2.CascadeClassifier(haar_path)

# Transform for input normalization
transform = T.Compose([
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225])
])

# ---------------- FastAPI Setup ---------------- #
app = FastAPI(title="Deepfake Detection API", version="1.0")

# Enable CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Logging Setup ---------------- #
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)
logger = logging.getLogger("deepfake-backend")

@app.middleware("http")
async def log_requests(request, call_next):
    start = time.perf_counter()
    try:
        response = await call_next(request)
        return response
    finally:
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(f"%s %s -> %s in %.1fms",
                    request.method,
                    request.url.path,
                    getattr(response, 'status_code', 'NA'),
                    duration_ms)

# ---------------- Helper Function ---------------- #
# ---------------- Helper Function ---------------- #
def extract_faces_from_video(video_path, num_frames=16):
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video: {video_path}")
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    step = max(total // num_frames, 1)

    faces = []
    for i in range(num_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * step)
        ret, frame = cap.read()
        if not ret:
            break
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        face_tensor = None

        # Try MTCNN first if available
        if mtcnn is not None:
            try:
                mtcnn_face = mtcnn(img)
                if mtcnn_face is not None:
                    face_tensor = mtcnn_face
            except Exception:
                face_tensor = None

        # Fallback to Haar cascade
        if face_tensor is None and haar_detector is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detections = haar_detector.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
            )
            if len(detections) > 0:
                x, y, w, h = sorted(detections, key=lambda r: r[2] * r[3], reverse=True)[0]
                x1, y1, x2, y2 = max(0, x), max(0, y), min(frame.shape[1], x + w), min(frame.shape[0], y + h)
                face_bgr = frame[y1:y2, x1:x2]
                face_rgb = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2RGB)
                face_pil = Image.fromarray(face_rgb)
                face_tensor = T.ToTensor()(face_pil)

        # Last-resort center crop
        if face_tensor is None:
            w, h = img.size
            crop = img.crop(((w - h)//2, 0, (w + h)//2, h))
            face_tensor = T.ToTensor()(crop)

        # Ensure the face tensor is resized to 224x224
        face_pil_resized = T.ToPILImage()(face_tensor)
        face_resized = T.Resize((224, 224))(face_pil_resized)
        face_tensor = transform(face_resized)

        faces.append(face_tensor)

    cap.release()

    if len(faces) < num_frames:
        logger.warning(f"⚠️ Only {len(faces)} frames extracted from video.")

    if not faces:
        raise ValueError("No faces could be extracted from the provided video.")

    # Stack into shape (1, T, C, H, W)
    return torch.stack(faces, dim=0).unsqueeze(0)


# ---------------- Prediction Route ---------------- #
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    tmp_path = None
    try:
        logger.info(f"/predict received: filename=%s content_type=%s", file.filename, file.content_type)
        # Validate content type (expecting video files)
        if file.content_type and not str(file.content_type).startswith('video/'):
            return JSONResponse(status_code=400, content={"error": f"Unsupported content type: {file.content_type}. Please upload a video file (e.g., mp4)."})

        if not MODEL_LOADED:
            return JSONResponse(status_code=503, content={
                "error": "Model not loaded on server. Please upload model weights or try again later.",
                "model_path": str(MODEL_PATH)
            })
        # Save temporary video file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(await file.read())
            tmp_path = Path(tmp.name)
        logger.info(f"Temporary file written: %s (exists=%s)", tmp_path, tmp_path.exists())

        # Extract frames and run model
        frames = extract_faces_from_video(tmp_path)
        frames = frames.to(DEVICE)
        with torch.no_grad():
            pred = model(frames).item()

        result = {
            "filename": file.filename,
            "prediction_score": float(pred),
            "label": "FAKE" if pred > 0.5 else "REAL"
        }

        logger.info("Prediction completed: score=%.4f label=%s", result["prediction_score"], result["label"])
        return JSONResponse(result)

    except Exception as e:
        logger.exception("Error during /predict: %s", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)

# ---------------- Root Route ---------------- #
@app.get("/")
def home():
    return {"message": "Deepfake Detection API is running 🚀"}

# ---------------- Health Route ---------------- #
@app.get("/health")
def health():
    return {
        "status": "ok",
        "device": str(DEVICE),
        "model_loaded": MODEL_LOADED,
        "model_path": str(MODEL_PATH)
    }

