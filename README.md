# 🎯 Inclusive Sign Translator

A real-time web application that detects basic sign language gestures through a webcam and translates them into text for beginners learning ASL.

## 🚀 Project Overview

This project helps people learn American Sign Language (ASL) by providing real-time gesture recognition and translation. The app uses computer vision and machine learning to detect hand gestures and display the corresponding letters or words.

## 📁 Project Structure

```
inclusive-sign-translator/
├── frontend/              # React web app for UI + camera feed
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── styles/
│   │   ├── utils/
│   │   └── main.jsx
│   ├── package.json
│   └── README.md
│
├── model/                 # Gesture recognition and ML model files
│   ├── training_notebooks/
│   ├── saved_models/
│   ├── mediapipe_test.py
│   └── README.md
│
├── backend/ (optional)    # Flask backend for advanced processing
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── .gitignore
├── README.md
└── CONTRIBUTING.md
```

## 👥 Team Members & Roles

- **Member 1: Frontend/UI Developer**
  - React + TailwindCSS setup
  - Camera access and display
  - Real-time UI updates

- **Member 2: Model Developer**
  - Mediapipe hand detection
  - ML model training for ASL gestures
  - Model optimization and export

- **Member 3: Integration/Backend Developer**
  - Frontend-backend integration
  - Real-time gesture processing
  - Optional text-to-speech features

## 🛠️ Tech Stack

- **Frontend:** React + Vite + TailwindCSS
- **Model:** Mediapipe Hands + TensorFlow.js
- **Backend:** Flask (Python) - Optional
- **AI Training:** Python Notebooks + Teachable Machine

## 🚀 Quick Start

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Model Development
```bash
cd model
pip install -r requirements.txt
jupyter notebook
```

### Backend Setup (Optional)
```bash
cd backend
pip install -r requirements.txt
python app.py
```

## 🧩 Features (MVP)

- [x] Webcam access using getUserMedia
- [x] Real-time hand gesture detection
- [x] Classification of static signs (A–E minimum)
- [x] Dynamic text display
- [x] Responsive dark theme UI
- [ ] Voice output using Web Speech API

## 🔄 Development Workflow

1. Create feature branches: `frontend`, `model`, `integration`
2. Work on your assigned components
3. Create pull requests for code review
4. Merge to `main` after approval

## 📝 Git Commit Guidelines

- `feat: add camera feed and start detection button`
- `model: trained ASL A–E gestures`
- `fix: text overlay display on video stream`
- `docs: update setup instructions`

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## 📄 License

MIT License - see LICENSE file for details.

