"""
Simple Hand Detection Test
Tests the improved hand detection without user input
"""

import cv2
import numpy as np
from improved_hand_detection import ImprovedHandDetector

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

def test_synthetic_hand():
    """Test with synthetic hand image"""
    print("Testing with synthetic hand image...")
    
    detector = ImprovedHandDetector()
    image = create_test_hand_image()
    
    # Detect hands
    hand_detected, landmarks = detector.detect_hands(image)
    
    if hand_detected:
        print(f"[OK] Hand detected! Landmarks: {len(landmarks)} points")
        
        # Draw landmarks
        annotated_image = detector.draw_landmarks(image, landmarks)
        
        # Draw contour
        contour_image = detector.draw_hand_contour(image)
        
        # Save results
        cv2.imwrite("test_hand_original.jpg", image)
        cv2.imwrite("test_hand_landmarks.jpg", annotated_image)
        cv2.imwrite("test_hand_contour.jpg", contour_image)
        
        print("[OK] Images saved:")
        print("  - test_hand_original.jpg")
        print("  - test_hand_landmarks.jpg") 
        print("  - test_hand_contour.jpg")
        
        return landmarks
    else:
        print("[ERROR] No hand detected in synthetic image")
        cv2.imwrite("test_hand_original.jpg", image)
        return None

def test_camera():
    """Test with camera"""
    print("Testing with camera...")
    
    detector = ImprovedHandDetector()
    
    # Try to open camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("[ERROR] Could not open camera")
        return False
    
    print("[OK] Camera opened successfully!")
    print("Press 'q' to quit, 'c' to toggle contour view")
    
    show_contour = False
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to read frame")
            break
        
        frame_count += 1
        frame = cv2.resize(frame, (640, 480))
        
        # Detect hands
        hand_detected, landmarks = detector.detect_hands(frame)
        
        if hand_detected:
            if frame_count % 30 == 0:  # Print every 30 frames
                print(f"[OK] Hand detected! Landmarks: {len(landmarks)} points")
            
            # Draw landmarks
            frame = detector.draw_landmarks(frame, landmarks)
            cv2.putText(frame, "Hand Detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No Hand Detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Show contour if requested
        if show_contour:
            frame = detector.draw_hand_contour(frame)
            cv2.putText(frame, "Contour View", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        cv2.imshow('Hand Detection Test', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            show_contour = not show_contour
    
    cap.release()
    cv2.destroyAllWindows()
    return True

if __name__ == "__main__":
    print("ASL Hand Detection Test")
    print("=" * 40)
    
    # Test with synthetic image first
    landmarks = test_synthetic_hand()
    
    if landmarks:
        print(f"\n[INFO] Landmark Analysis:")
        print(f"  - Total landmarks: {len(landmarks)}")
        print(f"  - Wrist point: {landmarks[0] if landmarks else 'None'}")
        print(f"  - Finger tips: {landmarks[1:5] if len(landmarks) > 4 else 'None'}")
    
    print("\n[CAMERA] Testing camera detection...")
    test_camera()
    
    print("\n[OK] Test completed!")
