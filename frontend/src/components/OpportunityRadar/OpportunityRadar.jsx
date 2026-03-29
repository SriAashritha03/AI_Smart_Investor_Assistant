import React from 'react'
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts'
import './OpportunityRadar.css'

/**
 * OpportunityRadar Component
 * Visualizes 5 key investment metrics in a radar/spider chart
 * 
 * @param {Array} data - Array of objects with { subject, value (0-100) }
 * @param {Object} config - Optional configuration object
 */
function OpportunityRadar({ data, config = {} }) {
  // Default configuration
  const defaultConfig = {
    height: 180,
    margin: { top: 15, right: 25, bottom: 15, left: 25 },
    radarStroke: '#3b82f6',
    radarFill: 'rgba(59, 130, 246, 0.15)',
    gridStroke: 'rgba(107, 114, 128, 0.2)',
  }

  const settings = { ...defaultConfig, ...config }

  // Default sample data if none provided
  const defaultData = [
    { subject: 'Technical', value: 70 },
    { subject: 'Sentiment', value: 45 },
    { subject: 'Volume', value: 50 },
    { subject: 'Trend', value: 80 },
    { subject: 'Risk', value: 30 }
  ]

  const chartData = data && data.length > 0 ? data : defaultData

  // Calculate overall strength/score
  const averageScore = Math.round(
    chartData.reduce((sum, item) => sum + (item.value || 0), 0) / chartData.length
  )

  // Determine strength level
  const getStrengthLevel = (score) => {
    if (score >= 70) return { level: 'Strong', color: '#10b981', label: 'STRONG' }
    if (score >= 50) return { level: 'Moderate', color: '#f59e0b', label: 'MODERATE' }
    if (score >= 30) return { level: 'Weak', color: '#ef4444', label: 'WEAK' }
    return { level: 'Poor', color: '#6b7280', label: 'POOR' }
  }

  const strengthInfo = getStrengthLevel(averageScore)

  return (
    <div className="opportunity-radar-container">
      <div className="radar-header">
        <h3 className="radar-title">Opportunity Strength</h3>
        <div className="radar-score">
          <span className="score-value" style={{ color: strengthInfo.color }}>
            {averageScore}%
          </span>
          <span className="score-label">{strengthInfo.label}</span>
        </div>
      </div>

      <div className="radar-chart-wrapper">
        <ResponsiveContainer width="100%" height={settings.height}>
          <RadarChart
            data={chartData}
            margin={settings.margin}
            cx="50%"
            cy="50%"
          >
            {/* Grid background */}
            <PolarGrid
              stroke={settings.gridStroke}
              fill="none"
              strokeWidth={1}
              polarRadius={[20, 40, 60, 80, 100]}
            />

            {/* Label ring (axis labels) */}
            <PolarAngleAxis
              dataKey="subject"
              tick={(props) => {
                const { x, y, payload } = props
                return (
                  <text
                    x={x}
                    y={y}
                    textAnchor="middle"
                    dominantBaseline="middle"
                    className="radar-axis-label"
                  >
                    {payload.value}
                  </text>
                )
              }}
              stroke="#9ca3af"
            />

            {/* Radial axis (0-100 scale) */}
            <PolarRadiusAxis
              angle={90}
              domain={[0, 100]}
              tick={false}
              tickCount={5}
            />

            {/* Data polygon */}
            <Radar
              name="Metrics"
              dataKey="value"
              stroke={settings.radarStroke}
              fill={settings.radarFill}
              strokeWidth={2}
              fillOpacity={0.6}
              isAnimationActive={true}
              animationDuration={800}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Metrics breakdown */}
      <div className="radar-metrics">
        {chartData.map((item, idx) => (
          <div key={idx} className="metric-item">
            <div className="metric-label">{item.subject}</div>
            <div className="metric-bar-container">
              <div
                className="metric-bar"
                style={{
                  width: `${item.value}%`,
                  backgroundColor: settings.radarStroke
                }}
              ></div>
            </div>
            <div className="metric-value">{item.value}%</div>
          </div>
        ))}
      </div>

      {/* Info footer */}
      <div className="radar-footer">
        <p className="radar-info">
          All metrics must score above 50% for a strong opportunity signal
        </p>
      </div>
    </div>
  )
}

export default OpportunityRadar
