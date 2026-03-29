import React from 'react'
import { FaExclamationTriangle } from 'react-icons/fa'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header/Header'
import Sidebar from './components/Sidebar/Sidebar'
import StockSelector from './components/StockSelector/StockSelector'
import Dashboard from './components/Dashboard/Dashboard'
import AlertsModal from './components/AlertsModal/AlertsModal'
import DashboardPage from './components/DashboardPage/DashboardPage'
import ChatPage from './components/ChatPage/ChatPage'
import PortfolioPage from './components/PortfolioPage/PortfolioPage'
import VideoEnginePage from './components/VideoEnginePage/VideoEnginePage'
import ErrorBoundary from './components/ErrorBoundary/ErrorBoundary'
import { healthCheck, analyzeStock } from './services/stockApi'
import { getDemoResponse } from './constants/mockData'
import './App.css'

function App() {
  const [isBackendReady, setIsBackendReady] = React.useState(true)
  const [demoMode, setDemoMode] = React.useState(true) // Demo mode ON by default
  const [isAlertsOpen, setIsAlertsOpen] = React.useState(false)
  const [error, setError] = React.useState(null)
  const [selectedStock, setSelectedStock] = React.useState('AAPL')
  const [isLoading, setIsLoading] = React.useState(false)
  const [analysisData, setAnalysisData] = React.useState(null)

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

  const handleStockSelect = (stock) => {
    setSelectedStock(stock)
    setError(null) // Clear errors when selecting new stock
  }

  const handleAnalyze = async () => {
    setIsLoading(true)
    setError(null)

    try {
      let result;

      // Use demo data if demo mode is enabled
      if (demoMode) {
        result = getDemoResponse(selectedStock)
        // Simulate API delay for authenticity
        await new Promise((resolve) => setTimeout(resolve, 800))
      } else {
        // Call real API
        result = await analyzeStock(selectedStock)
      }
      
      if (result.success) {
        // Transform API response to match Dashboard component expectations
        const triggeredSignalNames = result.signals_triggered.map(signal => {
          // Handle both objects with signal_name and plain strings
          return typeof signal === 'string' ? signal : signal.signal_name || signal.name
        })
        
        setAnalysisData({
          stock: result.stock,
          date: new Date().toISOString().split('T')[0],
          opportunity_level: result.opportunity_level,
          confidence: result.confidence,
          action: result.action,
          signals_triggered: triggeredSignalNames,
          signal_details: result.signal_details,
          summary: result.summary,
          data_points: result.data_points,
          chart_patterns: result.chart_patterns,
          news_sentiment: result.news_sentiment,
          event_signals: result.event_signals,
          alerts: result.alerts,
          isDemo: demoMode,
        })
      } else {
        setError(result.error || 'Analysis failed')
      }
    } catch (err) {
      setError(`Error analyzing stock: ${err.message}`)
      console.error('Analysis error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <ErrorBoundary>
      <Router>
        <div className="app">
          {/* Persistent Sidebar (desktop) */}
          <Sidebar />

          {/* Top Header Bar */}
          <Header 
            demoMode={demoMode} 
            onDemoModeChange={setDemoMode}
            alerts={analysisData?.alerts || []}
            onAlertsToggle={() => setIsAlertsOpen(!isAlertsOpen)}
          />

          {/* Alerts Modal */}
          {isAlertsOpen && (
            <AlertsModal
              alerts={analysisData?.alerts || []}
              onClose={() => setIsAlertsOpen(false)}
            />
          )}

          {/* Main Content */}
          <main className="app-main">
            <Routes>
              <Route 
                path="/" 
                element={
                  <>
                    {error && (
                      <div className="error-message">
                        <span><FaExclamationTriangle style={{ marginRight: '8px' }} />{error}</span>
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
              <Route path="/portfolio" element={<PortfolioPage />} />
              <Route path="/video-engine" element={<VideoEnginePage />} />
            </Routes>
          </main>

          {/* Mobile Bottom Nav */}
          <MobileBottomNav />
        </div>
      </Router>
    </ErrorBoundary>
  )
}

/* ── Mobile Bottom Navigation (matches Stitch) ───────────────────────── */
function MobileBottomNav() {
  return (
    <nav className="mobile-bottom-nav">
      <a href="/" className="mobile-nav-btn mobile-nav-btn--active">
        <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>dashboard</span>
        <span>Dashboard</span>
      </a>
      <a href="/chat" className="mobile-nav-btn">
        <span className="material-symbols-outlined">chat_bubble</span>
        <span>Chat</span>
      </a>
      <a href="/portfolio" className="mobile-nav-btn">
        <span className="material-symbols-outlined">account_balance_wallet</span>
        <span>Assets</span>
      </a>
      <a href="/video-engine" className="mobile-nav-btn">
        <span className="material-symbols-outlined">videocam</span>
        <span>Video</span>
      </a>
    </nav>
  )
}

export default App
