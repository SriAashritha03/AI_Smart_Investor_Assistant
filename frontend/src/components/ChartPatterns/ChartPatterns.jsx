import React from 'react'
import './ChartPatterns.css'

function ChartPatterns({ patterns }) {
  if (!patterns) {
    return null
  }

  const getRecommendationColor = (recommendation) => {
    switch (recommendation) {
      case 'BUY':
        return '#10b981' // Green
      case 'SELL':
        return '#ef4444' // Red
      case 'WAIT':
        return '#f59e0b' // Amber
      case 'HOLD':
        return '#3b82f6' // Blue
      default:
        return '#6b7280'
    }
  }

  const getRecommendationIcon = (recommendation) => {
    switch (recommendation) {
      case 'BUY':
        return '🟢'
      case 'SELL':
        return '🔴'
      case 'WAIT':
        return '🟡'
      case 'HOLD':
        return '🟠'
      default:
        return '⚪'
    }
  }

  const getPatternColor = (detected) => {
    return detected ? '#10b981' : '#9ca3af'
  }

  const getStrengthColor = (strength) => {
    switch (strength) {
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

  const breakout = patterns.patterns_detected?.[0] || {}
  const support = patterns.patterns_detected?.[1] || {}
  const maCrossover = patterns.patterns_detected?.[2] || {}
  const successRates = patterns.success_rates || {}
  const recommendation = patterns.recommendation || 'HOLD'
  const reasoning = patterns.recommendation_reasoning || ''

  return (
    <div className="chart-patterns-container">
      {/* Recommendation Section - HIGHLIGHTED */}
      <div className="recommendation-section">
        <div className="recommendation-header">
          <h3 className="recommendation-title">
            {getRecommendationIcon(recommendation)} Trading Recommendation
          </h3>
        </div>
        <div className="recommendation-card" style={{ borderLeftColor: getRecommendationColor(recommendation) }}>
          <div className="recommendation-value" style={{ color: getRecommendationColor(recommendation) }}>
            {recommendation}
          </div>
          <p className="recommendation-reasoning">{reasoning}</p>
        </div>
      </div>

      {/* Success Rates Section */}
      <div className="success-rates-section">
        <div className="section-header">
          <h3 className="section-title">📊 Historical Success Rates (Backtested)</h3>
        </div>
        <div className="success-rates-grid">
          <div className="success-rate-card">
            <div className="sr-label">Breakout Pattern</div>
            <div className="sr-value">{successRates.breakout || 0}%</div>
            <div className="sr-bar">
              <div className="sr-fill" style={{ width: `${successRates.breakout || 0}%` }}></div>
            </div>
          </div>
          <div className="success-rate-card">
            <div className="sr-label">Support Pattern</div>
            <div className="sr-value">{successRates.support || 0}%</div>
            <div className="sr-bar">
              <div className="sr-fill" style={{ width: `${successRates.support || 0}%` }}></div>
            </div>
          </div>
          <div className="success-rate-card">
            <div className="sr-label">MA Crossover</div>
            <div className="sr-value">{successRates.ma_crossover || 0}%</div>
            <div className="sr-bar">
              <div className="sr-fill" style={{ width: `${successRates.ma_crossover || 0}%` }}></div>
            </div>
          </div>
          <div className="success-rate-card overall">
            <div className="sr-label">Overall Success</div>
            <div className="sr-value">{successRates.overall || 0}%</div>
            <div className="sr-bar">
              <div className="sr-fill" style={{ width: `${successRates.overall || 0}%` }}></div>
            </div>
          </div>
        </div>
      </div>

      {/* Detected Patterns Section */}
      <div className="patterns-section">
        <div className="section-header">
          <h3 className="section-title">🎯 Detected Patterns</h3>
          <span className="pattern-count">
            {patterns.pattern_count || 0} Pattern{patterns.pattern_count !== 1 ? 's' : ''} Detected
          </span>
        </div>
        <div className="patterns-grid">
          {/* Breakout Pattern */}
          <div className={`pattern-card ${breakout.detected ? 'detected' : 'not-detected'}`}>
            <div className="pattern-indicator" style={{ color: getPatternColor(breakout.detected) }}>
              {breakout.detected ? '✓' : '✗'}
            </div>
            <div className="pattern-content">
              <h4 className="pattern-name">Breakout</h4>
              {breakout.detected ? (
                <>
                  <p className="pattern-detail">
                    <span className="detail-label">Resistance:</span>
                    <span className="detail-value">₹{breakout.resistance_level}</span>
                  </p>
                  <p className="pattern-detail">
                    <span className="detail-label">Current Price:</span>
                    <span className="detail-value">₹{breakout.current_price}</span>
                  </p>
                  <p className="pattern-detail">
                    <span className="detail-label">Margin:</span>
                    <span className="detail-value">{breakout.breakout_margin}%</span>
                  </p>
                  <div className="pattern-strength" style={{ color: getStrengthColor(breakout.strength) }}>
                    Strength: {breakout.strength}
                  </div>
                </>
              ) : (
                <p className="pattern-status">Breakout pattern does not exist in current market data</p>
              )}
            </div>
          </div>

          {/* Support Pattern */}
          <div className={`pattern-card ${support.detected ? 'detected' : 'not-detected'}`}>
            <div className="pattern-indicator" style={{ color: getPatternColor(support.detected) }}>
              {support.detected ? '✓' : '✗'}
            </div>
            <div className="pattern-content">
              <h4 className="pattern-name">Support Bounce</h4>
              {support.detected ? (
                <>
                  <p className="pattern-detail">
                    <span className="detail-label">Support Level:</span>
                    <span className="detail-value">₹{support.support_level}</span>
                  </p>
                  <p className="pattern-detail">
                    <span className="detail-label">Current Price:</span>
                    <span className="detail-value">₹{support.current_price}</span>
                  </p>
                  <p className="pattern-detail">
                    <span className="detail-label">Distance:</span>
                    <span className="detail-value">+{support.distance_from_support}%</span>
                  </p>
                  <div className="pattern-strength" style={{ color: getStrengthColor(support.strength) }}>
                    Strength: {support.strength}
                  </div>
                </>
              ) : (
                <p className="pattern-status">Support bounce pattern does not exist in current market data</p>
              )}
            </div>
          </div>

          {/* MA Crossover Pattern */}
          <div className={`pattern-card ${maCrossover.detected ? 'detected' : 'not-detected'}`}>
            <div className="pattern-indicator" style={{ color: getPatternColor(maCrossover.detected) }}>
              {maCrossover.detected ? '✓' : '✗'}
            </div>
            <div className="pattern-content">
              <h4 className="pattern-name">MA Crossover</h4>
              {maCrossover.detected ? (
                <>
                  <p className="pattern-detail">
                    <span className="detail-label">Type:</span>
                    <span className="detail-value">{maCrossover.crossover_type}</span>
                  </p>
                  <p className="pattern-detail">
                    <span className="detail-label">SMA50:</span>
                    <span className="detail-value">₹{maCrossover.sma50}</span>
                  </p>
                  <p className="pattern-detail">
                    <span className="detail-label">SMA200:</span>
                    <span className="detail-value">₹{maCrossover.sma200}</span>
                  </p>
                  <p className="pattern-detail">
                    <span className="detail-label">Distance:</span>
                    <span className="detail-value">{maCrossover.ma_distance}%</span>
                  </p>
                  <div className="pattern-strength" style={{ color: getStrengthColor(maCrossover.strength) }}>
                    Strength: {maCrossover.strength}
                  </div>
                </>
              ) : (
                <p className="pattern-status">Moving average crossover pattern does not exist in current market data</p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Pattern Interpretation Guide */}
      <div className="interpretation-guide">
        <div className="section-header">
          <h3 className="section-title">📚 Pattern Guide</h3>
        </div>
        <div className="guide-items">
          <div className="guide-item">
            <span className="guide-icon">📈</span>
            <div className="guide-content">
              <h4>Breakout</h4>
              <p>Price breaks above resistance with volume confirmation. Strong bullish signal.</p>
            </div>
          </div>
          <div className="guide-item">
            <span className="guide-icon">🔧</span>
            <div className="guide-content">
              <h4>Support Bounce</h4>
              <p>Price bounces from support level. Indicates potential reversal or consolidation.</p>
            </div>
          </div>
          <div className="guide-item">
            <span className="guide-icon">🔀</span>
            <div className="guide-content">
              <h4>MA Crossover</h4>
              <p>Golden Cross (bullish) or Death Cross (bearish) when SMA50 crosses SMA200.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChartPatterns
