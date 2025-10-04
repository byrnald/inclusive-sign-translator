// API utilities for backend communication
// This file handles communication with the Flask backend (if used)

const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:5000'

export class GestureAPI {
  constructor(baseURL = API_BASE_URL) {
    this.baseURL = baseURL
  }

  // Send video frame to backend for gesture detection
  async detectGestureFromFrame(imageData) {
    try {
      const response = await fetch(`${this.baseURL}/api/detect-gesture`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: imageData
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      return result
    } catch (error) {
      console.error('API request failed:', error)
      return {
        gesture: 'none',
        confidence: 0,
        error: error.message
      }
    }
  }

  // Send hand landmarks to backend for classification
  async classifyLandmarks(landmarks) {
    try {
      const response = await fetch(`${this.baseURL}/api/classify-landmarks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          landmarks: landmarks
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      return result
    } catch (error) {
      console.error('API request failed:', error)
      return {
        gesture: 'none',
        confidence: 0,
        error: error.message
      }
    }
  }

  // Get model status
  async getModelStatus() {
    try {
      const response = await fetch(`${this.baseURL}/api/model-status`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      return result
    } catch (error) {
      console.error('API request failed:', error)
      return {
        status: 'offline',
        error: error.message
      }
    }
  }

  // Upload training data
  async uploadTrainingData(data) {
    try {
      const response = await fetch(`${this.baseURL}/api/upload-training-data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      return result
    } catch (error) {
      console.error('API request failed:', error)
      return {
        success: false,
        error: error.message
      }
    }
  }
}

// Create API instance
export const gestureAPI = new GestureAPI()

// Utility function to convert canvas to base64
export const canvasToBase64 = (canvas) => {
  return canvas.toDataURL('image/jpeg', 0.8)
}

// Utility function to convert video frame to base64
export const videoFrameToBase64 = (videoElement) => {
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  
  canvas.width = videoElement.videoWidth
  canvas.height = videoElement.videoHeight
  
  ctx.drawImage(videoElement, 0, 0)
  
  return canvasToBase64(canvas)
}

export default GestureAPI

