import React from 'react'
import './AlertsModal.css'

function AlertsModal({ isOpen, alerts = [], onClose }) {
  if (!isOpen) {
    return null
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
    <>
      {/* Backdrop */}
      <div className="alerts-modal-backdrop" onClick={onClose}></div>

      {/* Modal */}
      <div className="alerts-modal">
        {/* Modal Header */}
        <div className="alerts-modal-header">
          <div className="alerts-modal-title-group">
            <h2 className="alerts-modal-title">📢 Smart Alerts</h2>
            <span className="alerts-modal-badge">{alerts.length}</span>
            {criticalCount > 0 && (
              <span className="alerts-modal-critical-badge">🔴 {criticalCount}</span>
            )}
            {warningCount > 0 && (
              <span className="alerts-modal-warning-badge">🟠 {warningCount}</span>
            )}
          </div>
          <button className="alerts-modal-close" onClick={onClose}>
            ✕
          </button>
        </div>

        {/* Alerts Content */}
        <div className="alerts-modal-content">
          {alerts.length === 0 ? (
            <div className="alerts-empty">
              <span className="empty-icon">😊</span>
              <p>No alerts at this time. Everything looks good!</p>
            </div>
          ) : (
            <div className="alerts-modal-list">
              {alerts.map((alert, idx) => (
                <div
                  key={idx}
                  className={`alerts-modal-item alert-${alert.severity.toLowerCase()}`}
                  style={getSeverityStyle(alert.severity)}
                >
                  <div className="alert-modal-header-item">
                    <div className="alert-modal-title-text">{alert.title}</div>
                    {alert.action && (
                      <span
                        className="alert-modal-action-badge"
                        style={{ backgroundColor: getActionBadgeColor(alert.action) }}
                      >
                        {alert.action}
                      </span>
                    )}
                  </div>
                  <p className="alert-modal-message">{alert.message}</p>
                  <div className="alert-modal-footer">
                    {alert.timestamp && (
                      <span className="alert-modal-timestamp">
                        ⏱️ {new Date(alert.timestamp).toLocaleTimeString()}
                      </span>
                    )}
                    <span className="alert-modal-type">
                      {alert.alert_type}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Modal Stats */}
        <div className="alerts-modal-stats">
          <div className="modal-stat-item">
            <span className="modal-stat-label">Critical</span>
            <span className="modal-stat-value critical">{criticalCount}</span>
          </div>
          <div className="modal-stat-item">
            <span className="modal-stat-label">Warning</span>
            <span className="modal-stat-value warning">{warningCount}</span>
          </div>
          <div className="modal-stat-item">
            <span className="modal-stat-label">Info</span>
            <span className="modal-stat-value info">
              {alerts.filter((a) => a.severity === 'INFO').length}
            </span>
          </div>
          <div className="modal-stat-item">
            <span className="modal-stat-label">Success</span>
            <span className="modal-stat-value success">
              {alerts.filter((a) => a.severity === 'SUCCESS').length}
            </span>
          </div>
        </div>
      </div>
    </>
  )
}

export default AlertsModal
