import React from 'react'
import './AlertsModal.css'

function AlertsModal({ isOpen, alerts = [], onClose }) {
  if (!isOpen) return null

  const getSeverityClass = (severity) => {
    switch (severity) {
      case 'CRITICAL': return 'alert-critical';
      case 'WARNING':  return 'alert-warning';
      case 'SUCCESS':  return 'alert-success';
      case 'INFO':     return 'alert-info';
      default:         return '';
    }
  }

  const getActionBadgeColor = (action) => {
    switch (action) {
      case 'BUY':    return 'var(--secondary)';
      case 'SELL':   return 'var(--tertiary-container)';
      case 'HOLD':   return 'var(--primary-fixed-dim)';
      case 'WATCH':  return 'var(--primary)';
      default:       return 'var(--outline)';
    }
  }

  const criticalCount = alerts.filter((a) => a.severity === 'CRITICAL').length
  const warningCount = alerts.filter((a) => a.severity === 'WARNING').length

  return (
    <>
      <div className="alerts-modal-backdrop" onClick={onClose}></div>

      <div className="alerts-modal">
        <div className="alerts-modal-header">
          <div className="alerts-modal-title-group">
            <span className="material-symbols-outlined" style={{ color: 'var(--primary)' }}>campaign</span>
            <h2 className="alerts-modal-title">System Alerts</h2>
            <span className="alerts-modal-badge">{alerts.length} Active</span>
          </div>
          <button className="alerts-modal-close" onClick={onClose}>
            <span className="material-symbols-outlined">close</span>
          </button>
        </div>

        <div className="alerts-modal-content">
          {alerts.length === 0 ? (
            <div className="alerts-empty">
              <span className="material-symbols-outlined empty-icon">check_circle</span>
              <p>No active alerts detected. Monitoring market feeds...</p>
            </div>
          ) : (
            <div className="alerts-modal-list">
              {alerts.map((alert, idx) => (
                <div key={idx} className={`alerts-modal-item ${getSeverityClass(alert.severity)}`}>
                  <div className="alert-modal-header-item">
                    <div className="alert-modal-title-text">{alert.title}</div>
                    {alert.action && (
                      <span
                        className="alert-modal-action-badge"
                        style={{ background: getActionBadgeColor(alert.action), color: 'var(--on-primary)' }}
                      >
                        {alert.action}
                      </span>
                    )}
                  </div>
                  <p className="alert-modal-message">{alert.message}</p>
                  <div className="alert-modal-footer">
                    <span className="material-symbols-outlined" style={{ fontSize: '12px', marginRight: '4px' }}>schedule</span>
                    {alert.timestamp ? new Date(alert.timestamp).toLocaleTimeString() : 'Live'}
                    <span style={{ marginLeft: 'auto' }}>{alert.alert_type}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

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
