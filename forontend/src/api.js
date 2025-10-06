// Simple API configuration and helper for backend integration
const DEFAULT_BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

export const API_BASE_URL = DEFAULT_BACKEND_URL;

export async function uploadVideoForPrediction(file, onProgress) {
  const url = `${API_BASE_URL}/predict`;
  const formData = new FormData();
  formData.append('file', file);

  // Use XMLHttpRequest for progress events
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.responseType = 'json';

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable && typeof onProgress === 'function') {
        const percent = Math.min(100, Math.round((event.loaded / event.total) * 100));
        onProgress(percent);
      }
    };

    xhr.onreadystatechange = () => {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(xhr.response || JSON.parse(xhr.responseText));
        } else {
          try {
            const err = xhr.response || JSON.parse(xhr.responseText);
            reject(new Error(err?.error || `Upload failed with status ${xhr.status}`));
          } catch (_e) {
            reject(new Error(`Upload failed with status ${xhr.status}`));
          }
        }
      }
    };

    xhr.onerror = () => reject(new Error('Network error during upload'));
    xhr.send(formData);
  });
}


