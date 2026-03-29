import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import './Sidebar.css'

const navItems = [
  { to: '/',             icon: 'dashboard',              label: 'Dashboard' },
  { to: '/chat',         icon: 'chat_bubble',            label: 'Chat' },
  { to: '/portfolio',    icon: 'account_balance_wallet',  label: 'Portfolio' },
  { to: '/video-engine', icon: 'videocam',               label: 'Video Engine' },
]

function Sidebar() {
  const location = useLocation()
  const isActive = (path) => location.pathname === path

  return (
    <aside className="sidebar">
      {/* Brand */}
      <div className="sidebar-brand">
        <div className="sidebar-logo">
          <span className="material-symbols-outlined sidebar-logo-icon">insights</span>
        </div>
        <div>
          <h2 className="sidebar-title">Intelligence</h2>
          <p className="sidebar-subtitle">Active Terminal</p>
        </div>
      </div>

      {/* Nav Items */}
      <nav className="sidebar-nav">
        {navItems.map(({ to, icon, label }) => (
          <Link
            key={to}
            to={to}
            className={`sidebar-link ${isActive(to) ? 'sidebar-link--active' : ''}`}
          >
            <span
              className="material-symbols-outlined"
              style={isActive(to) ? { fontVariationSettings: "'FILL' 1" } : undefined}
            >
              {icon}
            </span>
            <span>{label}</span>
          </Link>
        ))}
      </nav>

      {/* Bottom utility links */}
      <div className="sidebar-footer">
        <a className="sidebar-link" href="#">
          <span className="material-symbols-outlined">settings</span>
          <span>Settings</span>
        </a>
        <a className="sidebar-link" href="#">
          <span className="material-symbols-outlined">help</span>
          <span>Support</span>
        </a>
      </div>
    </aside>
  )
}

export default Sidebar
