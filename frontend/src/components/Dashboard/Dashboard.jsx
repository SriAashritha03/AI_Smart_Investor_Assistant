import React from 'react'
import StockChart from '../StockChart/StockChart'
import ChartPatterns from '../ChartPatterns/ChartPatterns'
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

  const getSignalStrengthColor = (strength) => {
    switch (strength) {
      case 'Strong':
        return '#22c55e'
      case 'Moderate':
        return '#f59e0b'
      case 'Weak':
        return '#3b82f6'
      default:
        return '#6b7280'
    }
  }

  const getSignalStrengthBadge = (strength) => {
    switch (strength) {
      case 'Strong':
        return '🟢'
      case 'Moderate':
        return '🟡'
      case 'Weak':
        return '🔵'
      default:
        return '⚪'
    }
  }

  const generateCombinedInsight = () => {
    const hasBreakout = data.signals_triggered.includes('Breakout')
    const hasUptrend = data.signals_triggered.includes('Uptrend')
    const hasVolumeSpike = data.signals_triggered.includes('Volume Spike')
    const hasPriceSurge = data.signals_triggered.includes('Price Surge')
    const sentiment = data.news_sentiment?.sentiment_label?.toLowerCase() || ''
    const hasPositiveSentiment = sentiment === 'positive'
    const hasNegativeSentiment = sentiment === 'negative'
    const hasPriceSpike = data.event_signals?.events_detected?.includes('Price Spike')
    const hasVolumeSurge = data.event_signals?.events_detected?.includes('Volume Surge')

    // Strong bullish setup
    if ((hasBreakout || hasUptrend) && (hasVolumeSpike || hasVolumeSurge) && hasPositiveSentiment) {
      return '💡 Strong bullish setup: Positive sentiment + Technical breakout + Volume confirmation = High conviction opportunity'
    }

    // Moderate bullish
    if ((hasBreakout || hasUptrend) && hasPositiveSentiment) {
      return '💡 Moderate bullish setup: Positive sentiment backing technical strength = Solid opportunity'
    }

    // Price action with momentum
    if ((hasPriceSurge || hasPriceSpike) && (hasVolumeSpike || hasVolumeSurge)) {
      return '💡 Strong momentum detected: Price surge + Volume increase = Short-term buying pressure'
    }

    // Bearish setup
    if (hasNegativeSentiment && data.opportunity_level === 'None') {
      return '⚠️ Bearish sentiment: Negative news with no technical support = Avoid until sentiment improves'
    }

    // Mixed signals
    if (data.signals_triggered.length > 0 && hasPositiveSentiment) {
      return '💡 Mixed signals with positive sentiment: Monitor for confirmation before entry'
    }

    // No clear setup
    if (data.signals_triggered.length === 0) {
      return '👀 No clear signals detected: Waiting for technical setup or sentiment change'
    }

    // Default
    return '📊 Monitor for emerging opportunity based on current signals and market sentiment'
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

      {/* Combined Insight Section - HIGH IMPACT */}
      <div className="dashboard-section combined-insight-section">
        <div className="combined-insight-content">
          <div className="combined-insight-label">💡 AI Insight</div>
          <div className="combined-insight-text">{generateCombinedInsight()}</div>
        </div>
      </div>

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
          <span className="confidence-explanation">Based on combined signals + sentiment analysis</span>
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
            <div className="section-title-group">
              <h3 className="section-title">⚡ Signal Details</h3>
              <span className="help-text" title="Technical indicators like momentum, volatility, and trend that trigger buy/hold/sell signals">ℹ️ Tech Signals</span>
            </div>
            <h3 className="section-title">🎯 Opportunity Radar - Signal Details</h3>
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
                    <div className="signal-badges">
                      <span className={`signal-strength strength-${signal.strength.toLowerCase()}`}>
                        {getSignalStrengthBadge(signal.strength)} {signal.strength}
                      </span>
                    </div>
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

        {/* Why Different Responses - Explanation */}
        <div className="dashboard-section comparison-section">
          <div className="section-header">
            <h3 className="section-title">🤔 Why Different Responses?</h3>
          </div>
          <div className="section-content">
            <p className="comparison-intro">Signal Details and Chart Patterns use different analysis approaches, so they may provide different recommendations:</p>
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Factor</th>
                  <th>{' '}⚡Signals</th>
                  <th>📊 Patterns</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="factor-label">Analysis Type</td>
                  <td>Short-term indicators</td>
                  <td>Long-term trends</td>
                </tr>
                <tr>
                  <td className="factor-label">Data Used</td>
                  <td>Last 10-20 days</td>
                  <td>1 year history</td>
                </tr>
                <tr>
                  <td className="factor-label">Reasoning</td>
                  <td>Current momentum</td>
                  <td>Historical patterns</td>
                </tr>
                <tr>
                  <td className="factor-label">Actions Available</td>
                  <td>BUY, HOLD, PASS</td>
                  <td>BUY, SELL, HOLD, WAIT ✅</td>
                </tr>
              </tbody>
            </table>
            <p className="comparison-note">💡 <strong>Tip:</strong> For best results, consider both perspectives when making trading decisions. Signals show immediate opportunities, while patterns reveal proven historical strategies.</p>
          </div>
        </div>

        {/* Chart Patterns Analysis Section */}
        {data.chart_patterns && (
          <div className="dashboard-section chart-patterns-section">
            <ChartPatterns patterns={data.chart_patterns} />
          </div>
        )}

        {/* News Sentiment Section */}
        <div className="dashboard-section news-sentiment-section">
          <div className="section-header">
            <h3 className="section-title">📰 News Sentiment</h3>
            {data.news_sentiment && (
              <span className={`sentiment-badge sentiment-${data.news_sentiment.sentiment_label.toLowerCase()}`}>
                {data.news_sentiment.sentiment_label}
              </span>
            )}
          </div>
          {data.news_sentiment ? (
            <div className="section-content">
              <div className="sentiment-score-card">
                <span className="sentiment-label">Overall Sentiment</span>
                <div className="sentiment-display">
                  <span className={`sentiment-value sentiment-${data.news_sentiment.sentiment_label.toLowerCase()}`}>
                    {data.news_sentiment.sentiment_score > 0 ? '+' : ''}{data.news_sentiment.sentiment_score.toFixed(2)}
                  </span>
                  <span className="sentiment-range">(-1.0 to +1.0)</span>
                </div>
              </div>

              <div className="news-stats">
                <div className="stat-item">
                  <span className="stat-label">Articles Analyzed</span>
                  <span className="stat-value">{data.news_sentiment.articles_analyzed}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Confidence</span>
                  <span className="stat-value">{data.news_sentiment.confidence.toFixed(1)}%</span>
                </div>
              </div>

              <div className="confidence-bar-small">
                <div
                  className="confidence-fill-small"
                  style={{ width: `${data.news_sentiment.confidence}%` }}
                ></div>
              </div>

              {data.news_sentiment.top_headlines && data.news_sentiment.top_headlines.length > 0 && (
                <div className="headlines-list">
                  <span className="headlines-title">Top Headlines</span>
                  {data.news_sentiment.top_headlines.map((headline, idx) => (
                    <div key={idx} className="headline-item">
                      <span className="headline-bullet">•</span>
                      <span className="headline-text">{headline}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <p className="no-data">No sentiment data available</p>
          )}
        </div>

        {/* Event Signals Section */}
        <div className="dashboard-section event-signals-section">
          <div className="section-header">
            <h3 className="section-title">⚡ Event Signals</h3>
            {data.event_signals && data.event_signals.events_detected && (
              <span className="event-count">
                {data.event_signals.events_detected.length} Event(s)
              </span>
            )}
          </div>
          {data.event_signals ? (
            <div className="section-content">
              {/* Price Spike */}
              <div className={`event-item ${data.event_signals.price_spike.detected ? 'event-triggered' : 'event-not-triggered'}`}>
                <div className="event-header">
                  <div className="event-name-group">
                    <span className={`event-indicator ${data.event_signals.price_spike.detected ? 'active' : 'inactive'}`}>
                      {data.event_signals.price_spike.detected ? '⚠' : '○'}
                    </span>
                    <div className="event-title-group">
                      <span className="event-name">⚡ Price Spike Detected</span>
                      <span className="event-desc">(Short-term momentum indicator)</span>
                    </div>
                  </div>
                  {data.event_signals.price_spike.detected && (
                    <span className={`event-change event-${data.event_signals.price_spike.direction}`}>
                      {data.event_signals.price_spike.direction === 'upward' ? '↑' : '↓'} {Math.abs(data.event_signals.price_spike.change_percent).toFixed(2)}%
                    </span>
                  )}
                </div>
                <p className="event-description">{data.event_signals.price_spike.description}</p>
              </div>

              {/* Volume Surge */}
              <div className={`event-item ${data.event_signals.volume_surge.detected ? 'event-triggered' : 'event-not-triggered'}`}>
                <div className="event-header">
                  <div className="event-name-group">
                    <span className={`event-indicator ${data.event_signals.volume_surge.detected ? 'active' : 'inactive'}`}>
                      {data.event_signals.volume_surge.detected ? '📊' : '○'}
                    </span>
                    <div className="event-title-group">
                      <span className="event-name">📊 Volume Surge Detected</span>
                      <span className="event-desc">(Institutional or retail buying pressure)</span>
                    </div>
                  </div>
                  {data.event_signals.volume_surge.detected && (
                    <span className="event-ratio">
                      {data.event_signals.volume_surge.ratio.toFixed(2)}x
                    </span>
                  )}
                </div>
                <p className="event-description">{data.event_signals.volume_surge.description}</p>
                {data.event_signals.volume_surge.detected && (
                  <div className="volume-details">
                    <div className="volume-item">
                      <span className="volume-label">Current</span>
                      <span className="volume-value">{(data.event_signals.volume_surge.current_volume / 1000000).toFixed(1)}M</span>
                    </div>
                    <span className="volume-divider">/</span>
                    <div className="volume-item">
                      <span className="volume-label">Avg</span>
                      <span className="volume-value">{(data.event_signals.volume_surge.average_volume / 1000000).toFixed(1)}M</span>
                    </div>
                  </div>
                )}
              </div>

              {data.event_signals.summary && (
                <div className="event-summary">
                  <span className="event-summary-label">Summary</span>
                  <span className="event-summary-text">{data.event_signals.summary}</span>
                </div>
              )}
            </div>
          ) : (
            <p className="no-data">No event data available</p>
          )}
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
