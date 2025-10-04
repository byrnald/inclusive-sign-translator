// Text-to-Speech utility for ASL gesture translation
// This provides voice output for detected gestures

import { useState, useEffect, useCallback } from 'react'

class TextToSpeechService {
  constructor() {
    this.synth = window.speechSynthesis
    this.isEnabled = true
    this.voice = null
    this.lastSpokenText = ''
    this.speechTimeout = null
  }

  // Initialize TTS with preferred voice
  async initialize() {
    try {
      // Wait for voices to load
      if (this.synth.getVoices().length === 0) {
        await new Promise(resolve => {
          this.synth.onvoiceschanged = resolve
        })
      }

      // Find a suitable voice (prefer English voices)
      const voices = this.synth.getVoices()
      this.voice = voices.find(voice => 
        voice.lang.startsWith('en') && voice.localService
      ) || voices[0]

      console.log('Text-to-Speech initialized with voice:', this.voice?.name)
      return true
    } catch (error) {
      console.error('Failed to initialize TTS:', error)
      return false
    }
  }

  // Speak the detected gesture
  speakGesture(gesture, confidence) {
    if (!this.isEnabled || !this.synth) return

    // Don't repeat the same gesture too quickly
    const text = `Letter ${gesture}`
    if (text === this.lastSpokenText) return

    // Clear any existing speech
    this.synth.cancel()

    // Create speech utterance
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.voice = this.voice
    utterance.rate = 0.8
    utterance.pitch = 1.0
    utterance.volume = 0.7

    // Add confidence information if low
    if (confidence < 0.7) {
      utterance.text = `${text} (low confidence)`
    }

    // Speak the text
    this.synth.speak(utterance)
    this.lastSpokenText = text

    // Clear the last spoken text after a delay
    if (this.speechTimeout) {
      clearTimeout(this.speechTimeout)
    }
    this.speechTimeout = setTimeout(() => {
      this.lastSpokenText = ''
    }, 2000)
  }

  // Speak a custom message
  speak(text) {
    if (!this.isEnabled || !this.synth) return

    this.synth.cancel()
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.voice = this.voice
    utterance.rate = 0.8
    utterance.pitch = 1.0
    utterance.volume = 0.7

    this.synth.speak(utterance)
  }

  // Enable/disable TTS
  setEnabled(enabled) {
    this.isEnabled = enabled
    if (!enabled) {
      this.synth.cancel()
    }
  }

  // Check if TTS is supported
  isSupported() {
    return 'speechSynthesis' in window
  }

  // Get available voices
  getVoices() {
    return this.synth.getVoices()
  }

  // Set specific voice
  setVoice(voiceName) {
    const voices = this.synth.getVoices()
    this.voice = voices.find(voice => voice.name === voiceName) || voices[0]
  }
}

// Create singleton instance
export const textToSpeech = new TextToSpeechService()

// React hook for TTS
export const useTextToSpeech = () => {
  const [isInitialized, setIsInitialized] = useState(false)
  const [isEnabled, setIsEnabled] = useState(true)

  useEffect(() => {
    const initTTS = async () => {
      const success = await textToSpeech.initialize()
      setIsInitialized(success)
    }
    
    initTTS()
  }, [])

  const speakGesture = useCallback((gesture, confidence) => {
    if (isInitialized && isEnabled) {
      textToSpeech.speakGesture(gesture, confidence)
    }
  }, [isInitialized, isEnabled])

  const speak = useCallback((text) => {
    if (isInitialized && isEnabled) {
      textToSpeech.speak(text)
    }
  }, [isInitialized, isEnabled])

  const toggleEnabled = useCallback(() => {
    const newEnabled = !isEnabled
    setIsEnabled(newEnabled)
    textToSpeech.setEnabled(newEnabled)
  }, [isEnabled])

  return {
    isInitialized,
    isEnabled,
    speakGesture,
    speak,
    toggleEnabled,
    isSupported: textToSpeech.isSupported()
  }
}

export default textToSpeech
