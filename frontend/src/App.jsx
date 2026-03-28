import React from 'react'
import Header from './components/Header/Header'
import StockSelector from './components/StockSelector/StockSelector'
import Dashboard from './components/Dashboard/Dashboard'
import ErrorBoundary from './components/ErrorBoundary/ErrorBoundary'
import { analyzeStock, healthCheck } from './services/stockApi'
import { getDemoResponse } from './constants/mockData'
import './App.css'

function App() {
  const [selectedStock, setSelectedStock] = React.useState('AAPL')
  const [analysisData, setAnalysisData] = React.useState(null)
  const [isLoading, setIsLoading] = React.useState(false)
  const [error, setError] = React.useState(null)
  const [isBackendReady, setIsBackendReady] = React.useState(true)
  const [demoMode, setDemoMode] = React.useState(true) // Demo mode ON by default

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
      <div className="app">
        <Header demoMode={demoMode} onDemoModeChange={setDemoMode} />
        <main className="app-main">
          <StockSelector 
            selectedStock={selectedStock} 
            onSelectStock={handleStockSelect}
            onAnalyze={handleAnalyze}
            isLoading={isLoading}
            isBackendReady={isBackendReady}
          />
          
          {/* Error Message */}
          {error && (
            <div className="error-message">
              <span>⚠️ {error}</span>
              {error.includes('not running') && (
                <small>Backend API should be running on http://localhost:8000</small>
              )}
            </div>
          )}

          {/* Loading Spinner */}
          {isLoading && (
            <div className="loading-overlay">
              <div className="spinner"></div>
              <p>Analyzing {selectedStock}...</p>
            </div>
          )}

          {/* Dashboard Results */}
          {analysisData && !isLoading && <Dashboard data={analysisData} />}
        </main>
      </div>
    </ErrorBoundary>
  )
}

export default App
