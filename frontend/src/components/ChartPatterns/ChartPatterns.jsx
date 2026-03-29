import React from 'react'
import './ChartPatterns.css'

function ChartPatterns({ patterns }) {
  if (!patterns) {
    return null
  }

  const getRecommendationColor = (recommendation) => {
    switch (recommendation) {
      case 'BUY':
        return 'var(--secondary)' // MD3 Green
      case 'SELL':
        return 'var(--tertiary-container)' // MD3 Red
      case 'WAIT':
        return 'var(--primary-fixed-dim)' // MD3 Blue/Amber
      case 'HOLD':
        return 'var(--primary-container)' // MD3 Blue
      default:
        return 'var(--on-surface-variant)'
    }
  }

  const getPatternIndicator = (detected) => {
    return (
      <span className="material-symbols-outlined" style={{ color: detected ? 'var(--secondary)' : 'var(--outline)' }}>
        {detected ? 'check_circle' : 'cancel'}
      </span>
    )
  }

  const getStrengthColor = (strength) => {
    switch (strength) {
      case 'Strong':
        return 'var(--secondary)'
      case 'Moderate':
        return 'var(--primary)'
      case 'Weak':
        return 'var(--outline)'
      default:
        return 'var(--on-surface-variant)'
    }
  }

  const breakout = patterns.patterns_detected?.[0] || {}
  const support = patterns.patterns_detected?.[1] || {}
  const maCrossover = patterns.patterns_detected?.[2] || {}
  const successRates = patterns.success_rates || {}
  const recommendation = patterns.recommendation || 'HOLD'
  const reasoning = patterns.recommendation_reasoning || ''

  return (
    <div className="chart-patterns-container">
      Detected Patterns List
      <div className="patterns-section">
        <div className="section-header">
          <h3 className="section-title">
            <span className="material-symbols-outlined">analytics</span>
            Detected Price Patterns
          </h3>
          <span className="pattern-count">
            {patterns.pattern_count || 0} Pattern{patterns.pattern_count !== 1 ? 's' : ''} Active
          </span>
        </div>
        
        <div className="patterns-grid">
          {/* Breakout Pattern */}
          <div className={`pattern-card ${breakout.detected ? 'detected' : 'not-detected'}`}>
            <div className="pattern-indicator">
              {getPatternIndicator(breakout.detected)}
            </div>
            <div className="pattern-content">
              <h4 className="pattern-name">Breakout</h4>
              {breakout.detected ? (
                <>
                  <div className="pattern-detail">
                    <span className="detail-label">Resistance:</span>
                    <span className="detail-value">₹{breakout.resistance_level}</span>
                  </div>
                  <div className="pattern-detail">
                    <span className="detail-label">Current:</span>
                    <span className="detail-value">₹{breakout.current_price}</span>
                  </div>
                  <div className="pattern-detail">
                    <span className="detail-label">Margin:</span>
                    <span className="detail-value">{breakout.breakout_margin}%</span>
                  </div>
                  <div className="pattern-strength" style={{ color: getStrengthColor(breakout.strength) }}>
                    Confidence: {breakout.strength}
                  </div>
                </>
              ) : (
                <p className="pattern-status">Breakout pattern not confirmed in window</p>
              )}
            </div>
          </div>

          {/* Support Pattern */}
          <div className={`pattern-card ${support.detected ? 'detected' : 'not-detected'}`}>
            <div className="pattern-indicator">
              {getPatternIndicator(support.detected)}
            </div>
            <div className="pattern-content">
              <h4 className="pattern-name">Support Bounce</h4>
              {support.detected ? (
                <>
                  <div className="pattern-detail">
                    <span className="detail-label">Floor Support:</span>
                    <span className="detail-value">₹{support.support_level}</span>
                  </div>
                  <div className="pattern-detail">
                    <span className="detail-label">Current:</span>
                    <span className="detail-value">₹{support.current_price}</span>
                  </div>
                  <div className="pattern-detail">
                    <span className="detail-label">Distance:</span>
                    <span className="detail-value">+{support.distance_from_support}%</span>
                  </div>
                  <div className="pattern-strength" style={{ color: getStrengthColor(support.strength) }}>
                    Confidence: {support.strength}
                  </div>
                </>
              ) : (
                <p className="pattern-status">Support level test not active</p>
              )}
            </div>
          </div>

          {/* MA Crossover Pattern */}
          <div className={`pattern-card ${maCrossover.detected ? 'detected' : 'not-detected'}`}>
            <div className="pattern-indicator">
              {getPatternIndicator(maCrossover.detected)}
            </div>
            <div className="pattern-content">
              <h4 className="pattern-name">MA Crossover</h4>
              {maCrossover.detected ? (
                <>
                  <div className="pattern-detail">
                    <span className="detail-label">Type:</span>
                    <span className="detail-value">{maCrossover.crossover_type}</span>
                  </div>
                  <div className="pattern-detail">
                    <span className="detail-label">Distance:</span>
                    <span className="detail-value">{maCrossover.ma_distance}%</span>
                  </div>
                  <div className="pattern-strength" style={{ color: getStrengthColor(maCrossover.strength) }}>
                    Confidence: {maCrossover.strength}
                  </div>
                </>
              ) : (
                <p className="pattern-status">Moving average crossover not observed</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChartPatterns
