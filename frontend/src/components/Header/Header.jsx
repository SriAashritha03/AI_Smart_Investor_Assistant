import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import './Header.css'

function Header({ demoMode = true, onDemoModeChange = () => {}, alerts = [], onAlertsToggle = () => {} }) {
  const criticalCount = alerts.filter((a) => a.severity === 'CRITICAL').length
  
function Header({ demoMode = true, onDemoModeChange = () => {} }) {
  const location = useLocation()

  const isActive = (path) => location.pathname === path ? 'active' : ''

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <h1 className="header-title">
            <span className="title-icon">📊</span>
            AI Smart Investor Assistant
          </h1>
          <p className="header-subtitle">Technical Signal Analysis & Opportunity Detection</p>
        </div>

        {/* Navigation Bar */}
        <nav className="navbar">
          <Link to="/" className={`nav-link ${isActive('/')}`}>
            📈 Dashboard
          </Link>
          <Link to="/chat" className={`nav-link ${isActive('/chat')}`}>
            💬 Chat
          </Link>
        </nav>

        <div className="header-right">
          {/* Notification Bell */}
          <button 
            className="notification-bell"
            onClick={onAlertsToggle}
            title={`${alerts.length} alerts`}
          >
            <span className="bell-icon">🔔</span>
            {alerts.length > 0 && (
              <span className="notification-badge">
                {alerts.length > 9 ? '9+' : alerts.length}
              </span>
            )}
            {criticalCount > 0 && (
              <span className="critical-dot" title={`${criticalCount} critical alerts`}>●</span>
            )}
          </button>

          {/* Demo Mode Toggle */}
          <div className="demo-mode-section">
            <label htmlFor="demo-toggle" className="demo-toggle-label">
              <input
                id="demo-toggle"
                type="checkbox"
                checked={demoMode}
                onChange={(e) => onDemoModeChange(e.target.checked)}
                className="demo-toggle-input"
              />
              <span className="demo-toggle-switch"></span>
              <span className="demo-toggle-text">Demo Mode</span>
            </label>
            {demoMode && <span className="demo-badge">🎭 Demo Active</span>}
          </div>

          {/* Status Indicator */}
          <div className="status-indicator">
            <span className="status-dot"></span>
            <span className="status-text">Live Feed</span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
