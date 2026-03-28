import React, { useState } from 'react'
import './Alerts.css'

function Alerts({ alerts = [] }) {
  const [expandedAlerts, setExpandedAlerts] = useState({})

  if (!alerts || alerts.length === 0) {
    return null
  }

  const toggleExpand = (index) => {
    setExpandedAlerts((prev) => ({
      ...prev,
      [index]: !prev[index],
    }))
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'CRITICAL':
        return '#ef4444'
      case 'WARNING':
        return '#f59e0b'
      case 'SUCCESS':
        return '#10b981'
      case 'INFO':
      default:
        return '#3b82f6'
    }
  }

  const getSeverityStyle = (severity) => {
    const baseColor = getSeverityColor(severity)
    return {
      borderLeftColor: baseColor,
      backgroundColor: `rgba(59, 130, 246, 0.05)`,
    }
  }

  const getActionBadgeColor = (action) => {
    switch (action) {
      case 'BUY':
        return '#10b981'
      case 'SELL':
        return '#ef4444'
      case 'HOLD':
        return '#f59e0b'
      case 'WATCH':
        return '#3b82f6'
      default:
        return '#6b7280'
    }
  }

  const criticalCount = alerts.filter((a) => a.severity === 'CRITICAL').length
  const warningCount = alerts.filter((a) => a.severity === 'WARNING').length

  return (
    <div className="alerts-container">
      {/* Alerts Header */}
      <div className="alerts-header">
        <div className="alerts-title-group">
          <h3 className="alerts-title">📢 Smart Alerts</h3>
          <span className="alerts-badge">{alerts.length}</span>
          {criticalCount > 0 && (
            <span className="critical-badge" title="Critical alerts">
              🔴 {criticalCount}
            </span>
          )}
          {warningCount > 0 && (
            <span className="warning-badge" title="Warning alerts">
              🟠 {warningCount}
            </span>
          )}
        </div>
      </div>

      {/* Alerts List */}
      <div className="alerts-list">
        {alerts.map((alert, idx) => (
          <div
            key={idx}
            className={`alert-item alert-${alert.severity.toLowerCase()}`}
            style={getSeverityStyle(alert.severity)}
          >
            {/* Alert Header */}
            <div
              className="alert-header"
              onClick={() => toggleExpand(idx)}
              style={{ cursor: 'pointer' }}
            >
              <div className="alert-header-left">
                <div className="alert-title-wrapper">
                  <span className="alert-title-text">{alert.title}</span>
                  {alert.action && (
                    <span
                      className="alert-action-badge"
                      style={{ backgroundColor: getActionBadgeColor(alert.action) }}
                    >
                      {alert.action}
                    </span>
                  )}
                </div>
              </div>
              <div className="alert-toggle">
                <span className="toggle-icon">
                  {expandedAlerts[idx] ? '▼' : '▶'}
                </span>
              </div>
            </div>

            {/* Alert Message (Expandable) */}
            {expandedAlerts[idx] && (
              <div className="alert-content">
                <p className="alert-message">{alert.message}</p>
                {alert.timestamp && (
                  <div className="alert-timestamp">
                    ⏱️ {new Date(alert.timestamp).toLocaleTimeString()}
                  </div>
                )}
                <div className="alert-type-badge">
                  Type: <span>{alert.alert_type}</span>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Quick Stats */}
      <div className="alerts-stats">
        <div className="stat-item">
          <span className="stat-label">Critical</span>
          <span className="stat-value critical">{criticalCount}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Warning</span>
          <span className="stat-value warning">{warningCount}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Info</span>
          <span className="stat-value info">
            {alerts.filter((a) => a.severity === 'INFO').length}
          </span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Success</span>
          <span className="stat-value success">
            {alerts.filter((a) => a.severity === 'SUCCESS').length}
          </span>
        </div>
      </div>
    </div>
  )
}

export default Alerts
