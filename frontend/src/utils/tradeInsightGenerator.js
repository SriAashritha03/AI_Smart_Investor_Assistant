/**
 * Trade Insight Generator
 * Generates dynamic, explainable insights based on unified decision logic
 * 
 * IMPROVED: Now uses score_breakdown, bearish_patterns, and decision reasoning
 * from the backend decision fusion engine instead of just pattern detection
 */

export function generateTradeInsight(analysisData) {
  // Support both direct patterns object and full analysis data
  const patterns = analysisData?.chart_patterns || analysisData
  const fullData = analysisData?.action ? analysisData : null
  
  if (!patterns) {
    return {
      insight_points: ['Insufficient data available'],
      interpretation: 'Waiting for pattern detection',
      suggested_action: 'Insufficient data to make a decision'
    }
  }

  const insightPoints = []
  
  // Extract decision data from full analysis if available
  const action = fullData?.action
  const confidence = fullData?.confidence || 50
  const scoreBreakdown = fullData?.score_breakdown || {}
  const bearishPatterns = fullData?.bearish_patterns || []
  const bullishPatterns = fullData?.bullish_patterns || []
  const sentimentLabel = fullData?.news_sentiment?.sentiment_label || 'Neutral'
  const signalSummary = fullData?.signal_summary || ''
  
  // Find patterns by name instead of index
  const breakout = patterns.patterns_detected?.find(p => p.pattern_name === 'Breakout') || {}
  const support = patterns.patterns_detected?.find(p => p.pattern_name === 'Support') || {}
  const maCrossover = patterns.patterns_detected?.find(p => p.pattern_name === 'MA Crossover') || {}
  const successRates = patterns.success_rates || {}

  // Pattern combination logic - use actual detected property from API
  const hasBreakout = breakout?.detected === true
  const hasSupport = support?.detected === true
  const hasGoldenCross = maCrossover?.detected === true && maCrossover?.crossover_type === 'Golden Cross'
  const hasDeathCross = maCrossover?.detected === true && maCrossover?.crossover_type === 'Death Cross'

  // ===== INSIGHT 1: Use unified decision if available =====
  if (fullData) {
    // Death Cross is highest priority
    if (hasDeathCross || bearishPatterns?.includes('Death Cross')) {
      insightPoints.push('⚠️ Death Cross: Bearish trend reversal detected - strong sell signal')
    }
    // Strong bullish setup
    else if ((hasBreakout && hasSupport) || bullishPatterns?.length >= 2) {
      insightPoints.push('✅ Strong bullish setup: Multiple confirmations align for upside')
    }
    // Mixed signals
    else if (bearishPatterns?.length > 0 && bullishPatterns?.length > 0) {
      insightPoints.push(`⚖️ Mixed signals: ${bullishPatterns.length} bullish vs ${bearishPatterns.length} bearish patterns`)
    }
  }
  
  // ===== INSIGHT 2: Use signal summary from decision fusion =====
  if (signalSummary) {
    insightPoints.push(`Signal status: ${signalSummary}`)
  } else {
    // Fallback to pattern-based insights
    if (hasBreakout && hasSupport) {
      const breakoutMargin = breakout?.breakout_margin
      const supportDistance = support?.distance_from_support
      insightPoints.push(
        breakoutMargin 
          ? `Breakout + support bounce = strong confirmation (${breakoutMargin.toFixed(2)}% above resistance)`
          : 'Breakout + support bounce = strong bullish confirmation'
      )
    } else if (hasBreakout) {
      const breakoutMargin = breakout?.breakout_margin
      const volumeConfirm = breakout?.volume_confirmation ? ' with volume confirmation' : ''
      insightPoints.push(
        `Breakout detected${volumeConfirm}${breakoutMargin ? ` (${breakoutMargin.toFixed(2)}% above resistance)` : ''}`
      )
    } else if (hasSupport) {
      const distanceFromSupport = support?.distance_from_support
      insightPoints.push(
        `Support level holding${distanceFromSupport ? ` (${distanceFromSupport.toFixed(2)}% above support)` : ''}, potential reversal setup`
      )
    }
  }

  // ===== INSIGHT 3: Use score breakdown if available =====
  if (scoreBreakdown?.technical !== undefined) {
    const tech = scoreBreakdown.technical
    const sent = scoreBreakdown.sentiment
    const events = scoreBreakdown.events
    
    const maxScore = Math.max(tech, sent, events)
    if (maxScore > 70) {
      if (tech > 65) insightPoints.push(`Strong technical setup (${tech.toFixed(0)}/100)`)
      if (sent > 65) insightPoints.push(`Positive sentiment alignment (${sent.toFixed(0)}/100)`)
      if (events > 65) insightPoints.push(`Strong event signals detected (${events.toFixed(0)}/100)`)
    }
  }

  // ===== INSIGHT 4: MA Crossover patterns =====
  if (hasGoldenCross) {
    insightPoints.push('Golden Cross: bullish trend crossover detected')
  } else if (hasDeathCross && insightPoints.length === 1) {
    // Already added above if Death Cross
    insightPoints.push('Trend reversal signaled - exercise caution')
  }

  // ===== INSIGHT 5: Success rate interpretation =====
  const overallSuccessRate = successRates.overall || 0
  if (overallSuccessRate >= 60) {
    insightPoints.push(`High reliability: ${Math.round(overallSuccessRate)}% historical success`)
  } else if (overallSuccessRate >= 40) {
    insightPoints.push(`Moderate reliability: ${Math.round(overallSuccessRate)}% historical success`)
  } else if (overallSuccessRate > 0) {
    insightPoints.push(`⚠ Low reliability: ${Math.round(overallSuccessRate)}% historical success`)
  }

  // Limit to 5 lines
  const truncatedPoints = insightPoints.slice(0, 5)

  // ===== INTERPRETATION: Use unified decision data =====
  let interpretation = ''
  
  if (fullData && action) {
    // Use decision-based interpretation
    if (action === 'SELL' && (hasDeathCross || bearishPatterns?.includes('Death Cross'))) {
      interpretation = `Bearish signal detected due to Death Cross, despite lack of strong bullish indicators. Confidence: ${confidence}%`
    } 
    else if (action === 'BUY' && ((hasBreakout && hasSupport) || bullishPatterns?.length >= 2)) {
      const breakoutRate = successRates.breakout || 0
      const supportRate = successRates.support || 0
      interpretation = `Dual pattern confirmation: Breakout (${Math.round(breakoutRate)}% success) + Support (${Math.round(supportRate)}% success). Market aligns for upside.`
    } 
    else if (action === 'HOLD' && (bearishPatterns?.length > 0 || sentimentLabel === 'Negative')) {
      interpretation = `Mixed signals prevent strong conviction. Bearish factors present - monitor for reversal confirmation before entry.`
    }
    else if (hasGoldenCross && action === 'BUY') {
      interpretation = 'Bullish momentum: Technical breakout confirmed by bullish trend crossover'
    }
  }
  
  // Fallback interpretations if no unified data
  if (!interpretation) {
    if (hasDeathCross) {
      interpretation = `Bearish trend alert: Death Cross signals potential reversal (${Math.round(successRates.ma_crossover || 0)}% historical signal reliability)`
    } else if (hasBreakout && hasGoldenCross) {
      interpretation = 'Bullish momentum: Technical breakout confirmed by bullish trend crossover'
    } else if (hasBreakout) {
      const breakoutRate = successRates.breakout || 0
      interpretation = `Breakout setup forming (${Math.round(breakoutRate)}% historical success) - awaiting confirmation`
    } else if (hasSupport) {
      interpretation = 'Price holding at support - stabilization phase with upside potential'
    } else {
      interpretation = 'No strong technical setup currently detected - monitor for developments'
    }
  }

  // ===== SUGGESTED ACTION: Use decision data =====
  let suggestedAction = ''
  const hasHighSuccess = overallSuccessRate > 60
  const hasModerateSuccess = overallSuccessRate >= 40
  
  if (fullData && action) {
    // Use decision-based actions
    if (action === 'BUY') {
      if (hasBreakout && hasSupport && hasHighSuccess) {
        const supportLevel = support?.support_level
        suggestedAction = supportLevel 
          ? `Strong setup confirmed: Consider entry on pullback near support (${supportLevel.toFixed(2)})`
          : 'Strong setup confirmed: Consider scaling into position'
      } else {
        suggestedAction = 'Bullish alignment: Build position on any weakness'
      }
    }
    else if (action === 'SELL') {
      suggestedAction = 'Bearish signal confirmed: Consider reducing exposure or establishing short positions'
    }
    else if (action === 'HOLD') {
      if (confidence >= 60) {
        suggestedAction = 'Current setup mixed - await clearer directional confirmation'
      } else {
        suggestedAction = 'Insufficient signals: Continue monitoring for setup clarity'
      }
    }
  }
  
  // Fallback actions if no unified decision
  if (!suggestedAction) {
    if (hasBreakout && hasSupport && hasHighSuccess) {
      const supportLevel = support?.support_level
      suggestedAction = supportLevel 
        ? `Strong setup: Consider entry on pullback near support level (${supportLevel.toFixed(2)})`
        : 'Strong setup: Consider entry on minor pullback confirmation'
    } else if (hasBreakout && hasSupport && hasModerateSuccess) {
      suggestedAction = 'Dual confirmation present: Build position on breakout pullback'
    } else if (hasBreakout && overallSuccessRate > 50) {
      const resistanceLevel = breakout?.resistance_level
      suggestedAction = resistanceLevel
        ? `Monitor above resistance (${resistanceLevel.toFixed(2)}) for trend confirmation`
        : 'Monitor for continuation above breakout level'
    } else if (hasGoldenCross && overallSuccessRate > 50) {
      suggestedAction = 'Bullish crossover confirmed: Consider accumulation on weakness'
    } else if (hasDeathCross) {
      suggestedAction = 'Bearish signal: Consider reducing exposure or awaiting reversal signals'
    } else if (hasSupport && overallSuccessRate > 40) {
      const supportLevel = support?.support_level
      suggestedAction = supportLevel
        ? `Monitor support (${supportLevel.toFixed(2)}); watch for breakout confirmation`
        : 'Monitor support level; watch for breakout attempt'
    } else {
      suggestedAction = 'Insufficient signals: Wait for clearer technical setup before entry'
    }
  }

  return {
    insight_points: truncatedPoints,
    interpretation,
    suggested_action: suggestedAction,
    avgSuccessRate: overallSuccessRate > 0 ? overallSuccessRate : null,
    // NEW: Include score breakdown if available
    scoreBreakdown: scoreBreakdown,
    // NEW: Include decision info if available
    decision: action ? { action, confidence } : null
  }
}
