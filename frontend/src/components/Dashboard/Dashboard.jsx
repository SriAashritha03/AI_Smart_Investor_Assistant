import React from 'react'
import StockChart from '../StockChart/StockChart'
import Watchlist from '../Watchlist/Watchlist'
import './Dashboard.css'
import Portfolio from "../Portfolio/Portfolio";
import VideoEngine from "../VideoEngine/VideoEngine";

function Dashboard({ data }) {
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

  const getSignalStatusClass = (triggered) => {
    return triggered ? 'signal-triggered' : 'signal-not-triggered'
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

  return (
    <div className={`dashboard-container ${data.isDemo ? 'demo-mode' : ''}`}>
      {/* Demo Mode Indicator */}
      {data.isDemo && (
        <div className="demo-indicator">
          <span className="demo-indicator-icon">🎭</span>
          <span className="demo-indicator-text">Demo Mode - Using Sample Data</span>
        </div>
      )}

      {/* Stock Chart Section */}
      <StockChart 
        stock={data.stock} 
        confidence={data.confidence}
        opportunityLevel={data.opportunity_level}
      />

      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="summary-card opportunity-card">
          <span className="card-label">Opportunity Level</span>
          <span
            className="card-value opportunity-value"
            style={{ color: getOpportunityColor(data.opportunity_level) }}
          >
            {data.opportunity_level}
          </span>
          <span className="card-sublabel">Technical Analysis</span>
          {data.isDemo && <span className="demo-chip">Demo</span>}
        </div>

        <div className="summary-card confidence-card">
          <span className="card-label">Confidence Score</span>
          <div className="confidence-display">
            <span className="card-value confidence-value">{data.confidence}%</span>
            <div className="confidence-bar">
              <div
                className="confidence-fill"
                style={{ width: `${data.confidence}%` }}
              ></div>
            </div>
          </div>
        </div>

        <div className="summary-card action-card">
          <span className="card-label">Recommended Action</span>
          <span
            className="card-value action-value"
            style={{ color: getActionColor(data.action) }}
          >
            {data.action}
          </span>
          <span className="card-sublabel">Trading Signal</span>
        </div>

        <div className="summary-card data-card">
          <span className="card-label">Data Points</span>
          <span className="card-value data-value">{data.data_points}</span>
          <span className="card-sublabel">Trading Days</span>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="dashboard-grid">
        {/* Analysis Summary */}
        <div className="dashboard-section summary-section">
          <div className="section-header">
            <h3 className="section-title">📋 Analysis Summary</h3>
          </div>
          <div className="section-content">
            <p className="summary-text">{data.summary}</p>
            <div className="analysis-meta">
              <div className="meta-item">
                <span className="meta-label">Stock</span>
                <span className="meta-value">{data.stock}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Analysis Date</span>
                <span className="meta-value">{data.date}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Signals Detail */}
        <div className="dashboard-section signals-section">
          <div className="section-header">
            <h3 className="section-title">⚡ Signal Details</h3>
            <span className="signal-count">
              {data.signals_triggered.length}/{data.signal_details.length} Triggered
            </span>
          </div>
          <div className="signals-list">
            {data.signal_details.map((signal, idx) => (
              <div
                key={idx}
                className={`signal-item ${getSignalStatusClass(signal.triggered)}`}
              >
                <div className="signal-header">
                  <div className="signal-name-group">
                    <span className={`signal-indicator ${signal.triggered ? 'active' : 'inactive'}`}>
                      {signal.triggered ? '✓' : '○'}
                    </span>
                    <span className="signal-name">{signal.name}</span>
                  </div>
                  {signal.triggered && (
                    <span className={`signal-strength strength-${signal.strength.toLowerCase()}`}>
                      {signal.strength}
                    </span>
                  )}
                </div>
                <p className="signal-reasoning">{signal.reasoning}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Triggered Signals Summary */}
        <div className="dashboard-section triggered-section">
          <div className="section-header">
            <h3 className="section-title">✓ Triggered Signals</h3>
          </div>
          <div className="triggered-list">
            {data.signals_triggered.length > 0 ? (
              data.signals_triggered.map((signal, idx) => (
                <div key={idx} className="triggered-item">
                  <span className="triggered-badge">✓</span>
                  <span className="triggered-name">{signal}</span>
                </div>
              ))
            ) : (
              <p className="no-signals">No signals currently triggered</p>
            )}
          </div>
        </div>
      </div>

      {/* Watchlist Section */}
      <Watchlist />
      <Portfolio />
      <VideoEngine />
    </div>
  )
}

export default Dashboard
