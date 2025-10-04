# Frontend - Inclusive Sign Translator

React frontend application for real-time ASL gesture recognition.

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation
```bash
cd frontend
npm install
```

### Development
```bash
npm run dev
```

The app will start on `http://localhost:3000`

### Build for Production
```bash
npm run build
```

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── CameraFeed.jsx   # Camera feed with gesture detection
│   │   ├── Header.jsx       # App header
│   │   └── GestureDisplay.jsx # Gesture display component
│   ├── pages/               # Page components
│   ├── styles/              # CSS styles
│   │   └── index.css        # TailwindCSS styles
│   ├── utils/               # Utility functions
│   │   ├── gestureDetector.js # Gesture detection logic
│   │   ├── mediapipe.js     # Mediapipe integration
│   │   └── api.js           # Backend API communication
│   ├── App.jsx              # Main app component
│   └── main.jsx             # App entry point
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## 🎨 Features

### Components

#### CameraFeed
- Webcam access using getUserMedia
- Real-time video display
- Hand landmark detection overlay
- Gesture detection integration

#### GestureDisplay
- Real-time gesture display
- Confidence meter
- Status indicators
- Supported gestures grid

#### Header
- App title and branding
- Status indicators
- Navigation elements

### Utilities

#### gestureDetector.js
- Main gesture detection logic
- Mediapipe integration
- ML model integration
- Feature extraction

#### mediapipe.js
- Mediapipe Hands setup
- Hand landmark extraction
- Feature calculation
- Camera integration

#### api.js
- Backend API communication
- Image processing
- Error handling
- Data formatting

## 🎯 Usage

### Basic Usage
1. Open the app in a modern browser
2. Allow camera access when prompted
3. Click "Start Detection" to begin gesture recognition
4. Make ASL gestures (A, B, C, D, E) in front of the camera
5. Watch the detected gesture appear in real-time

### Advanced Features
- **Calibration**: Use the calibrate button to improve detection
- **Confidence**: Monitor confidence levels for gesture accuracy
- **Status**: Check detection status and system health

## 🔧 Configuration

### Environment Variables
- `VITE_API_URL`: Backend API URL (default: http://localhost:5000)

### TailwindCSS
The app uses TailwindCSS for styling with a custom dark theme:
- Dark background (`bg-dark-bg`)
- Surface colors (`bg-dark-surface`)
- Accent colors (`bg-accent`)
- Custom gradients and animations

## 🧪 Testing

### Manual Testing
1. Test camera access in different browsers
2. Verify gesture detection accuracy
3. Check responsive design on different screen sizes
4. Test error handling for camera access denied

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🚀 Deployment

### Vercel
```bash
npm run build
# Deploy dist/ folder to Vercel
```

### Netlify
```bash
npm run build
# Deploy dist/ folder to Netlify
```

### Docker
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 🔧 Development

### Adding New Gestures
1. Update `GESTURES` array in components
2. Add new gesture to training data
3. Retrain ML model
4. Update frontend display logic

### Customizing UI
- Modify TailwindCSS classes in components
- Update color scheme in `tailwind.config.js`
- Add new components in `src/components/`

### Performance Optimization
- Use React.memo for expensive components
- Implement lazy loading for large components
- Optimize camera feed rendering
- Cache API responses

## 🐛 Troubleshooting

### Common Issues
1. **Camera not working**: Check browser permissions and HTTPS
2. **Gesture detection not working**: Verify Mediapipe initialization
3. **API errors**: Check backend connection and CORS settings
4. **Performance issues**: Reduce camera resolution or frame rate

### Debug Mode
Enable debug logging by setting `localStorage.debug = 'gesture-detector'`

## 📱 Mobile Support

The app is responsive and works on mobile devices:
- Touch-friendly interface
- Responsive camera feed
- Mobile-optimized gesture detection
- Touch gestures for navigation

## 🔒 Security

- Camera access requires user permission
- No data is stored locally
- API communication uses HTTPS in production
- CORS protection for backend communication
