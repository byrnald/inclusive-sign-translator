import React from 'react'

const Header = () => {
  return (
    <header className="bg-dark-surface border-b border-dark-border">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gradient">
              Inclusive Sign Translator
            </h1>
            <p className="text-gray-400 mt-1">
              Real-time ASL gesture recognition for beginners
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-sm text-gray-400">
              <span className="inline-block w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              Ready
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header

