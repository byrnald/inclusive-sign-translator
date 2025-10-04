"""
Simple Finger Detection using Contour Analysis
This approach focuses on detecting individual fingers using contour defects
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional

class FingerDetector:
    def __init__(self):
        self.min_contour_area = 5000
        self.max_contour_area = 50000

    def detect_fingers(self, image: np.ndarray) -> Tuple[bool, Optional[List]]:
        """
        Detect fingers using contour analysis and convexity defects
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Tuple of (fingers_detected, finger_points)
        """
        # Convert to HSV for better skin detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define skin color range
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Create skin mask
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return False, None
        
        # Find the largest contour (hand)
        hand_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(hand_contour)
        
        if area < self.min_contour_area:
            return False, None
        
        # Find finger tips using convex hull
        finger_points = self._find_finger_tips(hand_contour, image.shape)
        
        if len(finger_points) >= 3:  # At least 3 fingers detected
            return True, finger_points
        
        return False, None
    
    def _find_finger_tips(self, contour: np.ndarray, image_shape: Tuple) -> List:
        """
        Find finger tips using convex hull analysis
        
        Args:
            contour: Hand contour
            image_shape: Shape of the input image
            
        Returns:
            List of finger tip points
        """
        # Find convex hull
        hull = cv2.convexHull(contour, returnPoints=True)
        
        # Find the center of the hand
        moments = cv2.moments(contour)
        if moments['m00'] == 0:
            return []
        
        center_x = int(moments['m10'] / moments['m00'])
        center_y = int(moments['m01'] / moments['m00'])
        
        # Find finger tips (points on convex hull that are far from center)
        finger_tips = []
        for point in hull:
            x, y = point[0]
            # Calculate distance from center
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            
            # If point is far from center and above the center (fingers are usually above palm)
            if distance > 50 and y < center_y:
                finger_tips.append([x / image_shape[1], y / image_shape[0], 0.0])
        
        # Sort finger tips by x-coordinate
        finger_tips.sort(key=lambda p: p[0])
        
        return finger_tips[:5]  # Maximum 5 fingers
    
    def draw_fingers(self, image: np.ndarray, finger_points: List) -> np.ndarray:
        """
        Draw detected finger points on the image
        
        Args:
            image: Input image
            finger_points: List of finger tip points
            
        Returns:
            Image with finger points drawn
        """
        annotated_image = image.copy()
        
        if finger_points:
            for i, point in enumerate(finger_points):
                # Convert normalized coordinates to pixel coordinates
                x = int(point[0] * image.shape[1])
                y = int(point[1] * image.shape[0])
                
                # Draw finger tip
                cv2.circle(annotated_image, (x, y), 8, (0, 255, 0), -1)
                cv2.putText(annotated_image, f"F{i+1}", (x + 10, y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return annotated_image
    
    def draw_hand_contour(self, image: np.ndarray) -> np.ndarray:
        """
        Draw the detected hand contour
        
        Args:
            image: Input image
            
        Returns:
            Image with hand contour drawn
        """
        # Convert to HSV for better skin detection
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define skin color range
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        # Create skin mask
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        annotated_image = image.copy()
        
        if contours:
            # Find the largest contour (hand)
            hand_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(hand_contour)
            
            if area > self.min_contour_area:
                # Draw the contour
                cv2.drawContours(annotated_image, [hand_contour], -1, (0, 255, 0), 2)
                
                # Draw convex hull
                hull = cv2.convexHull(hand_contour)
                cv2.drawContours(annotated_image, [hull], -1, (255, 0, 0), 2)
                
                # Draw center point
                moments = cv2.moments(hand_contour)
                if moments['m00'] != 0:
                    center_x = int(moments['m10'] / moments['m00'])
                    center_y = int(moments['m01'] / moments['m00'])
                    cv2.circle(annotated_image, (center_x, center_y), 5, (0, 0, 255), -1)
        
        return annotated_image

def test_finger_detection():
    """Test finger detection with webcam"""
    detector = FingerDetector()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Could not open camera")
        return
    
    print("Finger Detection Test")
    print("Press 'q' to quit")
    print("Press 'c' to toggle contour view")
    print("Green circles = Detected finger tips")
    
    show_contour = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (640, 480))
        
        # Detect fingers
        fingers_detected, finger_points = detector.detect_fingers(frame)
        
        if fingers_detected:
            print(f"Fingers detected: {len(finger_points)}")
            
            # Draw finger points
            frame = detector.draw_fingers(frame, finger_points)
            
            cv2.putText(frame, f"Fingers: {len(finger_points)}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No Fingers Detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Show contour if requested
        if show_contour:
            frame = detector.draw_hand_contour(frame)
            cv2.putText(frame, "Contour View", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        cv2.imshow('Finger Detection', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            show_contour = not show_contour
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_finger_detection()
