import React, { useMemo } from 'react';
import './OpportunityAlerts.css';
import { formatAlertTime } from '../../utils/alertGenerator';

/**
 * OpportunityAlerts Component
 * Displays dynamic alerts generated from stock analysis
 * 
 * @param {Array} alerts - Array of alert objects
 * @param {Boolean} showDemo - Show demo alerts when no live alerts
 */
function OpportunityAlerts({ alerts = [], showDemo = true }) {
  // Show top 3 alerts only
  const displayedAlerts = useMemo(() => {
    return (alerts || []).slice(0, 3);
  }, [alerts]);

  // No alerts and demo disabled
  if (displayedAlerts.length === 0 && !showDemo) {
    return (
      <div className="opportunity-alerts">
        <div className="alerts-header">
          <h3>
            <span className="material-symbols-outlined">notifications_none</span>
            No Active Alerts
          </h3>
          <p className="alerts-subtitle">Waiting for market signals...</p>
        </div>
      </div>
    );
  }

  // Get type badge styling
  const getTypeStyles = (type) => {
    const styles = {
      HIGH: { bg: 'var(--alert-high)', fg: '#fff', icon: '🔴' },
      MEDIUM: { bg: 'var(--alert-medium)', fg: 'var(--on-surface)', icon: '🟡' },
      LOW: { bg: 'var(--alert-low)', fg: 'var(--on-surface)', icon: '🔵' },
    };
    return styles[type] || styles.LOW;
  };

  const getActionColor = (action) => {
    switch (action) {
      case 'BUY': return 'var(--secondary)';
      case 'SELL': return '#F4511E';
      case 'HOLD':
      case 'MONITOR': return 'var(--primary)';
      case 'WATCH': return 'var(--tertiary)';
      default: return 'var(--on-surface-variant)';
    }
  };

  return (
    <div className="opportunity-alerts">
      {/* HEADER */}
      <div className="alerts-header">
        <h3>
          <span className="material-symbols-outlined">notifications_active</span>
          Live Opportunity Alerts
        </h3>
        <span className="alerts-count">{displayedAlerts.length}</span>
      </div>

      {/* ALERTS LIST */}
      <div className="alerts-list">
        {displayedAlerts.length > 0 ? (
          displayedAlerts.map((alert, idx) => {
            const typeStyle = getTypeStyles(alert.type);
            return (
              <div key={idx} className="alert-card">
                {/* Alert Badge & Ticker */}
                <div className="alert-header-row">
                  <div className="alert-badge-ticker">
                    <span
                      className="alert-type-badge"
                      style={{
                        backgroundColor: typeStyle.bg,
                        color: typeStyle.fg,
                      }}
                    >
                      {typeStyle.icon} {alert.type}
                    </span>
                    <span className="alert-ticker">{alert.ticker}</span>
                  </div>
                  <span className="alert-time">{formatAlertTime(alert.timestamp)}</span>
                </div>

                {/* Alert Message */}
                <p className="alert-message">{alert.message}</p>

                {/* Alert Metadata Row */}
                <div className="alert-metadata">
                  {/* Confidence */}
                  <div className="metadata-item">
                    <span className="material-symbols-outlined">trending_up</span>
                    <span>{alert.confidence}% Confidence</span>
                  </div>

                  {/* Action */}
                  {alert.action && (
                    <div className="metadata-item">
                      <span
                        className="action-badge"
                        style={{ color: getActionColor(alert.action) }}
                      >
                        {alert.action}
                      </span>
                    </div>
                  )}

                  {/* Signal Count */}
                  {alert.signals && alert.signals.length > 0 && (
                    <div className="metadata-item">
                      <span className="material-symbols-outlined">bolt</span>
                      <span>{alert.signals.length} Signal{alert.signals.length !== 1 ? 's' : ''}</span>
                    </div>
                  )}
                </div>

                {/* Signals Tags (if any) */}
                {alert.signals && alert.signals.length > 0 && (
                  <div className="alert-signals">
                    {alert.signals.slice(0, 3).map((signal, i) => (
                      <span key={i} className="signal-tag">
                        {typeof signal === 'string' ? signal : signal.name || signal}
                      </span>
                    ))}
                    {alert.signals.length > 3 && (
                      <span className="signal-tag signal-more">
                        +{alert.signals.length - 3} more
                      </span>
                    )}
                  </div>
                )}

                {/* Demo Indicator */}
                {alert.isDemo && (
                  <div className="alert-demo-badge">
                    Demo Alert
                  </div>
                )}
              </div>
            );
          })
        ) : (
          <div className="alerts-empty">
            <span className="material-symbols-outlined">info</span>
            <p>Run an analysis to generate live alerts</p>
          </div>
        )}
      </div>

      {/* FOOTER: Show alert count by type if alerts exist */}
      {displayedAlerts.length > 0 && (
        <div className="alerts-footer">
          <div className="alert-stats">
            {displayedAlerts.filter(a => a.type === 'HIGH').length > 0 && (
              <span className="stat">
                <span className="stat-badge high">●</span>
                {displayedAlerts.filter(a => a.type === 'HIGH').length} High
              </span>
            )}
            {displayedAlerts.filter(a => a.type === 'MEDIUM').length > 0 && (
              <span className="stat">
                <span className="stat-badge medium">●</span>
                {displayedAlerts.filter(a => a.type === 'MEDIUM').length} Medium
              </span>
            )}
            {displayedAlerts.filter(a => a.type === 'LOW').length > 0 && (
              <span className="stat">
                <span className="stat-badge low">●</span>
                {displayedAlerts.filter(a => a.type === 'LOW').length} Low
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default OpportunityAlerts;
