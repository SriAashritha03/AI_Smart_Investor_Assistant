import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header/Header'
import DashboardPage from './components/DashboardPage/DashboardPage'
import ChatPage from './components/ChatPage/ChatPage'
import ErrorBoundary from './components/ErrorBoundary/ErrorBoundary'
import { healthCheck } from './services/stockApi'
import './App.css'

function App() {
  const [isBackendReady, setIsBackendReady] = React.useState(true)
  const [error, setError] = React.useState(null)
  const [demoMode, setDemoMode] = React.useState(false) // Demo mode OFF by default - use real API

  // Check if backend is running on mount
  React.useEffect(() => {
    const checkBackend = async () => {
      const ready = await healthCheck()
      setIsBackendReady(ready)
      if (!ready) {
        setError('Backend API is not running. Make sure FastAPI server is started on localhost:8000')
      }
    }
    checkBackend()
  }, [])

  return (
    <ErrorBoundary>
      <Router>
        <div className="app">
          <Header demoMode={demoMode} onDemoModeChange={setDemoMode} />
          <main className="app-main">
            <Routes>
              <Route 
                path="/" 
                element={
                  <>
                    {error && (
                      <div className="error-message">
                        <span>⚠️ {error}</span>
                        {error.includes('not running') && (
                          <small>Backend API should be running on http://localhost:8000</small>
                        )}
                      </div>
                    )}
                    <DashboardPage demoMode={demoMode} />
                  </>
                } 
              />
              <Route path="/chat" element={<ChatPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </ErrorBoundary>
  )
}

export default App
