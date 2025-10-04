import React, { useState } from 'react'
import CameraFeed from './components/CameraFeed'
import Header from './components/Header'
import GestureDisplay from './components/GestureDisplay'
import { useTextToSpeech } from './utils/textToSpeech'

function App() {
  const [isDetecting, setIsDetecting] = useState(false)
  const [detectedGesture, setDetectedGesture] = useState('')
  const [confidence, setConfidence] = useState(0)
  
  const { speakGesture, isEnabled: ttsEnabled, toggleEnabled: toggleTTS } = useTextToSpeech()

  const handleGestureDetected = (gesture, conf) => {
    setDetectedGesture(gesture)
    setConfidence(conf)
    
    // Speak the detected gesture
    if (gesture && gesture !== 'none') {
      speakGesture(gesture, conf)
    }
  }

  const toggleDetection = () => {
    setIsDetecting(!isDetecting)
    if (!isDetecting) {
      setDetectedGesture('')
      setConfidence(0)
    }
  }

  return (
    <div className="min-h-screen bg-dark-bg">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Camera Feed Section */}
          <div className="card">
            <h2 className="text-2xl font-semibold mb-4 text-gradient">
              Camera Feed
            </h2>
            <CameraFeed 
              isDetecting={isDetecting}
              onGestureDetected={handleGestureDetected}
            />
            <div className="mt-4 flex gap-4">
              <button
                onClick={toggleDetection}
                className={`btn-primary ${isDetecting ? 'bg-red-600 hover:bg-red-700' : ''}`}
              >
                {isDetecting ? 'Stop Detection' : 'Start Detection'}
              </button>
              <button 
                onClick={toggleTTS}
                className={`btn-secondary ${ttsEnabled ? 'bg-green-600 hover:bg-green-700' : ''}`}
              >
                {ttsEnabled ? '🔊 Voice On' : '🔇 Voice Off'}
              </button>
              <button className="btn-secondary">
                Calibrate
              </button>
            </div>
          </div>

          {/* Gesture Display Section */}
          <div className="card">
            <h2 className="text-2xl font-semibold mb-4 text-gradient">
              Detected Gesture
            </h2>
            <GestureDisplay 
              gesture={detectedGesture}
              confidence={confidence}
              isDetecting={isDetecting}
            />
          </div>
        </div>

        {/* Instructions */}
        <div className="mt-8 card">
          <h3 className="text-xl font-semibold mb-4">How to Use</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-300">
            <div>
              <h4 className="font-medium text-white mb-2">1. Position Your Hand</h4>
              <p>Hold your hand in front of the camera with good lighting</p>
            </div>
            <div>
              <h4 className="font-medium text-white mb-2">2. Make ASL Signs</h4>
              <p>Try making the letters A, B, C, D, or E with your hand</p>
            </div>
            <div>
              <h4 className="font-medium text-white mb-2">3. See Results</h4>
              <p>Watch the detected letter appear in real-time</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App

