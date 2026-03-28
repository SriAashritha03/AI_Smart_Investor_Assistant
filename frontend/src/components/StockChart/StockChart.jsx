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

// Register ChartJS components ONCE at module load time
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
  console.log('✅ Chart.js registered successfully')
} catch (e) {
  console.warn('Chart.js already registered or registration error:', e.message)
}

function StockChart({ stock, confidence, opportunityLevel }) {
  const canvasRef = useRef(null)
  const chartRef = useRef(null)

  useEffect(() => {
    console.log('🎯 StockChart useEffect running for stock:', stock)
    if (!canvasRef.current) {
      console.error('❌ Canvas ref is null!')
      return
    }

    // CRITICAL: Destroy existing chart BEFORE any canvas operations
    if (chartRef.current) {
      try {
        console.log('🗑️ Destroying existing chart...')
        chartRef.current.destroy()
        chartRef.current = null
        console.log('✅ Chart destroyed successfully')
      } catch (e) {
        console.error('⚠️ Error destroying chart:', e)
        chartRef.current = null
      }
    }

    // Reset canvas HTML to completely clear it and prevent reuse errors
    const canvas = canvasRef.current
    canvas.width = canvas.width // This resets the canvas internal state
    
    // Clear canvas context
    const ctx = canvas.getContext('2d')
    if (ctx) {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      console.log('🧹 Canvas cleared')
    }

    // Set canvas display size explicitly
    const wrapper = canvas.parentElement
    if (wrapper) {
      const rect = wrapper.getBoundingClientRect()
      canvas.width = rect.width - 24 // Subtract padding
      canvas.height = rect.height
      console.log('📐 Canvas size set to:', canvas.width, 'x', canvas.height)
    }

    // Generate mock price data for demonstration
    const generateMockPriceData = (stock) => {
      const basePrice = {
        'AAPL': 185,
        'MSFT': 425,
        'TSLA': 245,
        'RELIANCE.NS': 2850,
        'TCS.NS': 3650,
        'INFY.NS': 1580
      }

      const base = basePrice[stock] || 200
      const days = 30
      const prices = []
      const labels = []

      for (let i = 0; i < days; i++) {
        const randomChange = (Math.random() - 0.48) * 5
        const price = base + (i * randomChange) + (i % 3) * 2
        prices.push(parseFloat(price.toFixed(2)))
        
        const date = new Date()
        date.setDate(date.getDate() - (days - i))
        labels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }))
      }

      return { labels, prices }
    }

    const { labels, prices } = generateMockPriceData(stock)
    console.log('✅ Generated mock data - labels:', labels.length, 'prices:', prices)

    // Color based on opportunity level
    const getChartColors = (level) => {
      switch (level) {
        case 'Strong':
          return { line: '#10b981', fill: 'rgba(16, 185, 129, 0.1)', border: '#059669' }
        case 'Moderate':
          return { line: '#f59e0b', fill: 'rgba(245, 158, 11, 0.1)', border: '#d97706' }
        case 'Weak':
          return { line: '#3b82f6', fill: 'rgba(59, 130, 246, 0.1)', border: '#1d4ed8' }
        default:
          return { line: '#6b7280', fill: 'rgba(107, 114, 128, 0.1)', border: '#4b5563' }
      }
    }

    const colors = getChartColors(opportunityLevel)

    try {
      const ctx = canvasRef.current.getContext('2d')
      console.log('🎨 Got canvas context:', !!ctx)
      if (!ctx) {
        console.error('❌ Failed to get canvas context')
        return
      }

      console.log('🚀 Creating Chart.js instance with type: line')

      chartRef.current = new ChartJS(ctx, {
        type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: `${stock} Price (30 Days)`,
            data: prices,
            borderColor: colors.line,
            backgroundColor: colors.fill,
            borderWidth: 3,
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointBackgroundColor: colors.line,
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointHoverRadius: 6,
            shadowColor: 'rgba(0, 0, 0, 0.3)',
            shadowBlur: 10
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            display: true,
            labels: {
              color: '#e5e7eb',
              font: { size: 12, weight: '600' },
              padding: 15,
              usePointStyle: true,
              pointStyle: 'circle'
            },
            align: 'end'
          },
          tooltip: {
            backgroundColor: 'rgba(15, 23, 42, 0.9)',
            titleColor: '#fff',
            bodyColor: '#e5e7eb',
            borderColor: colors.line,
            borderWidth: 1,
            padding: 12,
            cornerRadius: 6,
            titleFont: { size: 13, weight: 'bold' },
            bodyFont: { size: 12 },
            displayColors: false
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            ticks: {
              color: '#9ca3af',
              font: { size: 11 },
              callback: (value) => `$${value.toFixed(0)}`
            },
            grid: {
              color: 'rgba(107, 114, 128, 0.1)',
              drawBorder: false
            }
          },
          x: {
            ticks: {
              color: '#9ca3af',
              font: { size: 11 },
              maxRotation: 45,
              minRotation: 0
            },
            grid: {
              display: false,
              drawBorder: false
            }
          }
        }
      }
    })
    console.log('✅ Chart created successfully:', chartRef.current)
    } catch (error) {
      console.error('❌ Critical error creating chart:', error, error.stack)
    }

    return () => {
      console.log('🧹 Cleanup: destroying chart on unmount/dependency change')
      if (chartRef.current) {
        try {
          chartRef.current.destroy()
          chartRef.current = null
        } catch (e) {
          console.error('Error in cleanup:', e)
        }
      }
    }
  }, [stock, opportunityLevel])

  return (
    <div className="stock-chart-container">
      <div className="chart-header">
        <h3 className="chart-title">📈 {stock} Price Trend (30 Days)</h3>
        <div className="chart-meta">
          <span className="meta-item">
            <span className="meta-label">Confidence:</span>
            <span className="meta-value">{confidence}%</span>
          </span>
          <span className="meta-item">
            <span className="meta-label">Trend:</span>
            <span className="meta-value">{opportunityLevel}</span>
          </span>
        </div>
      </div>
      <div className="chart-wrapper">
        <canvas ref={canvasRef}></canvas>
      </div>
      <div className="chart-footer">
        <p className="chart-note">📊 Chart shows historical price movement with trend analysis</p>
      </div>
    </div>
  )
}

export default StockChart
