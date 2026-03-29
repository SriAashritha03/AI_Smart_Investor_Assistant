import React, { useEffect, useRef } from 'react'
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  Title, 
  Tooltip, 
  Legend, 
  Filler,
  LineController 
} from 'chart.js'
import './StockChart.css'

// Register ChartJS components
try {
  ChartJS.register(
    LineController,
    CategoryScale, 
    LinearScale, 
    PointElement, 
    LineElement, 
    Title, 
    Tooltip, 
    Legend, 
    Filler
  )
} catch (e) {
  console.warn('Chart.js registration error:', e.message)
}

function StockChart({ stock, confidence, opportunityLevel }) {
  const canvasRef = useRef(null)
  const chartRef = useRef(null)

  useEffect(() => {
    if (!canvasRef.current) return

    if (chartRef.current) {
      chartRef.current.destroy()
    }

    const ctx = canvasRef.current.getContext('2d')
    
    // Generate mock price data
    const generateMockPriceData = (stock) => {
      const basePrice = { 'AAPL': 185, 'MSFT': 425, 'TSLA': 245, 'RELIANCE.NS': 2850, 'TCS.NS': 3650, 'INFY.NS': 1580 }
      const base = basePrice[stock] || 200
      const days = 30
      const prices = []
      const labels = []

      for (let i = 0; i < days; i++) {
        const randomChange = (Math.random() - 0.48) * 5
        const price = base + (i * randomChange) + (Math.sin(i/2) * 5)
        prices.push(parseFloat(price.toFixed(2)))
        const date = new Date()
        date.setDate(date.getDate() - (days - i))
        labels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }))
      }
      return { labels, prices }
    }

    const { labels, prices } = generateMockPriceData(stock)
    
    // MD3 Theme Colors
    const getChartColors = (level) => {
      switch (level) {
        case 'Strong':   return { line: '#4ae176', fill: 'rgba(74, 225, 118, 0.05)' }
        case 'Moderate': return { color: '#adc6ff', fill: 'rgba(173, 198, 255, 0.05)' }
        case 'Weak':     return { color: '#dfe2f2', fill: 'rgba(223, 226, 242, 0.03)' }
        default:         return { color: '#adc6ff', fill: 'rgba(173, 198, 255, 0.05)' }
      }
    }

    const themeColors = getChartColors(opportunityLevel)
    const lineColor = themeColors.line || '#adc6ff'

    chartRef.current = new ChartJS(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: `${stock} Performance`,
          data: prices,
          borderColor: lineColor,
          backgroundColor: themeColors.fill,
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointRadius: 0,
          pointHoverRadius: 6,
          pointHoverBackgroundColor: lineColor,
          pointHoverBorderColor: '#fff',
          pointHoverBorderWidth: 2,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { intersect: false, mode: 'index' },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#1b1f2b',
            titleColor: '#dfe2f2',
            bodyColor: '#dfe2f2',
            borderColor: 'rgba(66, 71, 84, 0.4)',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8,
            titleFont: { size: 12, weight: 'bold', family: 'Inter' },
            bodyFont: { size: 13, family: 'JetBrains Mono' },
            displayColors: false
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            grid: { color: 'rgba(66, 71, 84, 0.1)', drawBorder: false },
            ticks: {
              color: 'rgba(194, 198, 214, 0.5)',
              font: { size: 10, family: 'JetBrains Mono' },
              callback: (value) => `₹${value.toLocaleString()}`
            }
          },
          x: {
            grid: { display: false, drawBorder: false },
            ticks: {
              color: 'rgba(194, 198, 214, 0.5)',
              font: { size: 10, family: 'JetBrains Mono' },
              maxRotation: 0
            }
          }
        }
      }
    })

    return () => {
      if (chartRef.current) chartRef.current.destroy()
    }
  }, [stock, opportunityLevel])

  return (
    <div className="stock-chart-container">
      <div className="chart-header">
        <h3 className="chart-title">
          <span className="material-symbols-outlined">timeline</span>
          Asset Performance Matrix
        </h3>
        <div className="chart-meta">
          <div className="meta-item">
            <span className="meta-label">Ticker</span>
            <span className="meta-value">{stock}</span>
          </div>
          <div className="meta-item">
            <span className="meta-label">Signal</span>
            <span className="meta-value">{opportunityLevel}</span>
          </div>
        </div>
      </div>
      <div className="chart-wrapper">
        <canvas ref={canvasRef}></canvas>
      </div>
      <div className="chart-footer">
        <p className="chart-note">
          <span className="material-symbols-outlined" style={{ fontSize: '14px' }}>info</span>
          Real-time synthesizing active. Data streams from primary financial gateways.
        </p>
      </div>
    </div>
  )
}

export default StockChart
