import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import './Header.css'

function Header({ demoMode = true, onDemoModeChange = () => { }, alerts = [], onAlertsToggle = () => { } }) {
  const criticalCount = alerts.filter((a) => a.severity === 'CRITICAL').length
  const location = useLocation()
  const isActive = (path) => location.pathname === path

  return (
    <header className="header">
      <div className="header-inner">
        {/* Brand + Horizontal Nav (on large screens) */}
        <div className="header-left">
          <span className="header-brand">Smart Investor</span>

          {/* Horizontal nav links — visible on large screens */}
          <nav className="header-nav">
            <Link to="/" className={`header-nav-link ${isActive('/') ? 'header-nav-link--active' : ''}`}>
              Dashboard
            </Link>
            <Link to="/chat" className={`header-nav-link ${isActive('/chat') ? 'header-nav-link--active' : ''}`}>
              Chat
            </Link>
            <Link to="/portfolio" className={`header-nav-link ${isActive('/portfolio') ? 'header-nav-link--active' : ''}`}>
              Portfolio
            </Link>
            <Link to="/video-engine" className={`header-nav-link ${isActive('/video-engine') ? 'header-nav-link--active' : ''}`}>
              Video Engine
            </Link>
          </nav>
        </div>

        {/* Right Controls */}
        <div className="header-right">
          {/* Search */}
          

          {/* Icon Buttons */}
          <div className="header-icons">
            {/* Notifications */}
            <button className="header-icon-btn" onClick={onAlertsToggle} title={`${alerts.length} alerts`}>
              <span className="material-symbols-outlined">notifications</span>
              {alerts.length > 0 && (
                <span className="header-badge">{alerts.length > 9 ? '9+' : alerts.length}</span>
              )}
            </button>

            {/* Demo Mode Toggle */}
            <button
              className={`header-icon-btn ${demoMode ? 'header-icon-btn--active' : ''}`}
              onClick={() => onDemoModeChange(!demoMode)}
              title={demoMode ? 'Demo Mode ON' : 'Demo Mode OFF'}
            >
              <span className="material-symbols-outlined">
                {demoMode ? 'toggle_on' : 'toggle_off'}
              </span>
            </button>

            {/* Live Status */}
            <button className="header-icon-btn" title="Live Feed">
              <span className="material-symbols-outlined">sensors</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
