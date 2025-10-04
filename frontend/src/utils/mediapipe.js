// Mediapipe Hands integration utilities
// This file contains the actual Mediapipe implementation
// that will replace the placeholder logic in gestureDetector.js

import { Hands } from '@mediapipe/hands'
import { Camera } from '@mediapipe/camera_utils'

export class MediapipeHandDetector {
  constructor() {
    this.hands = null
    this.camera = null
    this.isInitialized = false
    this.onResults = null
  }

  async initialize() {
    try {
      this.hands = new Hands({
        locateFile: (file) => {
          return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
        }
      })

      this.hands.setOptions({
        maxNumHands: 1,
        modelComplexity: 1,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
      })

      this.hands.onResults((results) => {
        if (this.onResults) {
          this.onResults(results)
        }
      })

      this.isInitialized = true
      return true
    } catch (error) {
      console.error('Failed to initialize Mediapipe Hands:', error)
      return false
    }
  }

  async startCamera(videoElement) {
    if (!this.isInitialized) {
      throw new Error('Mediapipe not initialized')
    }

    this.camera = new Camera(videoElement, {
      onFrame: async () => {
        await this.hands.send({ image: videoElement })
      },
      width: 640,
      height: 480
    })

    await this.camera.start()
  }

  stopCamera() {
    if (this.camera) {
      this.camera.stop()
      this.camera = null
    }
  }

  setResultsCallback(callback) {
    this.onResults = callback
  }
}

// Utility function to extract hand landmarks
export const extractHandLandmarks = (results) => {
  if (!results.multiHandLandmarks || results.multiHandLandmarks.length === 0) {
    return null
  }

  // Get the first detected hand
  const landmarks = results.multiHandLandmarks[0]
  
  // Convert Mediapipe landmarks to our format
  return landmarks.map(landmark => ({
    x: landmark.x,
    y: landmark.y,
    z: landmark.z
  }))
}

// Utility function to calculate hand features
export const calculateHandFeatures = (landmarks) => {
  if (!landmarks || landmarks.length === 0) {
    return null
  }

  // Calculate distances between key points
  const thumbTip = landmarks[4]
  const indexTip = landmarks[8]
  const middleTip = landmarks[12]
  const ringTip = landmarks[16]
  const pinkyTip = landmarks[20]

  // Calculate distances
  const thumbIndexDistance = Math.sqrt(
    Math.pow(thumbTip.x - indexTip.x, 2) + 
    Math.pow(thumbTip.y - indexTip.y, 2)
  )

  const indexMiddleDistance = Math.sqrt(
    Math.pow(indexTip.x - middleTip.x, 2) + 
    Math.pow(indexTip.y - middleTip.y, 2)
  )

  // Calculate angles
  const thumbAngle = Math.atan2(thumbTip.y - landmarks[3].y, thumbTip.x - landmarks[3].x)
  const indexAngle = Math.atan2(indexTip.y - landmarks[5].y, indexTip.x - landmarks[5].x)

  return {
    distances: {
      thumbIndex: thumbIndexDistance,
      indexMiddle: indexMiddleDistance
    },
    angles: {
      thumb: thumbAngle,
      index: indexAngle
    },
    landmarks: landmarks
  }
}

export default MediapipeHandDetector

