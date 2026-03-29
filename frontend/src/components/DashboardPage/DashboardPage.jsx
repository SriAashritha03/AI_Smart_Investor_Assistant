import React from 'react'
import StockSelector from '../StockSelector/StockSelector'
import Dashboard from '../Dashboard/Dashboard'
import { analyzeStock } from '../../services/stockApi'
import { getDemoResponse } from '../../constants/mockData'

function DashboardPage({ demoMode }) {
  const [selectedStock, setSelectedStock] = React.useState('AAPL')
  const [analysisData, setAnalysisData] = React.useState(null)
  const [isLoading, setIsLoading] = React.useState(false)
  const [error, setError] = React.useState(null)
  const [isBackendReady, setIsBackendReady] = React.useState(true)

  const handleStockSelect = (stock) => {
    setSelectedStock(stock)
    setError(null)
  }

  const handleAnalyze = async () => {
    setIsLoading(true)
    setError(null)

    try {
      let result;

      if (demoMode) {
        result = getDemoResponse(selectedStock)
        await new Promise((resolve) => setTimeout(resolve, 800))
      } else {
        result = await analyzeStock(selectedStock)
      }
      
      if (result.success) {
        const triggeredSignalNames = result.signals_triggered.map(signal => {
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
          news_sentiment: result.news_sentiment || null,
          event_signals: result.event_signals || null,
          chart_patterns: result.chart_patterns || null,
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
    <div className="page-container dashboard-page">
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
    </div>
  )
}

export default DashboardPage
