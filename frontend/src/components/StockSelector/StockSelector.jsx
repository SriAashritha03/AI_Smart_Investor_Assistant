import React from 'react'
import { getAvailableStocks } from '../../services/stockApi'
import './StockSelector.css'

function StockSelector({ selectedStock, onSelectStock, onAnalyze, isLoading = false, isBackendReady = true }) {
  const [stocks, setStocks] = React.useState([])
  const [stocksLoading, setStocksLoading] = React.useState(true)

  // Fetch available stocks on mount
  React.useEffect(() => {
    const fetchStocks = async () => {
      try {
        const response = await getAvailableStocks()
        setStocks(response.stocks || [])
      } catch (error) {
        console.error('Failed to fetch stocks:', error)
        // Fallback to default stocks if API fails
        setStocks([
          { symbol: 'AAPL', name: 'Apple Inc.' },
          { symbol: 'RELIANCE.NS', name: 'Reliance Industries' },
          { symbol: 'TCS.NS', name: 'Tata Consultancy Services' },
          { symbol: 'INFY.NS', name: 'Infosys Limited' },
        ])
      } finally {
        setStocksLoading(false)
      }
    }

    if (isBackendReady) {
      fetchStocks()
    } else {
      setStocksLoading(false)
    }
  }, [isBackendReady])

  const isButtonDisabled = isLoading || !isBackendReady

  return (
    <div className="stock-selector-container">
      <div className="stock-selector">
        <div className="selector-header">
          <h2 className="selector-title">Stock Selection</h2>
          <p className="selector-subtitle">Choose from {stocks.length} available stocks for analysis</p>
        </div>

        <div className="selector-controls">
          <div className="control-group">
            <label htmlFor="stock-dropdown" className="control-label">
              Select Stock ({stocks.length})
            </label>
            <select
              id="stock-dropdown"
              className="stock-dropdown"
              value={selectedStock}
              onChange={(e) => onSelectStock(e.target.value)}
              disabled={isLoading || stocksLoading}
            >
              {stocks.length === 0 ? (
                <option>Loading stocks...</option>
              ) : (
                stocks.map((stock) => (
                  <option key={stock.symbol} value={stock.symbol}>
                    {stock.symbol} - {stock.name} ({stock.market})
                  </option>
                ))
              )}
            </select>
            <span className="dropdown-icon">▼</span>
          </div>

          <button 
            className={`analyze-button ${isButtonDisabled ? 'disabled' : ''}`}
            onClick={onAnalyze}
            disabled={isButtonDisabled}
            title={!isBackendReady ? 'Backend API is not running' : isLoading ? 'Analyzing...' : 'Click to analyze'}
          >
            <span className="button-icon">{isLoading ? '⏳' : '⚡'}</span>
            <span className="button-text">{isLoading ? 'Analyzing...' : 'Analyze Stock'}</span>
          </button>
        </div>

        <div className="stock-info">
          <div className="info-item">
            <span className="info-label">Current Selection</span>
            <span className="info-value">{selectedStock}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Data Period</span>
            <span className="info-value">6 Months</span>
          </div>
          <div className="info-item">
            <span className="info-label">Analysis Type</span>
            <span className="info-value">Technical Signals</span>
          </div>
          <div className="info-item">
            <span className="info-label">Backend Status</span>
            <span className={`info-value ${isBackendReady ? 'status-ready' : 'status-error'}`}>
              {isBackendReady ? '🟢 Connected' : '🔴 Disconnected'}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default StockSelector
