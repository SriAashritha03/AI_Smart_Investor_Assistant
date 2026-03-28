import React, { useState, useEffect } from 'react'
import { getDemoResponse } from '../../constants/mockData'
import './Watchlist.css'

function Watchlist() {
  const [watchlistData, setWatchlistData] = useState([])
  const [loading, setLoading] = useState(true)

  const WATCHLIST_STOCKS = ['AAPL', 'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'MSFT', 'TSLA']

  useEffect(() => {
    const loadWatchlistData = async () => {
      setLoading(true)
      try {
        // Get demo responses for all stocks in watchlist
        const data = WATCHLIST_STOCKS.map(ticker => {
          const response = getDemoResponse(ticker)
          return {
            stock: ticker,
            opportunity_level: response.opportunity_level,
            confidence: response.confidence,
            action: response.action,
            signals_triggered: response.signals_triggered.length,
            total_signals: response.signal_details.length
          }
        })

        setWatchlistData(data)
      } catch (error) {
        console.error('Error loading watchlist:', error)
      } finally {
        setLoading(false)
      }
    }

    loadWatchlistData()
  }, [])

  const getOpportunityColor = (level) => {
    switch (level) {
      case 'Strong':
        return '#10b981'
      case 'Moderate':
        return '#f59e0b'
      case 'Weak':
        return '#3b82f6'
      default:
        return '#6b7280'
    }
  }

  const getActionColor = (action) => {
    switch (action) {
      case 'BUY':
        return '#10b981'
      case 'HOLD':
        return '#f59e0b'
      case 'PASS':
        return '#ef4444'
      default:
        return '#6b7280'
    }
  }

  const getOpportunityBgColor = (level) => {
    switch (level) {
      case 'Strong':
        return 'rgba(16, 185, 129, 0.1)'
      case 'Moderate':
        return 'rgba(245, 158, 11, 0.1)'
      case 'Weak':
        return 'rgba(59, 130, 246, 0.1)'
      default:
        return 'rgba(107, 114, 128, 0.1)'
    }
  }

  const getActionBgColor = (action) => {
    switch (action) {
      case 'BUY':
        return 'rgba(16, 185, 129, 0.1)'
      case 'HOLD':
        return 'rgba(245, 158, 11, 0.1)'
      case 'PASS':
        return 'rgba(239, 68, 68, 0.1)'
      default:
        return 'rgba(107, 114, 128, 0.1)'
    }
  }

  const getConfidenceBarColor = (confidence) => {
    if (confidence >= 70) return '#10b981'
    if (confidence >= 50) return '#f59e0b'
    return '#3b82f6'
  }

  if (loading) {
    return (
      <div className="watchlist-container">
        <div className="watchlist-loading">
          <div className="spinner-small"></div>
          <p>Loading watchlist data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="watchlist-container">
      <div className="watchlist-header">
        <h3 className="watchlist-title">👀 Watchlist</h3>
        <div className="watchlist-info">
          <span className="info-badge">{watchlistData.length} Stocks</span>
          <span className="info-subtitle">Real-time Analysis</span>
        </div>
      </div>

      <div className="watchlist-table-wrapper">
        <table className="watchlist-table">
          <thead>
            <tr className="table-header-row">
              <th className="column-stock">Stock</th>
              <th className="column-opportunity">Opportunity</th>
              <th className="column-confidence">Confidence</th>
              <th className="column-action">Action</th>
              <th className="column-signals">Signals</th>
            </tr>
          </thead>
          <tbody>
            {watchlistData.map((item, idx) => (
              <tr key={idx} className="table-body-row">
                <td className="cell-stock">
                  <div className="stock-info">
                    <span className="stock-icon">📊</span>
                    <span className="stock-name">{item.stock}</span>
                  </div>
                </td>

                <td className="cell-opportunity">
                  <span
                    className="opportunity-badge"
                    style={{
                      color: getOpportunityColor(item.opportunity_level),
                      backgroundColor: getOpportunityBgColor(item.opportunity_level),
                      borderColor: getOpportunityColor(item.opportunity_level)
                    }}
                  >
                    {item.opportunity_level}
                  </span>
                </td>

                <td className="cell-confidence">
                  <div className="confidence-cell">
                    <span className="confidence-number">{item.confidence}%</span>
                    <div className="confidence-mini-bar">
                      <div
                        className="confidence-fill"
                        style={{
                          width: `${item.confidence}%`,
                          backgroundColor: getConfidenceBarColor(item.confidence)
                        }}
                      ></div>
                    </div>
                  </div>
                </td>

                <td className="cell-action">
                  <span
                    className="action-badge"
                    style={{
                      color: getActionColor(item.action),
                      backgroundColor: getActionBgColor(item.action),
                      borderColor: getActionColor(item.action)
                    }}
                  >
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
      </div>

      <div className="watchlist-footer">
        <div className="footer-legend">
          <div className="legend-item">
            <span className="legend-label">Opportunity Levels:</span>
            <span className="legend-values">
              <span className="legend-value" style={{ color: '#10b981' }}>🟢 Strong</span>
              <span className="legend-value" style={{ color: '#f59e0b' }}>🟡 Moderate</span>
              <span className="legend-value" style={{ color: '#3b82f6' }}>🔵 Weak</span>
              <span className="legend-value" style={{ color: '#6b7280' }}>⚪ None</span>
            </span>
          </div>
          <div className="legend-item">
            <span className="legend-label">Actions:</span>
            <span className="legend-values">
              <span className="legend-value" style={{ color: '#10b981' }}>BUY</span>
              <span className="legend-value" style={{ color: '#f59e0b' }}>HOLD</span>
              <span className="legend-value" style={{ color: '#ef4444' }}>PASS</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Watchlist
