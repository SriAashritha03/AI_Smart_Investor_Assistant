import React, { useState, useEffect } from 'react'
import { getDemoResponse } from '../../constants/mockData'
import { getAvailableStocks } from '../../services/stockApi'
import './Watchlist.css'

function Watchlist() {
  const [watchlistData, setWatchlistData] = useState([])
  const [loading, setLoading] = useState(true)
  const [showAll, setShowAll] = useState(false)

  useEffect(() => {
    const loadWatchlistData = async () => {
      setLoading(true)
      try {
        const response = await getAvailableStocks()
        const availableStocks = (response.stocks || []).map(s => s.symbol)
        
        const data = availableStocks.map(ticker => {
          const demoResponse = getDemoResponse(ticker)
          return {
            stock: ticker,
            opportunity_level: demoResponse.opportunity_level,
            confidence: demoResponse.confidence,
            action: demoResponse.action,
            signals_triggered: demoResponse.signals_triggered.length,
            total_signals: demoResponse.signal_details.length
          }
        })
        setWatchlistData(data)
      } catch (error) {
        console.error('Error loading watchlist:', error)
        const defaultStocks = ['AAPL', 'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'MSFT', 'TSLA']
        const fallbackData = defaultStocks.map(ticker => {
          const demoResponse = getDemoResponse(ticker)
          return {
            stock: ticker,
            opportunity_level: demoResponse.opportunity_level,
            confidence: demoResponse.confidence,
            action: demoResponse.action,
            signals_triggered: demoResponse.signals_triggered.length,
            total_signals: demoResponse.signal_details.length
          }
        })
        setWatchlistData(fallbackData)
      } finally {
        setLoading(false)
      }
    }

    loadWatchlistData()
  }, [])

  const getOpportunityStyle = (level) => {
    switch (level) {
      case 'Strong':   return { color: 'var(--secondary)', background: 'rgba(74, 225, 118, 0.1)', borderColor: 'rgba(74, 225, 118, 0.2)' }
      case 'Moderate': return { color: 'var(--primary)', background: 'rgba(173, 198, 255, 0.1)', borderColor: 'rgba(173, 198, 255, 0.2)' }
      case 'Weak':     return { color: 'var(--on-surface-variant)', background: 'rgba(66, 71, 84, 0.1)', borderColor: 'rgba(66, 71, 84, 0.2)' }
      default:         return { color: 'var(--outline)', background: 'rgba(66, 71, 84, 0.05)', borderColor: 'rgba(66, 71, 84, 0.1)' }
    }
  }

  const getActionStyle = (action) => {
    switch (action) {
      case 'BUY':  return { color: 'var(--secondary)', background: 'rgba(74, 225, 118, 0.1)', borderColor: 'rgba(74, 225, 118, 0.2)' }
      case 'HOLD': return { color: 'var(--primary)', background: 'rgba(173, 198, 255, 0.1)', borderColor: 'rgba(173, 198, 255, 0.2)' }
      case 'PASS': return { color: 'var(--tertiary-container)', background: 'rgba(255, 180, 171, 0.1)', borderColor: 'rgba(255, 180, 171, 0.2)' }
      default:     return { color: 'var(--outline)', background: 'rgba(66, 71, 84, 0.05)', borderColor: 'rgba(66, 71, 84, 0.1)' }
    }
  }

  const getConfidenceColor = (conf) => {
    if (conf >= 70) return 'var(--secondary)'
    if (conf >= 50) return 'var(--primary)'
    return 'var(--outline)'
  }

  if (loading) {
    return (
      <div className="watchlist-container">
        <div className="watchlist-loading">
          <div className="spinner-small"></div>
          <p>Initialising market matrix...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="watchlist-container">
      <div className="watchlist-header">
        <h3 className="watchlist-title">
          <span className="material-symbols-outlined">visibility</span>
          Market Watchlist
        </h3>
        <div className="watchlist-info">
          <span className="info-badge">{watchlistData.length} Assets</span>
          <span className="info-subtitle">Omni-Channel Stream</span>
        </div>
      </div>

      <div className="watchlist-table-wrapper">
        <table className="watchlist-table">
          <thead>
            <tr className="table-header-row">
              <th className="column-stock">Asset</th>
              <th className="column-opportunity">Sentiment</th>
              <th className="column-confidence">Quality</th>
              <th className="column-action">Logic</th>
              <th className="column-signals">Signals</th>
            </tr>
          </thead>
          <tbody>
            {watchlistData.slice(0, showAll ? watchlistData.length : 5).map((item, idx) => (
              <tr key={idx} className="table-body-row">
                <td className="cell-stock">
                  <div className="stock-info">
                    <span className="material-symbols-outlined stock-icon">monitoring</span>
                    <span className="stock-name">{item.stock}</span>
                  </div>
                </td>

                <td className="cell-opportunity">
                  <span className="opportunity-badge" style={getOpportunityStyle(item.opportunity_level)}>
                    {item.opportunity_level}
                  </span>
                </td>

                <td className="cell-confidence">
                  <div className="confidence-cell">
                    <span className="confidence-number">{item.confidence}%</span>
                    <div className="confidence-mini-bar">
                      <div
                        className="confidence-fill"
                        style={{ width: `${item.confidence}%`, background: getConfidenceColor(item.confidence) }}
                      ></div>
                    </div>
                  </div>
                </td>

                <td className="cell-action">
                  <span className="action-badge" style={getActionStyle(item.action)}>
                    {item.action}
                  </span>
                </td>

                <td className="cell-signals">
                  <div className="signal-indicator">
                    <span className="signal-triggered">{item.signals_triggered}</span>
                    <span className="signal-separator">/</span>
                    <span className="signal-total">{item.total_signals}</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {watchlistData.length > 5 && (
          <div className="watchlist-show-more">
            <button 
              className="show-more-button"
              onClick={() => setShowAll(!showAll)}
            >
              {showAll ? '▲ Show Less' : `▼ Show More (${watchlistData.length - 5} more stocks)`}
            </button>
          </div>
        )}
      </div>

      <div className="watchlist-footer">
        <div className="footer-legend">
          <div className="legend-item">
            <span className="legend-label">Confidence:</span>
            <div className="legend-values">
              <span className="legend-value" style={{ color: 'var(--secondary)' }}>High</span>
              <span className="legend-value" style={{ color: 'var(--primary)' }}>Medium</span>
              <span className="legend-value" style={{ color: 'var(--outline)' }}>Low</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Watchlist
