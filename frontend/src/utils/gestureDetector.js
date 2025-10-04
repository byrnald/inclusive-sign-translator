import { useState, useCallback, useRef } from 'react'
import { MediapipeHandDetector, extractHandLandmarks, calculateHandFeatures } from './mediapipe'
import { gestureAPI } from './api'

// Real gesture detection using Mediapipe + ML model integration
const useGestureDetection = () => {
  const [isInitialized, setIsInitialized] = useState(false)
  const [isDetecting, setIsDetecting] = useState(false)
  const handDetectorRef = useRef(null)
  const lastDetectionTime = useRef(0)
  const detectionInterval = 200 // Detect every 200ms to avoid overwhelming the system

  // Initialize Mediapipe Hands
  const initializeMediapipe = useCallback(async () => {
    try {
      if (handDetectorRef.current) {
        return true
      }

      handDetectorRef.current = new MediapipeHandDetector()
      const success = await handDetectorRef.current.initialize()
      
      if (success) {
        console.log('Mediapipe Hands initialized successfully')
        setIsInitialized(true)
        return true
      } else {
        console.error('Failed to initialize Mediapipe Hands')
        return false
      }
    } catch (error) {
      console.error('Failed to initialize Mediapipe:', error)
      return false
    }
  }, [])

  // Detect gesture from video frame using Mediapipe
  const detectGesture = useCallback(async (videoElement) => {
    if (!isInitialized || !handDetectorRef.current) {
      await initializeMediapipe()
    }

    // Throttle detection to avoid overwhelming the system
    const now = Date.now()
    if (now - lastDetectionTime.current < detectionInterval) {
      return { gesture: 'none', confidence: 0 }
    }
    lastDetectionTime.current = now

    try {
      // Set up results callback for Mediapipe
      let detectionResult = { gesture: 'none', confidence: 0 }
      
      handDetectorRef.current.setResultsCallback((results) => {
        const landmarks = extractHandLandmarks(results)
        
        if (landmarks) {
          const features = calculateHandFeatures(landmarks)
          
          if (features) {
            // For now, use simple rule-based detection
            // TODO: Replace with actual ML model classification
            const gesture = classifyGestureFromFeatures(features)
            detectionResult = gesture
          }
        }
      })

      // Process the current video frame
      await handDetectorRef.current.hands.send({ image: videoElement })
      
      return detectionResult
    } catch (error) {
      console.error('Gesture detection error:', error)
      return {
        gesture: 'none',
        confidence: 0
      }
    }
  }, [isInitialized, initializeMediapipe])

  // Simple rule-based gesture classification (placeholder for ML model)
  const classifyGestureFromFeatures = (features) => {
    const { distances, angles } = features
    
    // Simple rules based on finger distances and angles
    // These are placeholder rules - replace with actual ML model
    if (distances.thumbIndex < 0.1) {
      return { gesture: 'A', confidence: 0.8 }
    } else if (distances.thumbIndex > 0.2 && distances.indexMiddle < 0.1) {
      return { gesture: 'B', confidence: 0.7 }
    } else if (distances.thumbIndex > 0.15 && distances.indexMiddle > 0.15) {
      return { gesture: 'C', confidence: 0.75 }
    } else if (distances.thumbIndex > 0.2 && distances.indexMiddle > 0.1) {
      return { gesture: 'D', confidence: 0.7 }
    } else if (distances.thumbIndex > 0.25) {
      return { gesture: 'E', confidence: 0.8 }
    }
    
    return { gesture: 'none', confidence: 0 }
  }

  // Start continuous detection
  const startDetection = useCallback(async (videoElement) => {
    if (!isInitialized) {
      await initializeMediapipe()
    }
    
    if (handDetectorRef.current) {
      setIsDetecting(true)
      await handDetectorRef.current.startCamera(videoElement)
    }
  }, [isInitialized, initializeMediapipe])

  // Stop detection
  const stopDetection = useCallback(() => {
    if (handDetectorRef.current) {
      handDetectorRef.current.stopCamera()
      setIsDetecting(false)
    }
  }, [])

  return {
    detectGesture,
    startDetection,
    stopDetection,
    isInitialized,
    isDetecting
  }
}

export { useGestureDetection }

// Utility functions for hand landmark processing
export const processHandLandmarks = (landmarks) => {
  // TODO: Process Mediapipe hand landmarks
  // Extract relevant features for gesture classification
  // Normalize coordinates, calculate distances, angles, etc.
  
  return {
    // Processed features for ML model
    features: []
  }
}

// Gesture classification model (placeholder)
export const classifyGesture = async (features) => {
  // TODO: Load and run trained ML model
  // Return gesture prediction with confidence
  
  return {
    gesture: 'A',
    confidence: 0.85
  }
}

// Mediapipe Hands configuration
export const handsConfig = {
  maxNumHands: 1,
  modelComplexity: 1,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5
}

