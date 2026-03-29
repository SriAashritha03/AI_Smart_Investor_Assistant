import React from 'react'
import { FaChartBar } from 'react-icons/fa'
import Portfolio from '../Portfolio/Portfolio'
import './PortfolioPage.css'

function PortfolioPage() {
  return (
    <div className="page-container portfolio-page">
      <div className="page-header">
        <h2 className="page-title"><FaChartBar style={{ marginRight: '8px' }} />Portfolio Analyzer</h2>
        <p className="page-description">Analyze and compare multiple stocks in your portfolio</p>
      </div>
      <Portfolio />
    </div>
  )
}

export default PortfolioPage
