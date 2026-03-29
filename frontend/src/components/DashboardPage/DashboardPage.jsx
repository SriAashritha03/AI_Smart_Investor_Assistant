import React from 'react'
import StockSelector from '../StockSelector/StockSelector'
import Dashboard from '../Dashboard/Dashboard'
import { analyzeStock } from '../../services/stockApi'
import { getDemoResponse } from '../../constants/mockData'

/**
 * Helper function to add missing decision fusion fields to mock/old API responses
 */
function enrichAnalysisData(result) {
  const enriched = { ...result }
  
  // Add missing decision fusion fields with sensible defaults
  if (!enriched.signal_summary) {
    const signals = enriched.signals_triggered || []
    const bearishPatterns = enriched.bearish_patterns || []
    const bullishPatterns = enriched.bullish_patterns || []
    
    if (signals.length > 0) {
      enriched.signal_summary = `${signals.length} signal(s) detected: ${signals.join(', ')}`
    } else if (bearishPatterns.length > 0 || bullishPatterns.length > 0) {
      // More intelligent: mention bearish/bullish patterns
      const bearishMsg = bearishPatterns.length > 0 ? `Bearish pattern present (${bearishPatterns.join(', ')})` : ''
      const bullishMsg = bullishPatterns.length > 0 ? `Bullish pattern present (${bullishPatterns.join(', ')})` : ''
      
      if (bearishPatterns.length > 0) {
        enriched.signal_summary = `No bullish signals detected. ${bearishMsg}`
      } else {
        enriched.signal_summary = bullishMsg
      }
    } else {
      enriched.signal_summary = 'No clear trading signals detected'
    }
  }
  
  if (!enriched.explanation_block) {
    // Generate intelligent explanation from actual data
    const action = enriched.action?.toUpperCase() || 'HOLD'
    const bearishPatterns = enriched.bearish_patterns || []
    const bullishPatterns = enriched.bullish_patterns || []
    const priceSpike = enriched.event_signals?.price_spike
    const hasNegativePriceMove = priceSpike?.direction === 'downward'
    
    const explanationLines = []
    
    // First line: Decision with confidence + reason
    if (bearishPatterns.includes('Death Cross')) {
      explanationLines.push(`Death Cross detected - strong bearish signal (${enriched.confidence}% confidence)`)
    } else if (action === 'SELL' && bearishPatterns.length > 0) {
      explanationLines.push(`${bearishPatterns.join(', ')} present - bearish setup (${enriched.confidence}% confidence)`)
    } else if (action === 'BUY' && bullishPatterns.length > 0) {
      explanationLines.push(`${bullishPatterns.join(', ')} confirmed - bullish setup (${enriched.confidence}% confidence)`)
    } else {
      explanationLines.push(`Action: ${action} with ${enriched.confidence}% confidence`)
    }
    
    // Second line: Signal alignment or lack thereof
    if (action === 'SELL' && enriched.signals_triggered?.length === 0) {
      explanationLines.push('No bullish signals triggered - weakness bias confirmed')
    } else if (action === 'BUY' && enriched.signals_triggered?.length > 0) {
      explanationLines.push(`${enriched.signals_triggered?.length} bullish signal(s) confirmed`)
    } else if (action === 'HOLD') {
      explanationLines.push('Mixed signals - insufficient conviction for strong direction')
    }
    
    // Third line: Event context (price move, sentiment, etc)
    if (hasNegativePriceMove) {
      const movePct = Math.abs(priceSpike.change_percent).toFixed(1)
      explanationLines.push(`Recent price drop (-${movePct}%) supports bearish outlook`)
    } else if (enriched.news_sentiment?.sentiment_label === 'Positive' && action === 'BUY') {
      explanationLines.push('Positive sentiment aligns with bullish setup')
    }
    
    enriched.explanation_block = explanationLines.slice(0, 3) // Max 3 lines
  }
  
  // IMPORTANT: Only generate score_breakdown if backend didn't provide it
  // Backend _generate_score_breakdown uses authoritative formulas
  if (!enriched.score_breakdown) {
    // Fallback: Use backend formula (same as decision_fusion.py)
    // Technical: (signal_count * 15) + (detected_patterns * 20) + (confidence * 0.5)
    const signalCount = enriched.signals_triggered?.length || 0
    const detectedPatterns = enriched.chart_patterns?.patterns_detected?.filter(p => p.detected).length || 0
    const technicalScore = Math.min(100, (signalCount * 15) + (detectedPatterns * 20) + (enriched.confidence * 0.5))
    
    // Sentiment: ((sentiment_score + 1) / 2 * 100) * (sentiment_confidence / 100)
    const sentimentRaw = enriched.news_sentiment?.sentiment_score || 0
    const sentimentConfidence = enriched.news_sentiment?.confidence || 50
    const sentimentScore = Math.max(0, Math.min(100, ((sentimentRaw + 1) / 2 * 100) * (sentimentConfidence / 100)))
    
    // Events: len(events) * 40 + 10
    const eventsCount = enriched.event_signals?.events_detected?.length || 0
    let eventsScore = Math.min(100, eventsCount * 40 + 10)
    if (enriched.event_signals?.price_spike?.detected) eventsScore = Math.min(100, eventsScore + 15)
    if (enriched.event_signals?.volume_surge?.detected) eventsScore = Math.min(100, eventsScore + 15)
    
    enriched.score_breakdown = {
      technical: technicalScore,
      sentiment: sentimentScore,
      events: eventsScore
    }
  }
  
  if (!enriched.bearish_patterns) {
    enriched.bearish_patterns = []
  }
  
  if (!enriched.bullish_patterns) {
    enriched.bullish_patterns = enriched.signals_triggered || []
  }
  
  return enriched
}

function DashboardPage({ demoMode }) {
  const [selectedStock, setSelectedStock] = React.useState('AAPL')
  const [analysisData, setAnalysisData] = React.useState(null)
  const [isLoading, setIsLoading] = React.useState(false)
  const [error, setError] = React.useState(null)
  const [isBackendReady, setIsBackendReady] = React.useState(true)

  // DEBUG: Log analysis data changes
  React.useEffect(() => {
    if (analysisData) {
      console.log('[DashboardPage] analysisData updated:', {
        stock: analysisData.stock,
        has_signal_summary: !!analysisData.signal_summary,
        has_explanation_block: !!analysisData.explanation_block,
        explanation_block_length: analysisData.explanation_block?.length,
        has_score_breakdown: !!analysisData.score_breakdown,
        score_breakdown_keys: Object.keys(analysisData.score_breakdown || {}),
      })
    }
  }, [analysisData])

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
      
      // Enrich result with missing decision fusion fields
      result = enrichAnalysisData(result)
      
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
          // ENRICHED: These come from enrichAnalysisData() function
          signal_summary: result.signal_summary,
          explanation_block: result.explanation_block,
          score_breakdown: result.score_breakdown,
          bearish_patterns: result.bearish_patterns,
          bullish_patterns: result.bullish_patterns,
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
