import React from 'react'
import { FaCircle, FaLightbulb, FaExclamationTriangle, FaEye, FaChartBar, FaMask, FaClipboardList, FaBullseye, FaCheckCircle, FaNewspaper, FaBolt } from 'react-icons/fa'
import StockChart from '../StockChart/StockChart'
import ChartPatterns from '../ChartPatterns/ChartPatterns'
import OpportunityRadar from '../OpportunityRadar/OpportunityRadar'
import TradeInsightPanel from '../TradeInsightPanel/TradeInsightPanel'
import Watchlist from '../Watchlist/Watchlist'
import './Dashboard.css'

function Dashboard({ data }) {
  if (!data) return null;

  // DEBUG: Log data structure to console
  React.useEffect(() => {
    console.log('[Dashboard] Data received:', {
      stock: data.stock,
      has_explanation_block: !!data.explanation_block,
      explanation_block: data.explanation_block,
      has_score_breakdown: !!data.score_breakdown,
      score_breakdown: data.score_breakdown,
      has_signal_summary: !!data.signal_summary,
      action: data.action,
      confidence: data.confidence,
    })
  }, [data])

  const getOpportunityColor = (level) => {
    switch (level) {
      case 'Strong': return 'var(--secondary)';
      case 'Moderate': return 'var(--primary)';
      case 'Weak': return 'var(--on-surface-variant)';
      default: return 'var(--on-surface-variant)';
    }
  }

  const getActionColor = (action) => {
    switch (action) {
      case 'BUY': return 'var(--secondary)';
      case 'HOLD': return 'var(--primary)';
      case 'PASS': return 'var(--tertiary-container)';
      default: return 'var(--on-surface-variant)';
    }
  }

  const getSignalStrengthColor = (strength) => {
    switch (strength) {
      case 'Strong': return 'var(--secondary)';
      case 'Moderate': return 'var(--primary)';
      case 'Weak': return 'var(--outline)';
      default: return 'var(--outline)';
    }
  }

  const getRadarData = (data) => {
    if (!data) return null
    
    // CONSISTENT: Use backend score_breakdown values for radar
    // Ensures radar and score breakdown show same Technical score
    let technicalValue = 50  // default middle value
    
    if (data.score_breakdown?.technical !== undefined) {
      technicalValue = data.score_breakdown.technical
    } else {
      // Fallback: use same formula as backend
      const signalCount = data.signals_triggered?.length || 0
      const detectedPatterns = data.chart_patterns?.patterns_detected?.filter(p => p.detected).length || 0
      technicalValue = Math.min(100, (signalCount * 15) + (detectedPatterns * 20) + (data.confidence * 0.5))
    }
    
    return [
      {
        subject: 'Technical',
        value: technicalValue
      },
      {
        subject: 'Sentiment',
        value: data.score_breakdown?.sentiment !== undefined 
          ? Math.round(data.score_breakdown.sentiment)
          : (data.news_sentiment ? Math.round((data.news_sentiment.sentiment_score + 1) / 2 * 100) : 50)
      },
      {
        subject: 'Volume',
        value: data.event_signals?.volume_surge?.detected ? 75 : 40
      },
      {
        subject: 'Trend',
        value: data.opportunity_level === 'Strong' ? 80
             : data.opportunity_level === 'Moderate' ? 60
             : 40
      },
      {
        subject: 'Risk',
        value: Math.max(0, 100 - (data.confidence || 50))
      }
    ]
  }

  const generateCombinedInsight = () => {
    // CONTEXT-AWARE INSIGHTS: Match decision fusion logic
    const action = data.action?.toUpperCase()
    const bearishPatterns = data.bearish_patterns || []
    const bullishPatterns = data.bullish_patterns || []
    const bullishSignals = data.signals_triggered || []
    const sentiment = data.news_sentiment?.sentiment_label?.toLowerCase() || ''
    const priceSpike = data.event_signals?.price_spike
    const hasNegativeMove = priceSpike?.direction === 'downward'
    
    // SELL SIGNALS: Bearish patterns
    if (action === 'SELL') {
      if (bearishPatterns.includes('Death Cross')) {
        const context = hasNegativeMove ? 'Recent price weakness confirms' : 'Signals'
        return `Bearish setup: Death Cross indicates trend reversal. ${context} downtrend risk.`
      }
      if (bearishPatterns.length > 0) {
        return `Trend weakness: ${bearishPatterns.join(', ')} pattern(s) detected - caution advised.`
      }
      return 'Bearish pressure detected across technical and sentiment factors.'
    }
    
    // BUY SIGNALS: Bullish patterns + confirmation
    if (action === 'BUY') {
      if (bullishPatterns.length > 0 && sentiment === 'positive') {
        return `Strong bullish setup: ${bullishPatterns.slice(0, 2).join(' + ')} confirmed with positive sentiment.`
      }
      if (bullishPatterns.length > 0) {
        return `Bullish patterns detected: ${bullishPatterns.join(', ')} suggest upside potential.`
      }
      if (sentiment === 'positive') {
        return 'Positive sentiment with technical support provides opportunity.'
      }
    }
    
    // HOLD SIGNALS: Mixed or uncertain
    if (action === 'HOLD') {
      if (bearishPatterns.length > 0 && bullishPatterns.length > 0) {
        return 'Mixed signals: Bearish and bullish patterns in conflict - wait for clearer direction.'
      }
      if (bullishSignals.length === 0 && bearishPatterns.length === 0) {
        return 'No clear signals. Monitor for trend formation before entering position.'
      }
      return 'Balanced risk-reward. Insufficient conviction for directional trade.'
    }
    
    return 'Analyzing market factors...'
  }

  const triggeredCount = data.signals_triggered?.length || 0
  const detailedCount = data.signal_details?.length || 0

  return (
    <div className="dashboard-container">
      {/* Demo Mode Indicator */}
      {data.isDemo && (
        <div className="demo-indicator">
          <span className="material-symbols-outlined demo-indicator-icon">visibility</span>
          <span className="demo-indicator-text">Demo Mode Active</span>
        </div>
      )}

      {/* ==================== HERO SECTION ==================== */}
      {/* Trading Recommendation + AI Insight + Key Metrics */}
      <div className="dashboard-hero-section">
        {/* Primary Decision: Trading Recommendation */}
        <div className="hero-main">
          <div className={`trading-rec-action action-${data.action.toLowerCase()}`}>
            <span className="action-text">{data.action}</span>
          </div>
          <div className="hero-meta">
            <div className="hero-item">
              <span className="hero-label">Recommendation</span>
              <p className="hero-description">{data.summary}</p>
            </div>
          </div>
        </div>

        {/* Secondary Metrics: Confidence + Opportunity */}
        <div className="hero-metrics">
          <div className="hero-metric-card">
            <span className="metric-label">Confidence</span>
            <div className="metric-value confidence-large">{data.confidence}%</div>
            <div className="metric-bar">
              <div className="metric-bar-fill" style={{ width: `${data.confidence}%` }}></div>
            </div>
          </div>

          <div className="hero-metric-card">
            <span className="metric-label">Opportunity</span>
            <div className="metric-value" style={{ color: getOpportunityColor(data.opportunity_level) }}>
              {data.opportunity_level} {data.action === 'SELL' ? '(Bearish)' : data.action === 'BUY' ? '(Bullish)' : ''}
            </div>
          </div>

          <div className="hero-metric-card">
            <span className="metric-label">Data Points</span>
            <div className="metric-value">{data.data_points}</div>
          </div>
        </div>

        {/* AI Insight Banner */}
        <div className="hero-insight">
          <span className="insight-icon material-symbols-outlined">lightbulb</span>
          <div className="insight-content">
            <span className="insight-header">AI Insight</span>
            <span className="insight-text">{generateCombinedInsight()}</span>
          </div>
        </div>
      </div>

      {/* ==================== ROW 1: CHART + RADAR/METRICS ==================== */}
      <div className="dashboard-row-main">
        {/* LEFT: Stock Chart (Large) */}
        <div className="main-chart-panel">
          <StockChart 
            stock={data.stock} 
            confidence={data.confidence}
            opportunityLevel={data.opportunity_level}
          />
        </div>

        {/* RIGHT: Opportunity Radar + Key Metrics Pills */}
        <div className="radar-metrics-panel">
          {/* Radar */}
          <div className="radar-box">
            <OpportunityRadar data={getRadarData(data)} />
          </div>

          {/* Quick Metrics (Tech/Sentiment/Trend/Risk) */}
          <div className="key-metrics-grid">
            <div className="metric-pill">
              <span className="pill-label">Technical</span>
              <span className="pill-icon material-symbols-outlined">analytics</span>
            </div>
            <div className="metric-pill">
              <span className="pill-label">Sentiment</span>
              <span className="pill-icon material-symbols-outlined">thumbs_up</span>
            </div>
            <div className="metric-pill">
              <span className="pill-label">Trend</span>
              <span className="pill-icon material-symbols-outlined">trending_up</span>
            </div>
            <div className="metric-pill">
              <span className="pill-label">Risk</span>
              <span className="pill-icon material-symbols-outlined">warning</span>
            </div>
          </div>
        </div>
      </div>

      {/* ==================== HEADLINES (Top News Context) ==================== */}
      {data.news_sentiment?.top_headlines && data.news_sentiment.top_headlines.length > 0 && (
        <div className="dashboard-headlines-section">
          <div className="section-header">
            <h3 className="section-title">
              <span className="material-symbols-outlined">newspaper</span>
              Top Headlines for {data.stock}
            </h3>
            <span className="headline-count">{data.news_sentiment.articles_analyzed} articles analyzed</span>
          </div>
          {data.news_sentiment.summary && (
            <p className="headline-subtitle">{data.news_sentiment.summary}</p>
          )}
          <div className="headlines-list">
            {data.news_sentiment.top_headlines.slice(0, 5).map((headline, idx) => (
              <div key={idx} className="headline-item">
                <span className="headline-number">{idx + 1}</span>
                <p className="headline-text">{headline}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ==================== ROW 2: SIGNAL DETAILS + SENTIMENT/EVENTS ==================== */}
      <div className="dashboard-row-analysis">
        {/* LEFT: Signal Details (Technical Analysis) */}
        {data.signal_details && data.signal_details.length > 0 && (
          <div className="signals-detail-panel">
            <div className="section-header">
              <h3 className="section-title">
                <span className="material-symbols-outlined">analytics</span>
                Signal Details
              </h3>
              <span className="signal-count">{triggeredCount} Triggered</span>
            </div>
            
            <div className="signal-details-list">
              {data.signal_details.map((signal, idx) => (
                <div key={idx} className={`signal-detail-item ${signal.triggered ? 'signal-triggered' : 'signal-not-triggered'}`}>
                  <div className="signal-detail-header">
                    <div className="signal-detail-indicator">
                      {signal.triggered ? (
                        <FaCheckCircle style={{ color: 'var(--secondary)', fontSize: '14px' }} />
                      ) : (
                        <FaCircle style={{ color: 'var(--outline)', fontSize: '14px' }} />
                      )}
                    </div>
                    <div className="signal-detail-title-group">
                      <span className="signal-detail-name">{signal.name}</span>
                      {signal.strength !== '-' && (
                        <span className={`signal-detail-strength strength-${signal.strength.toLowerCase()}`}>
                          {signal.strength}
                        </span>
                      )}
                    </div>
                  </div>
                  <p className="signal-detail-reasoning">{signal.reasoning}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* RIGHT: News Sentiment + Event Signals (Stacked) */}
        <div className="sentiment-events-panel">
          {/* News Sentiment */}
          <div className="news-sentiment-box">
            <div className="section-header">
              <h3 className="section-title">
                <span className="material-symbols-outlined">newspaper</span>
                News Sentiment
              </h3>
            </div>
            <div className="sentiment-display-large">
              <span className={`sentiment-value sentiment-${data.news_sentiment?.sentiment_label?.toLowerCase() || 'neutral'}`}>
                {data.news_sentiment?.sentiment_label || 'Neutral'}
              </span>
              <div className="sentiment-gauge-large">
                <div className="sentiment-score-info">
                  <span className="sentiment-score-value">
                    {data.news_sentiment?.sentiment_score !== undefined ? data.news_sentiment.sentiment_score.toFixed(2) : '0.00'}
                  </span>
                  <span className="sentiment-score-scale">
                    / Scale: -1 to 1
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Market Events */}
          <div className="events-box">
            <div className="section-header">
              <h3 className="section-title">
                <span className="material-symbols-outlined">campaign</span>
                Market Events
              </h3>
            </div>
            
            {/* Price Spike Event */}
            {data.event_signals?.price_spike && (
              <div className={`event-item ${data.event_signals.price_spike.detected ? 'event-triggered' : 'event-not-triggered'}`}>
                <div className="event-header">
                  <div className="event-name-group">
                    {data.event_signals.price_spike.detected ? (
                      <FaBolt style={{ color: 'var(--primary)', fontSize: '14px' }} />
                    ) : (
                      <FaCircle style={{ color: 'var(--outline)', fontSize: '14px' }} />
                    )}
                    <span className="event-name">
                    Price Spike {data.event_signals.price_spike.direction === 'downward' ? '(Bearish)' : '(Bullish)'}
                  </span>
                  </div>
                  <span className="event-change" style={{ 
                    color: data.event_signals.price_spike.direction === 'upward' ? 'var(--secondary)' : 'var(--tertiary-container)'
                  }}>
                    {data.event_signals.price_spike.direction === 'upward' ? '↑' : '↓'} {data.event_signals.price_spike.change_percent?.toFixed(1)}%
                  </span>
                </div>
                <p className="event-description">{data.event_signals.price_spike.description}</p>
              </div>
            )}

            {/* Volume Surge Event */}
            {data.event_signals?.volume_surge && (
              <div className={`event-item ${data.event_signals.volume_surge.detected ? 'event-triggered' : 'event-not-triggered'}`}>
                <div className="event-header">
                  <div className="event-name-group">
                    {data.event_signals.volume_surge.detected ? (
                      <FaBolt style={{ color: 'var(--primary)', fontSize: '14px' }} />
                    ) : (
                      <FaCircle style={{ color: 'var(--outline)', fontSize: '14px' }} />
                    )}
                    <span className="event-name">Volume Surge</span>
                  </div>
                  <span className="event-change">Ratio: {data.event_signals.volume_surge.ratio?.toFixed(2)}x</span>
                </div>
                <p className="event-description">{data.event_signals.volume_surge.description}</p>
                {data.event_signals.volume_surge.detected && (
                  <div className="volume-details-inline">
                    <span className="volume-detail">Current: {(data.event_signals.volume_surge.current_volume / 1000000).toFixed(1)}M</span>
                    <span className="volume-detail">Average: {(data.event_signals.volume_surge.average_volume / 1000000).toFixed(1)}M</span>
                  </div>
                )}
              </div>
            )}

            {(!data.event_signals?.price_spike && !data.event_signals?.volume_surge) && (
              <p className="no-data">No major events detected</p>
            )}
          </div>
        </div>
      </div>

      {/* ==================== ROW 3: CHART PATTERNS + SUCCESS RATES (MERGED) ==================== */}
      <div className="dashboard-patterns-section">
        <div className="patterns-and-success">
          {/* Patterns Info */}
          {data.chart_patterns && (
            <div className="patterns-box">
              {data.chart_patterns && <ChartPatterns patterns={data.chart_patterns} />}
            </div>
          )}

          {/* Success Rates */}
          {data.chart_patterns?.success_rates && (
            <div className="success-rates-box">
              <div className="section-header">
                <h3 className="section-title">
                  <span className="material-symbols-outlined">trending_up</span>
                  Pattern Success Rates (Backtested)
                </h3>
              </div>
              
              <div className="success-rates-grid">
                <div className="success-rate-item">
                  <span className="rate-label">Breakout</span>
                  <span className="rate-value">{data.chart_patterns.success_rates.breakout?.toFixed(1) || '0'}%</span>
                  <div className="rate-progress">
                    <div className="rate-progress-fill" style={{ width: `${data.chart_patterns.success_rates.breakout || 0}%` }}></div>
                  </div>
                </div>
                <div className="success-rate-item">
                  <span className="rate-label">Support</span>
                  <span className="rate-value">{data.chart_patterns.success_rates.support?.toFixed(1) || '0'}%</span>
                  <div className="rate-progress">
                    <div className="rate-progress-fill" style={{ width: `${data.chart_patterns.success_rates.support || 0}%` }}></div>
                  </div>
                </div>
                <div className="success-rate-item">
                  <span className="rate-label">MA Cross</span>
                  <span className="rate-value">{data.chart_patterns.success_rates.ma_crossover?.toFixed(1) || '0'}%</span>
                  <div className="rate-progress">
                    <div className="rate-progress-fill" style={{ width: `${data.chart_patterns.success_rates.ma_crossover || 0}%` }}></div>
                  </div>
                </div>
                <div className="success-rate-item overall">
                  <span className="rate-label">Overall Success</span>
                  <span className="rate-value">{data.chart_patterns.success_rates.overall?.toFixed(1) || '0'}%</span>
                  <div className="rate-progress">
                    <div className="rate-progress-fill" style={{ width: `${data.chart_patterns.success_rates.overall || 0}%` }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ==================== FINAL SECTION: TRADE INSIGHT (ONLY ONCE, HIGHLIGHTED) ==================== */}
      {data.chart_patterns && (
        <div className="dashboard-trade-insight-final">
          <TradeInsightPanel 
            analysisData={data}
            explanationBlock={data.explanation_block}
            scoreBreakdown={data.score_breakdown}
          />
        </div>
      )}

      {/* ==================== LAST ROW: WATCHLIST ==================== */}
      <div className="dashboard-watchlist-section">
        <Watchlist />
      </div>
    </div>
  )
}

export default Dashboard
