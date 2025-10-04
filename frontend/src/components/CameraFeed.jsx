import React, { useRef, useEffect, useState } from 'react'
import { useGestureDetection } from '../utils/gestureDetector'

const CameraFeed = ({ isDetecting, onGestureDetected }) => {
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const [isCameraReady, setIsCameraReady] = useState(false)
  const [error, setError] = useState(null)
  
  const { detectGesture, startDetection, stopDetection, isInitialized } = useGestureDetection()

  useEffect(() => {
    const initializeCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: {
            width: { ideal: 640 },
            height: { ideal: 480 },
            facingMode: 'user'
          }
        })
        
        if (videoRef.current) {
          videoRef.current.srcObject = stream
          videoRef.current.onloadedmetadata = () => {
            setIsCameraReady(true)
            setError(null)
          }
        }
      } catch (err) {
        console.error('Error accessing camera:', err)
        setError('Camera access denied or not available')
      }
    }

    initializeCamera()

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks()
        tracks.forEach(track => track.stop())
      }
    }
  }, [])

  useEffect(() => {
    if (!isDetecting || !isCameraReady || !isInitialized) return

    const detectLoop = async () => {
      if (videoRef.current) {
        const gesture = await detectGesture(videoRef.current)
        if (gesture && gesture.gesture !== 'none') {
          onGestureDetected(gesture.gesture, gesture.confidence)
        }
      }
      
      if (isDetecting) {
        requestAnimationFrame(detectLoop)
      }
    }

    detectLoop()
  }, [isDetecting, isCameraReady, isInitialized, detectGesture, onGestureDetected])

  // Handle Mediapipe camera integration
  useEffect(() => {
    if (isDetecting && isCameraReady && isInitialized && videoRef.current) {
      startDetection(videoRef.current)
    } else if (!isDetecting) {
      stopDetection()
    }
  }, [isDetecting, isCameraReady, isInitialized, startDetection, stopDetection])

  if (error) {
    return (
      <div className="aspect-video bg-dark-surface border border-dark-border rounded-lg flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-400 text-4xl mb-4">📷</div>
          <p className="text-red-400 mb-2">Camera Error</p>
          <p className="text-gray-400 text-sm">{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="relative">
      <div className="aspect-video bg-dark-surface border border-dark-border rounded-lg overflow-hidden">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="w-full h-full object-cover"
        />
        <canvas
          ref={canvasRef}
          className="absolute top-0 left-0 w-full h-full pointer-events-none"
          style={{ display: 'none' }}
        />
        
        {!isCameraReady && (
          <div className="absolute inset-0 flex items-center justify-center bg-dark-surface">
            <div className="text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-accent mx-auto mb-4"></div>
              <p className="text-gray-400">Initializing camera...</p>
            </div>
          </div>
        )}
        
        {isDetecting && isCameraReady && (
          <div className="absolute top-4 left-4 bg-red-600 text-white px-3 py-1 rounded-full text-sm font-medium">
            <span className="animate-pulse">●</span> Detecting
          </div>
        )}
      </div>
      
      <div className="mt-4 text-sm text-gray-400">
        <p>💡 Make sure you have good lighting and your hand is clearly visible</p>
      </div>
    </div>
  )
}

export default CameraFeed

