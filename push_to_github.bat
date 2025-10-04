@echo off
echo Setting up Git and pushing to GitHub...

REM Configure Git (replace with your GitHub username and email)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

REM Add all new files
git add .

REM Commit changes
git commit -m "Add improved hand detection and finger recognition

- Added finger_detection.py: Simple finger tip detection using contour analysis
- Added improved_hand_detection.py: Advanced hand landmark detection
- Added opencv_hand_detection.py: Basic skin color detection fallback
- Added test scripts: simple_test.py and test_hand_detection.py
- Updated requirements.txt for Python 3.13 compatibility
- Created test images for validation

Features:
- Real-time finger detection without MediaPipe
- Contour analysis for ASL gesture recognition
- Multiple detection approaches for robustness
- Ready for ASL A-E gesture training"

REM Push to GitHub
git push origin main

echo Done! Your work is now on GitHub.
pause
