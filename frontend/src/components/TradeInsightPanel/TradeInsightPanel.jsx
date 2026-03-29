import React from 'react'
import { FaLightbulb, FaChartLine } from 'react-icons/fa'
import { generateTradeInsight } from '../../utils/tradeInsightGenerator'
import './TradeInsightPanel.css'

/**
 * TradeInsightPanel Component
 * Displays dynamic trade insights based on detected patterns
 */
function TradeInsightPanel({ patterns }) {
  if (!patterns) {
    return null
  }

  const insight = generateTradeInsight(patterns)

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
    </div>
  )
}

export default TradeInsightPanel
