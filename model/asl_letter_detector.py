"""
ASL Letter Recognition System
Detects ASL letters A, B, C, D, E based on finger patterns and hand shape
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict
from finger_detection import FingerDetector

class ASLLetterDetector:
    def __init__(self):
        self.finger_detector = FingerDetector()
        self.letter_patterns = {
            'A': {'fingers': 1, 'description': 'Fist with thumb out'},
            'B': {'fingers': 5, 'description': 'Open hand with all fingers extended'},
            'C': {'fingers': 3, 'description': 'Curved hand like letter C'},
            'D': {'fingers': 1, 'description': 'Index finger pointing up'},
            'E': {'fingers': 0, 'description': 'Fist with all fingers closed'}
        }
        
        # Confidence thresholds
        self.min_confidence = 0.6
        self.stable_frames = 5  # Number of frames to confirm detection
        
        # Detection history for stability
        self.detection_history = []
        self.current_letter = None
        self.confidence = 0.0

    def detect_asl_letter(self, image: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Detect ASL letter from hand gesture
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Tuple of (detected_letter, confidence)
        """
        # Detect fingers first
        fingers_detected, finger_points = self.finger_detector.detect_fingers(image)
        
        if not fingers_detected:
            # No fingers detected - could be letter E (fist)
            detected_letter = 'E'
            confidence = 0.7
        else:
            # Count fingers and determine letter
            finger_count = len(finger_points)
            detected_letter, confidence = self._classify_by_finger_count(finger_count, finger_points)
        
        # Add to detection history for stability
        self.detection_history.append((detected_letter, confidence))
        if len(self.detection_history) > self.stable_frames:
            self.detection_history.pop(0)
        
        # Get stable detection
        stable_letter, stable_confidence = self._get_stable_detection()
        
        return stable_letter, stable_confidence

    def _classify_by_finger_count(self, finger_count: int, finger_points: List) -> Tuple[str, float]:
        """
        Classify ASL letter based on finger count and positions
        
        Args:
            finger_count: Number of detected fingers
            finger_points: List of finger tip positions
            
        Returns:
            Tuple of (letter, confidence)
        """
        if finger_count == 0:
            return 'E', 0.8  # Fist
        elif finger_count == 1:
            # Could be A (thumb) or D (index finger)
            return self._distinguish_a_or_d(finger_points)
        elif finger_count == 2:
            return 'C', 0.6  # Curved hand (might detect 2-3 fingers)
        elif finger_count == 3:
            return 'C', 0.7  # Curved hand
        elif finger_count == 4:
            return 'C', 0.6  # Curved hand (might detect 4 fingers)
        elif finger_count == 5:
            return 'B', 0.8  # Open hand
        else:
            return 'Unknown', 0.0

    def _distinguish_a_or_d(self, finger_points: List) -> Tuple[str, float]:
        """
        Distinguish between A (thumb) and D (index finger) when only 1 finger is detected
        
        Args:
            finger_points: List of finger tip positions
            
        Returns:
            Tuple of (letter, confidence)
        """
        if not finger_points:
            return 'A', 0.5
        
        # Get the finger position
        finger_x, finger_y = finger_points[0][0], finger_points[0][1]
        
        # Thumb (A) is typically on the left side, Index finger (D) is more centered
        if finger_x < 0.4:  # Left side of hand
            return 'A', 0.7  # Thumb out
        else:
            return 'D', 0.7  # Index finger up

    def _get_stable_detection(self) -> Tuple[Optional[str], float]:
        """
        Get stable detection from recent history
        
        Returns:
            Tuple of (stable_letter, average_confidence)
        """
        if len(self.detection_history) < self.stable_frames:
            return None, 0.0
        
        # Count occurrences of each letter
        letter_counts = {}
        total_confidence = 0.0
        
        for letter, confidence in self.detection_history:
            letter_counts[letter] = letter_counts.get(letter, 0) + 1
            total_confidence += confidence
        
        # Find most common letter
        most_common_letter = max(letter_counts, key=letter_counts.get)
        most_common_count = letter_counts[most_common_letter]
        
        # Check if detection is stable enough
        if most_common_count >= self.stable_frames * 0.6:  # 60% of frames
            avg_confidence = total_confidence / len(self.detection_history)
            return most_common_letter, avg_confidence
        
        return None, 0.0

    def draw_detection(self, image: np.ndarray, letter: str, confidence: float) -> np.ndarray:
        """
        Draw ASL letter detection on the image
        
        Args:
            image: Input image
            letter: Detected letter
            confidence: Detection confidence
            
        Returns:
            Image with detection drawn
        """
        annotated_image = image.copy()
        
        # Draw letter and confidence
        if letter and confidence > self.min_confidence:
            # Large letter display
            cv2.putText(annotated_image, f"ASL: {letter}", (50, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4)
            
            # Confidence bar
            bar_width = 200
            bar_height = 20
            bar_x = 50
            bar_y = 150
            
            # Background bar
            cv2.rectangle(annotated_image, (bar_x, bar_y), 
                         (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)
            
            # Confidence bar
            confidence_width = int(bar_width * confidence)
            color = (0, 255, 0) if confidence > 0.8 else (0, 255, 255) if confidence > 0.6 else (0, 0, 255)
            cv2.rectangle(annotated_image, (bar_x, bar_y), 
                         (bar_x + confidence_width, bar_y + bar_height), color, -1)
            
            # Confidence text
            cv2.putText(annotated_image, f"Confidence: {confidence:.2f}", (50, 190), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Letter description
            description = self.letter_patterns.get(letter, {}).get('description', '')
            cv2.putText(annotated_image, description, (50, 220), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        else:
            cv2.putText(annotated_image, "No ASL Letter Detected", (50, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        return annotated_image

    def get_letter_info(self, letter: str) -> Dict:
        """
        Get information about an ASL letter
        
        Args:
            letter: ASL letter
            
        Returns:
            Dictionary with letter information
        """
        return self.letter_patterns.get(letter, {})

def test_asl_detection():
    """Test ASL letter detection with webcam"""
    detector = ASLLetterDetector()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Could not open camera")
        return
    
    print("ASL Letter Detection Test")
    print("Show ASL letters A, B, C, D, E to the camera")
    print("Press 'q' to quit")
    print("Press 'h' to show help")
    print("Press 'c' to toggle contour view")
    
    show_contour = False
    show_help = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (640, 480))
        
        # Flip the frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Detect ASL letter
        letter, confidence = detector.detect_asl_letter(frame)
        
        # Draw detection
        frame = detector.draw_detection(frame, letter, confidence)
        
        # Show contour if requested
        if show_contour:
            frame = detector.finger_detector.draw_hand_contour(frame)
            cv2.putText(frame, "Contour View", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Show help if requested
        if show_help:
            help_text = [
                "ASL Letters:",
                "A: Fist with thumb out",
                "B: Open hand (5 fingers)",
                "C: Curved hand",
                "D: Index finger up",
                "E: Fist (no fingers)"
            ]
            for i, text in enumerate(help_text):
                cv2.putText(frame, text, (400, 50 + i * 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow('ASL Letter Detection', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            show_contour = not show_contour
        elif key == ord('h'):
            show_help = not show_help
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_asl_detection()
