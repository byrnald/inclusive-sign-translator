"""
ASL Training Helper
Helps collect training data and improve ASL letter detection
"""

import cv2
import numpy as np
import json
import os
from datetime import datetime
from finger_detection import FingerDetector

class ASLTrainingHelper:
    def __init__(self):
        self.finger_detector = FingerDetector()
        self.training_data = []
        self.current_letter = None
        self.data_dir = "training_data"
        
        # Create data directory
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def collect_sample(self, image, letter):
        """Collect a training sample"""
        # Detect fingers
        fingers_detected, finger_points = self.finger_detector.detect_fingers(image)
        
        if fingers_detected:
            finger_count = len(finger_points)
            sample = {
                'timestamp': datetime.now().isoformat(),
                'letter': letter,
                'finger_count': finger_count,
                'finger_points': finger_points,
                'image_shape': image.shape
            }
            self.training_data.append(sample)
            return True
        return False
    
    def save_training_data(self, filename=None):
        """Save collected training data"""
        if not filename:
            filename = f"asl_training_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(self.training_data, f, indent=2)
        
        print(f"Saved {len(self.training_data)} samples to {filepath}")
        return filepath
    
    def analyze_data(self):
        """Analyze collected training data"""
        if not self.training_data:
            print("No training data collected yet")
            return
        
        # Count samples per letter
        letter_counts = {}
        for sample in self.training_data:
            letter = sample['letter']
            letter_counts[letter] = letter_counts.get(letter, 0) + 1
        
        print("\nTraining Data Analysis:")
        print("=" * 30)
        for letter, count in letter_counts.items():
            print(f"{letter}: {count} samples")
        
        # Analyze finger counts
        finger_counts = {}
        for sample in self.training_data:
            count = sample['finger_count']
            finger_counts[count] = finger_counts.get(count, 0) + 1
        
        print("\nFinger Count Distribution:")
        for count, samples in finger_counts.items():
            print(f"{count} fingers: {samples} samples")

def training_session():
    """Interactive training session"""
    helper = ASLTrainingHelper()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Could not open camera")
        return
    
    print("ASL Training Session")
    print("Press keys to collect samples:")
    print("  'a' - Collect sample for letter A")
    print("  'b' - Collect sample for letter B") 
    print("  'c' - Collect sample for letter C")
    print("  'd' - Collect sample for letter D")
    print("  'e' - Collect sample for letter E")
    print("  's' - Save training data")
    print("  'p' - Print analysis")
    print("  'q' - Quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.flip(frame, 1)
        
        # Detect fingers
        fingers_detected, finger_points = helper.finger_detector.detect_fingers(frame)
        
        # Draw detection
        if fingers_detected:
            frame = helper.finger_detector.draw_fingers(frame, finger_points)
            cv2.putText(frame, f"Fingers: {len(finger_points)}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No fingers detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Show current letter
        if helper.current_letter:
            cv2.putText(frame, f"Current: {helper.current_letter}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        
        # Show sample count
        cv2.putText(frame, f"Samples: {len(helper.training_data)}", (10, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('ASL Training', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('a'):
            if helper.collect_sample(frame, 'A'):
                print("Collected sample for A")
        elif key == ord('b'):
            if helper.collect_sample(frame, 'B'):
                print("Collected sample for B")
        elif key == ord('c'):
            if helper.collect_sample(frame, 'C'):
                print("Collected sample for C")
        elif key == ord('d'):
            if helper.collect_sample(frame, 'D'):
                print("Collected sample for D")
        elif key == ord('e'):
            if helper.collect_sample(frame, 'E'):
                print("Collected sample for E")
        elif key == ord('s'):
            helper.save_training_data()
        elif key == ord('p'):
            helper.analyze_data()
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    training_session()
