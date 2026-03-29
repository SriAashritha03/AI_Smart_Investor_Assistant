import React from 'react'
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts'
import './OpportunityRadar.css'

function OpportunityRadar({ data }) {
  if (!data) return null

  // Custom Tooltip component for Recharts
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="radar-tooltip">
          <p className="label">{`${payload[0].name} : ${payload[0].value.toFixed(1)}%`}</p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="opportunity-radar-container">
      <div className="radar-chart-wrapper">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
            <PolarGrid 
              gridType="polygon"
              stroke="var(--outline-variant)"
              strokeOpacity={0.2}
            />
            <PolarAngleAxis 
              dataKey="subject" 
              tick={{ fill: 'var(--on-surface-variant)', fontSize: 10, fontWeight: 700 }}
            />
            <PolarRadiusAxis 
              angle={30} 
              domain={[0, 100]} 
              tick={false} 
              axisLine={false}
            />
            <Radar
              name="Market Strength"
              dataKey="value"
              stroke="var(--primary)"
              fill="var(--primary)"
              fillOpacity={0.15}
              strokeWidth={2}
              className="radar-polygon"
            />
            <Tooltip content={<CustomTooltip />} />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Metrics Breakdown */}
      <div className="radar-metrics">
        {data.map((metric, idx) => (
          <div key={idx} className="metric-item">
            <div className="metric-value-row">
              <span className="metric-label">{metric.subject}</span>
              <span className="metric-value">{metric.value.toFixed(0)}%</span>
            </div>
            <div className="metric-bar-container">
              <div 
                className="metric-bar" 
                style={{ width: `${metric.value}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default OpportunityRadar
