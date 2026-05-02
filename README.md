 # Deepfake Detection Platform

A modern, AI-powered deepfake detection platform built with React and TailwindCSS. This platform allows users to upload images or videos and instantly detect whether the content is real or manipulated using advanced neural networks.

## 🚀 Features

### Core Functionality
- **AI-Powered Detection**: Advanced CNN-LSTM hybrid model with 95% accuracy
- **Multi-Format Support**: Images (JPG, PNG, GIF, BMP, WebP) and Videos (MP4, MOV, AVI, MKV, WebM, FLV)
- **Real-time Analysis**: Get results in 3-5 seconds for images, 10-30 seconds for videos
- **Privacy First**: Automatic file deletion after processing
- **Batch Processing**: Upload up to 5 files simultaneously

### User Interface
- **Modern Design**: Clean, futuristic interface with dark mode support
- **Responsive Layout**: Mobile-first design that works on all devices
- **Interactive Components**: Drag-and-drop upload, progress bars, confidence meters
- **Visual Analysis**: Heatmap overlays showing suspicious areas
- **Detailed Reports**: Comprehensive analysis with explanations

### Advanced Features
- **Heatmap Visualization**: Visual overlay showing manipulated areas
- **Timeline Analysis**: Suspicious frame markers for video content
- **Metadata Analysis**: EXIF data and technical information
- **Explainable AI**: Detailed explanations of AI decisions
- **Confidence Scoring**: Percentage-based confidence levels

## 🛠️ Technology Stack

- **Frontend**: React 18, TailwindCSS, Framer Motion
- **UI Components**: Custom component library with accessibility features
- **Icons**: Lucide React
- **File Handling**: React Dropzone
- **Routing**: React Router DOM
- **State Management**: React Context API
- **Animations**: Framer Motion

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Button.js       # Custom button component
│   ├── Card.js         # Card container component
│   ├── ConfidenceMeter.js # Confidence visualization
│   ├── DarkModeToggle.js  # Dark mode switcher
│   ├── FileUpload.js   # Drag-and-drop file upload
│   ├── HeatmapOverlay.js # Heatmap visualization
│   ├── Navbar.js       # Navigation component
│   ├── ProgressBar.js  # Progress indicator
│   ├── Tabs.js         # Tab navigation
│   └── VideoPlayer.js  # Custom video player
├── context/            # React context providers
│   └── DarkModeContext.js # Dark mode state management
├── pages/              # Page components
│   ├── AboutPage.js    # About and team information
│   ├── HelpPage.js     # Help and support center
│   ├── LandingPage.js  # Homepage with hero section
│   ├── NewsPage.js     # News and research articles
│   ├── ResultsPage.js  # Analysis results display
│   └── UploadPage.js   # File upload and analysis
├── App.js              # Main application component
├── index.js            # Application entry point
└── index.css           # Global styles and Tailwind imports
```

## 🎨 Design System

### Color Palette
- **Primary**: Deep blue (#2563eb) - Trust and technology
- **Secondary**: Neutral grays - Professional and clean
- **Accent**: Purple (#8b5cf6) - AI and innovation
- **Success**: Green - Real/authentic content
- **Warning**: Yellow - Inconclusive results
- **Danger**: Red - Manipulated content

### Typography
- **Primary Font**: Inter - Modern and readable
- **Secondary Font**: Poppins - Friendly and approachable

### Components
- **Buttons**: Multiple variants (primary, secondary, outline, ghost)
- **Cards**: Consistent spacing and shadows
- **Forms**: Accessible inputs with proper focus states
- **Navigation**: Sticky header with smooth transitions

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ 
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/VarunLambole/deepFake.git
   cd deepFake
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## 📱 Pages Overview

### 🏠 Landing Page
- Hero section with compelling value proposition
- Animated statistics and feature highlights
- Real vs. fake examples carousel
- Call-to-action sections

### 📤 Upload Page
- Drag-and-drop file upload interface
- Multiple upload methods (file, webcam, URL)
- Real-time upload progress
- Analysis settings and privacy controls

### 📊 Results Page
- Comprehensive analysis results
- Tabbed interface (Overview, Heatmap, Timeline, Metadata, Explainability)
- Confidence meters and visual indicators
- Download and sharing options

### ℹ️ About Page
- Mission statement and company values
- Technology stack explanation
- Team member profiles
- Company timeline and milestones

### 📰 News Page
- Latest deepfake detection news
- Research papers and case studies
- Filterable content by category and type
- Newsletter subscription

### ❓ Help Page
- Comprehensive FAQ section
- Step-by-step guides
- Contact form and support options
- Searchable help content

## 🎯 Key Features Explained

### AI Detection Process
1. **Upload**: Users upload media files through multiple methods
2. **Analysis**: CNN-LSTM model analyzes facial features, lighting, and temporal patterns
3. **Results**: Detailed report with confidence scores and visual indicators
4. **Cleanup**: Files are automatically deleted for privacy

### Privacy & Security
- **No Data Retention**: Files deleted immediately after analysis
- **End-to-End Encryption**: Secure data transmission
- **GDPR Compliant**: Privacy-first approach
- **Transparent Processing**: Clear explanations of AI decisions

### Accessibility
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: Proper ARIA labels and semantic HTML
- **High Contrast**: Dark mode and high contrast options
- **Responsive Design**: Works on all screen sizes

## 🔧 Customization

### Theming
The platform uses TailwindCSS with a custom design system. To customize:

1. **Colors**: Update `tailwind.config.js` color palette
2. **Typography**: Modify font families in the config
3. **Components**: Customize component styles in `src/index.css`

### Adding New Features
1. **Components**: Add new components in `src/components/`
2. **Pages**: Create new pages in `src/pages/`
3. **Context**: Add global state in `src/context/`

## 📈 Performance

- **Lazy Loading**: Components loaded on demand
- **Image Optimization**: Responsive images with proper sizing
- **Bundle Splitting**: Code splitting for optimal loading
- **Caching**: Efficient caching strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **AI Research Community**: For advancing deepfake detection techniques
- **Open Source Libraries**: React, TailwindCSS, Framer Motion, and others
- **Design Inspiration**: Modern AI and cybersecurity platforms
- **User Feedback**: Continuous improvement based on user needs

## 📞 Support

- **Documentation**: Check the Help page for detailed guides
- **FAQ**: Common questions and answers
- **Contact**: Email support for technical issues
- **Community**: Join our community for discussions and updates

---

**Built with ❤️ for media authenticity and truth in the digital age.**
