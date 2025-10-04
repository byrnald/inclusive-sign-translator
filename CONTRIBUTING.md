# 🤝 Contributing to Inclusive Sign Translator

Thank you for your interest in contributing to the Inclusive Sign Translator project! This document provides guidelines for our 3-person hackathon team.

## 🚀 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- Git
- A modern web browser with camera access

### Development Setup
1. Clone the repository
2. Set up your assigned component (frontend/model/backend)
3. Create a feature branch
4. Make your changes
5. Test thoroughly
6. Create a pull request

## 👥 Team Roles & Responsibilities

### Frontend Developer
- **Branch:** `frontend`
- **Responsibilities:**
  - React + TailwindCSS implementation
  - Camera feed component
  - Real-time UI updates
  - Responsive design
- **Key Files:**
  - `frontend/src/components/CameraFeed.jsx`
  - `frontend/src/utils/gestureDetector.js`
  - `frontend/src/styles/`

### Model Developer
- **Branch:** `model`
- **Responsibilities:**
  - Mediapipe hand detection
  - ML model training
  - Model optimization
  - Data collection
- **Key Files:**
  - `model/training_notebooks/`
  - `model/mediapipe_test.py`
  - `model/saved_models/`

### Integration Developer
- **Branch:** `integration`
- **Responsibilities:**
  - Frontend-backend connection
  - Real-time processing
  - API integration
  - Text-to-speech features
- **Key Files:**
  - `backend/app.py`
  - `frontend/src/utils/api.js`

## 🔄 Git Workflow

### Branch Naming
- `frontend/feature-name`
- `model/feature-name`
- `integration/feature-name`

### Commit Messages
Use conventional commits:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code formatting
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

### Pull Request Process
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Create a pull request
5. Request review from team members
6. Address feedback
7. Merge after approval

## 🧪 Testing Guidelines

### Frontend Testing
- Test camera access in different browsers
- Verify responsive design
- Check real-time updates
- Test gesture detection accuracy

### Model Testing
- Validate hand landmark detection
- Test gesture classification accuracy
- Benchmark model performance
- Test with different lighting conditions

### Integration Testing
- Test API endpoints
- Verify real-time communication
- Test error handling
- Validate data flow

## 📝 Code Standards

### JavaScript/React
- Use functional components with hooks
- Follow React best practices
- Use meaningful variable names
- Add comments for complex logic

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to functions
- Keep functions small and focused

### General
- Write clean, readable code
- Add comments for complex logic
- Use consistent formatting
- Remove unused code

## 🐛 Bug Reports

When reporting bugs, include:
- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Browser/OS information
- Screenshots if applicable

## 💡 Feature Requests

When suggesting features:
- Describe the feature clearly
- Explain the use case
- Consider implementation complexity
- Discuss with team before starting

## 🚀 Deployment

### Frontend
- Build: `npm run build`
- Deploy to Vercel/Netlify
- Test in production environment

### Backend
- Deploy to Heroku/Railway
- Set up environment variables
- Monitor logs and performance

## 📞 Communication

- Use GitHub issues for bug reports
- Use pull request comments for code review
- Communicate blockers early
- Share progress updates regularly

## 🎯 Hackathon Goals

- **Day 1:** Basic setup and camera access
- **Day 2:** Hand detection and simple gestures
- **Day 3:** Model training and integration
- **Day 4:** Polish and presentation prep

## 🏆 Success Metrics

- Camera access working in all major browsers
- Real-time gesture detection with >80% accuracy
- Clean, responsive UI
- Smooth integration between components
- Working demo for presentation

Happy coding! 🚀

