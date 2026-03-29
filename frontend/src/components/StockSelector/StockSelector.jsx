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
          { symbol: 'AAPL', name: 'Apple Inc.', market: 'US' },
          { symbol: 'RELIANCE.NS', name: 'Reliance Industries', market: 'IN' },
          { symbol: 'TCS.NS', name: 'Tata Consultancy Services', market: 'IN' },
          { symbol: 'INFY.NS', name: 'Infosys Limited', market: 'IN' },
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
      {/* Page Title Section */}
      <div className="selector-header">
        <h1 className="selector-title">Market Overview</h1>
        <p className="selector-subtitle">Active Asset Terminal • Intelligence Center</p>
      </div>

      {/* Selector Controls Row */}
      <div className="selector-controls">
        <div className="control-group">
          <select
            id="stock-dropdown"
            className="stock-dropdown"
            value={selectedStock}
            onChange={(e) => onSelectStock(e.target.value)}
            disabled={isLoading || stocksLoading}
          >
            {stocks.length === 0 ? (
              <option>Loading available assets...</option>
            ) : (
              stocks.map((stock) => (
                <option key={stock.symbol} value={stock.symbol}>
                  {stock.symbol} — {stock.name}
                </option>
              ))
            )}
          </select>
          <span className="material-symbols-outlined dropdown-icon">expand_more</span>
        </div>

        <button 
          className={`analyze-button ${isButtonDisabled ? 'disabled' : ''}`}
          onClick={onAnalyze}
          disabled={isButtonDisabled}
          title={!isBackendReady ? 'Backend API is not running' : isLoading ? 'Analyzing...' : 'Run Analysis'}
        >
          <span className="material-symbols-outlined button-icon">
            {isLoading ? 'progress_activity' : 'analytics'}
          </span>
          <span className="button-text">{isLoading ? 'Analysing...' : 'Run Analysis'}</span>
        </button>
      </div>
    </div>
  )
}

export default StockSelector
