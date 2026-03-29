import React from 'react'
import { FaLightbulb, FaChartLine } from 'react-icons/fa'
import { generateTradeInsight } from '../../utils/tradeInsightGenerator'
import './TradeInsightPanel.css'

/**
 * TradeInsightPanel Component
 * Displays dynamic trade insights based on detected patterns and unified decision logic
 * 
 * Props:
 * - patterns: chart_patterns from API (for backwards compatibility)
 * - analysisData: full analysis object from API (preferred, includes decision logic)
 * - explanationBlock: pre-computed explanation array from backend (new)
 * - scoreBreakdown: pre-computed scores from backend (new)
 */
function TradeInsightPanel({ patterns, analysisData, explanationBlock, scoreBreakdown }) {
  // Support both old (patterns-only) and new (full analysis data) props
  const data = analysisData || patterns
  
  if (!data) {
    return null
  }

  const insight = generateTradeInsight(data)
  
  // DEBUG: Log received data to help troubleshoot missing fields
  React.useEffect(() => {
    if (analysisData) {
      console.log('[TradeInsightPanel] Received analysisData:', {
        has_explanation_block: !!analysisData.explanation_block,
        explanation_block_length: analysisData.explanation_block?.length,
        explanation_block: analysisData.explanation_block,
        has_score_breakdown: !!analysisData.score_breakdown,
        score_breakdown: analysisData.score_breakdown,
        has_signal_summary: !!analysisData.signal_summary,
        signal_summary: analysisData.signal_summary?.substring?.(0, 50),
      })
    }
  }, [analysisData])

  // Get explanation data - prioritize prop, then analysisData, then generate from insight
  const finalExplanationBlock = explanationBlock || analysisData?.explanation_block
  const hasExplanationData = finalExplanationBlock && Array.isArray(finalExplanationBlock) && finalExplanationBlock.length > 0

  // Get score data - prioritize prop, then analysisData, then generate from insight
  const finalScoreBreakdown = scoreBreakdown || analysisData?.score_breakdown
  const hasScoreData = finalScoreBreakdown && typeof finalScoreBreakdown === 'object' && Object.keys(finalScoreBreakdown).length > 0

  return (
    <div className="trade-insight-panel">
      <div className="insight-header">
        <h3 className="insight-title">
          <FaLightbulb style={{ marginRight: '10px' }} />
          Trade Insight
        </h3>
        {insight.avgSuccessRate && (
          <span className="reliability-badge">
            {insight.avgSuccessRate}% Success
          </span>
        )}
      </div>

      {/* Insight Points */}
      <div className="insight-section">
        <h4 className="insight-subtitle">Pattern Analysis</h4>
        <ul className="insight-points">
          {insight.insight_points.map((point, idx) => (
            <li key={idx} className="insight-point">
              <span className="point-bullet">◆</span>
              <span className="point-text">{point}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Interpretation */}
      <div className="insight-section">
        <h4 className="insight-subtitle">Interpretation</h4>
        <p className="interpretation-text">{insight.interpretation}</p>
      </div>

      {/* Suggested Action */}
      <div className="insight-section action-section">
        <h4 className="insight-subtitle">
          <FaChartLine style={{ marginRight: '6px' }} />
          Suggested Action
        </h4>
        <p className="action-text">{insight.suggested_action}</p>
      </div>

      {/* NEW: Explanation Block - Why this decision */}
      {hasExplanationData && (
        <div className="insight-section explanation-section">
          <h4 className="insight-subtitle">💡 Why this decision</h4>
          <ul className="explanation-list">
            {finalExplanationBlock.map((reason, idx) => (
              <li key={idx} className="explanation-item">
                {reason}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* NEW: Score Breakdown */}
      {hasScoreData && (
        <div className="insight-section score-section">
          <h4 className="insight-subtitle">📊 Score Breakdown</h4>
          <div className="score-grid">
            {Object.entries(finalScoreBreakdown).map(([key, value]) => {
              const numValue = typeof value === 'number' ? value : 0
              const safeValue = Math.min(100, Math.max(0, numValue))
              
              return (
                <div key={key} className="score-item">
                  <span className="score-label">
                    {key.charAt(0).toUpperCase() + key.slice(1)}
                  </span>
                  <div className="score-bar">
                    <div 
                      className={`score-bar-fill score-${key}`}
                      style={{ width: `${safeValue}%` }}
                    ></div>
                  </div>
                  <span className="score-value">{Math.round(safeValue)}</span>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}

export default TradeInsightPanel
