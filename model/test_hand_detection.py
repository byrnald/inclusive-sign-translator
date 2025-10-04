"""
Test Hand Detection with Image File
This script tests hand detection on a static image file
"""

import cv2
import numpy as np
import os
from improved_hand_detection import ImprovedHandDetector

def test_with_image(image_path: str = None):
    """Test hand detection with an image file"""
    detector = ImprovedHandDetector()
    
    if image_path and os.path.exists(image_path):
        # Load image from file
        image = cv2.imread(image_path)
        print(f"Loaded image: {image_path}")
    else:
        # Create a test image with a hand-like shape
        image = create_test_hand_image()
        print("Created test hand image")
    
    # Resize image
    image = cv2.resize(image, (640, 480))
    
    # Detect hands
    hand_detected, landmarks = detector.detect_hands(image)
    
    if hand_detected:
        print(f"Hand detected! Landmarks: {len(landmarks)} points")
        
        # Draw landmarks
        annotated_image = detector.draw_landmarks(image, landmarks)
        
        # Draw contour
        contour_image = detector.draw_hand_contour(image)
        
        # Display results
        cv2.imshow('Original Image', image)
        cv2.imshow('Hand Detection with Landmarks', annotated_image)
        cv2.imshow('Hand Contour', contour_image)
        
        print("Press any key to continue...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return landmarks
    else:
        print("No hand detected in the image")
        cv2.imshow('Original Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return None

def create_test_hand_image():
    """Create a test image with a hand-like shape"""
    # Create a black image
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Draw a hand-like shape using ellipses and rectangles
    # Palm
    cv2.ellipse(image, (320, 300), (80, 60), 0, 0, 360, (200, 180, 160), -1)
    
    # Fingers
    finger_positions = [(280, 200), (320, 180), (360, 200), (400, 220)]
    for i, (x, y) in enumerate(finger_positions):
        # Finger
        cv2.ellipse(image, (x, y), (15, 40), 0, 0, 360, (200, 180, 160), -1)
        # Finger tip
        cv2.circle(image, (x, y - 30), 10, (200, 180, 160), -1)
    
    # Thumb
    cv2.ellipse(image, (250, 280), (20, 30), -30, 0, 360, (200, 180, 160), -1)
    cv2.circle(image, (230, 270), 8, (200, 180, 160), -1)
    
    return image

def test_camera_detection():
    """Test camera detection with better error handling"""
    detector = ImprovedHandDetector()
    
    # Try different camera indices
    for camera_index in [0, 1, 2]:
        print(f"Trying camera index {camera_index}...")
        cap = cv2.VideoCapture(camera_index)
        
        if cap.isOpened():
            print(f"Camera {camera_index} opened successfully!")
            break
        else:
            print(f"Camera {camera_index} failed to open")
            cap.release()
    else:
        print("No camera found. Creating test image instead.")
        return test_with_image()
    
    print("Testing Improved Hand Detection...")
    print("Press 'q' to quit")
    print("Press 'c' to toggle contour view")
    print("Press 's' to save current frame")
    print("Red = Wrist, Green = Finger Tips, Blue = Other landmarks")
    
    show_contour = False
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from camera")
            break
        
        frame_count += 1
        
        # Resize frame for better performance
        frame = cv2.resize(frame, (640, 480))
        
        # Detect hands
        hand_detected, landmarks = detector.detect_hands(frame)
        
        if hand_detected:
            if frame_count % 30 == 0:  # Print every 30 frames
                print(f"Hand detected! Landmarks: {len(landmarks)} points")
            
            # Draw landmarks
            frame = detector.draw_landmarks(frame, landmarks)
            
            # Display confidence
            cv2.putText(frame, "Hand Detected (Improved)", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No Hand Detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Show contour if requested
        if show_contour:
            frame = detector.draw_hand_contour(frame)
            cv2.putText(frame, "Contour View", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Display the frame
        cv2.imshow('Improved Hand Detection', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            show_contour = not show_contour
        elif key == ord('s'):
            # Save current frame
            filename = f"hand_detection_frame_{frame_count}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Saved frame to {filename}")
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Hand Detection Test")
    print("1. Test with camera")
    print("2. Test with image file")
    print("3. Test with synthetic image")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        test_camera_detection()
    elif choice == "2":
        image_path = input("Enter image path (or press Enter for default): ").strip()
        if not image_path:
            image_path = None
        test_with_image(image_path)
    elif choice == "3":
        test_with_image()  # Will create synthetic image
    else:
        print("Invalid choice. Running camera test...")
        test_camera_detection()
