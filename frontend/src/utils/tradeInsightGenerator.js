/**
 * Trade Insight Generator
 * Generates dynamic, explainable insights based on detected patterns
 */

export function generateTradeInsight(patterns) {
  if (!patterns || !patterns.patterns_detected) {
    return {
      insight_points: ['Insufficient data available'],
      interpretation: 'Waiting for pattern detection',
      suggested_action: 'Insufficient data to make a decision'
    }
  }

  const insightPoints = []
  
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

  // Insert pattern detection insights with actual pattern data
  if (hasBreakout && hasSupport) {
    const breakoutMargin = breakout?.breakout_margin
    const supportDistance = support?.distance_from_support
    insightPoints.push(
      breakoutMargin 
        ? `Breakout + support bounce = strong bullish confirmation (${breakoutMargin.toFixed(2)}% above resistance)`
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

  if (hasGoldenCross) {
    insightPoints.push('Golden Cross: bullish trend crossover detected')
  } else if (hasDeathCross) {
    insightPoints.push('Death Cross warning: bearish trend reversal signaled')
  }

  // Success rate interpretation - Use overall rate for final reliability assessment
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

  // Generate interpretation based on actual data
  let interpretation = ''
  if (hasBreakout && hasSupport) {
    const breakoutRate = successRates.breakout || 0
    const supportRate = successRates.support || 0
    interpretation = `Dual pattern confirmation: Breakout (${Math.round(breakoutRate)}% success rate) + Support (${Math.round(supportRate)}% success rate)`
  } else if (hasBreakout && hasGoldenCross) {
    interpretation = 'Bullish momentum: Technical breakout confirmed by bullish trend crossover'
  } else if (hasDeathCross) {
    interpretation = `Bearish trend alert: Death Cross signals potential reversal (${Math.round(successRates.ma_crossover || 0)}% historical signal reliability)`
  } else if (hasBreakout) {
    const breakoutRate = successRates.breakout || 0
    interpretation = `Breakout setup forming (${Math.round(breakoutRate)}% historical success) - awaiting confirmation`
  } else if (hasSupport) {
    interpretation = 'Price holding at support - stabilization phase with upside potential'
  } else {
    interpretation = 'No strong technical setup currently detected - monitor for developments'
  }

  // Generate suggested action based on patterns and success rates
  let suggestedAction = ''
  const hasHighSuccess = overallSuccessRate > 60
  const hasModerateSuccess = overallSuccessRate >= 40
  
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

  return {
    insight_points: truncatedPoints,
    interpretation,
    suggested_action: suggestedAction,
    avgSuccessRate: overallSuccessRate > 0 ? overallSuccessRate : null
  }
}
