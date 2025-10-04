"""
Simple ASL Letter Detector
Easy-to-use ASL letter recognition with clear feedback
"""

import cv2
import numpy as np
from finger_detection import FingerDetector

class SimpleASLDetector:
    def __init__(self):
        self.finger_detector = FingerDetector()
        self.last_detection = None
        self.detection_count = 0
        
    def detect_letter(self, image):
        """Detect ASL letter from image"""
        # Detect fingers
        fingers_detected, finger_points = self.finger_detector.detect_fingers(image)
        
        if not fingers_detected:
            # No fingers = E (fist)
            return "E", 0.8, "Fist (no fingers)"
        else:
            finger_count = len(finger_points)
            
            if finger_count == 1:
                # 1 finger = A or D
                finger_x = finger_points[0][0]
                if finger_x < 0.4:
                    return "A", 0.7, "Thumb out"
                else:
                    return "D", 0.7, "Index finger up"
            elif finger_count == 2:
                return "C", 0.6, "Curved hand (2 fingers)"
            elif finger_count == 3:
                return "C", 0.7, "Curved hand (3 fingers)"
            elif finger_count == 4:
                return "C", 0.6, "Curved hand (4 fingers)"
            elif finger_count == 5:
                return "B", 0.8, "Open hand (5 fingers)"
            else:
                return "Unknown", 0.0, f"Detected {finger_count} fingers"
    
    def draw_result(self, image, letter, confidence, description):
        """Draw detection result on image"""
        # Clear background for text
        overlay = image.copy()
        cv2.rectangle(overlay, (10, 10), (400, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, image, 0.3, 0, image)
        
        # Draw letter
        cv2.putText(image, f"ASL Letter: {letter}", (20, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        
        # Draw confidence
        cv2.putText(image, f"Confidence: {confidence:.2f}", (20, 80), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        
        # Draw description
        cv2.putText(image, description, (20, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        return image

def test_simple_asl():
    """Test simple ASL detection"""
    detector = SimpleASLDetector()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Could not open camera")
        return
    
    print("Simple ASL Letter Detection")
    print("Show ASL letters A, B, C, D, E to the camera")
    print("Press 'q' to quit")
    print("Press 'h' for help")
    
    show_help = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.flip(frame, 1)  # Mirror effect
        
        # Detect letter
        letter, confidence, description = detector.detect_letter(frame)
        
        # Draw result
        frame = detector.draw_result(frame, letter, confidence, description)
        
        # Show help
        if show_help:
            help_lines = [
                "ASL Letters Guide:",
                "A: Fist with thumb out (1 finger)",
                "B: Open hand (5 fingers)", 
                "C: Curved hand (2-4 fingers)",
                "D: Index finger up (1 finger)",
                "E: Fist (0 fingers)"
            ]
            for i, line in enumerate(help_lines):
                cv2.putText(frame, line, (450, 50 + i * 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow('Simple ASL Detection', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('h'):
            show_help = not show_help
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_simple_asl()
