# OpportunityRadar Component Integration Guide

## Component Overview
The `OpportunityRadar` component creates a professional radar/spider chart visualization showing 5 key investment metrics with supporting breakdown bars.

## Features
✅ Renders 5 metrics: Technical, Sentiment, Volume, Trend, Risk
✅ Auto-calculates overall strength score (0-100%)
✅ Displays strength level (Strong/Moderate/Weak/Poor)
✅ Includes detailed metrics breakdown
✅ Fully responsive design
✅ Dark theme optimized
✅ Smooth animations

---

## Installation

Recharts is already installed. No additional setup needed.

```bash
npm install recharts
```

---

## Basic Usage

### Simple - Default Demo Data
```jsx
import OpportunityRadar from './components/OpportunityRadar/OpportunityRadar'

function MyComponent() {
  return <OpportunityRadar />
}
```

### With Custom Data
```jsx
import OpportunityRadar from './components/OpportunityRadar/OpportunityRadar'

function Dashboard({ stockData }) {
  // Transform your API data to radar format
  const radarData = [
    { subject: 'Technical', value: stockData.technical_strength },      // 0-100
    { subject: 'Sentiment', value: stockData.sentiment_score },         // 0-100
    { subject: 'Volume', value: stockData.volume_signal },              // 0-100
    { subject: 'Trend', value: stockData.trend_strength },              // 0-100
    { subject: 'Risk', value: 100 - stockData.risk_level }              // Invert risk for display
  ]

  return <OpportunityRadar data={radarData} />
}
```

### With Custom Configuration
```jsx
<OpportunityRadar 
  data={radarData}
  config={{
    height: 350,
    radarStroke: '#10b981',          // Green theme
    radarFill: 'rgba(16, 185, 129, 0.15)',
    gridStroke: 'rgba(200, 200, 200, 0.2)'
  }}
/>
```

---

## Data Format

```javascript
const radarData = [
  {
    subject: "Label",  // String - displayed on chart
    value: 70          // Number - 0 to 100
  },
  // ... up to 5 metrics recommended
]
```

### Suggested Metrics

| Subject | Source | Calculation |
|---------|--------|-------------|
| Technical | signals_triggered / total_signals * 100 |
| Sentiment | (sentiment_score + 1) / 2 * 100 |
| Volume | volume_ratio_to_avg * 100 (capped at 100) |
| Trend | trend_strength_percentage |
| Risk | max(0, 100 - risk_score) |

---

## Integration in Dashboard

### Step 1: Import the component
Add to top of `Dashboard.jsx`:

```jsx
import OpportunityRadar from '../OpportunityRadar/OpportunityRadar'
```

### Step 2: Transform API data

In your Dashboard component, before rendering:

```jsx
// Transform data for radar chart
const getRadarData = (data) => {
  if (!data) return null
  
  return [
    {
      subject: 'Technical',
      value: Math.min(100, (data.signals_triggered.length / data.signal_details.length) * 100)
    },
    {
      subject: 'Sentiment',
      value: data.news_sentiment 
        ? Math.round((data.news_sentiment.sentiment_score + 1) / 2 * 100)
        : 50
    },
    {
      subject: 'Volume',
      value: data.event_signals?.volume_surge?.detected ? 75 : 40
    },
    {
      subject: 'Trend',
      value: data.opportunity_level === 'Strong' ? 80
           : data.opportunity_level === 'Moderate' ? 60
           : 40
    },
    {
      subject: 'Risk',
      value: Math.max(0, 100 - (data.confidence || 50))
    }
  ]
}
```

### Step 3: Add to JSX (above "Analysis Summary")

```jsx
{/* Opportunity Radar */}
{data && (
  <div className="dashboard-section radar-section">
    <OpportunityRadar data={getRadarData(data)} />
  </div>
)}
```

### Step 4: Add to Dashboard.css

```css
.radar-section {
  grid-column: 1 / -1;
  /* Makes it span full width */
}

@media (max-width: 1200px) {
  .radar-section {
    grid-column: 1 / -1;
  }
}
```

---

## Complete Dashboard Integration Example

```jsx
import React from 'react'
import StockChart from '../StockChart/StockChart'
import Watchlist from '../Watchlist/Watchlist'
import ChartPatterns from '../ChartPatterns/ChartPatterns'
import OpportunityRadar from '../OpportunityRadar/OpportunityRadar'  // ← ADD THIS
import './Dashboard.css'

function Dashboard({ data }) {
  // ... existing code ...

  // Add this function
  const getRadarData = (data) => {
    if (!data) return null
    return [
      {
        subject: 'Technical',
        value: Math.min(100, (data.signals_triggered.length / data.signal_details.length) * 100)
      },
      {
        subject: 'Sentiment',
        value: data.news_sentiment 
          ? Math.round((data.news_sentiment.sentiment_score + 1) / 2 * 100)
          : 50
      },
      {
        subject: 'Volume',
        value: data.event_signals?.volume_surge?.detected ? 75 : 40
      },
      {
        subject: 'Trend',
        value: data.opportunity_level === 'Strong' ? 80
             : data.opportunity_level === 'Moderate' ? 60
             : 40
      },
      {
        subject: 'Risk',
        value: Math.max(0, 100 - (data.confidence || 50))
      }
    ]
  }

  return (
    <div className="dashboard-container">
      {/* ... existing sections ... */}

      {/* ADD AFTER summary-cards, BEFORE dashboard-grid */}
      {data && (
        <div className="dashboard-section radar-section">
          <OpportunityRadar data={getRadarData(data)} />
        </div>
      )}

      {/* Main grid continues as before */}
      <div className="dashboard-grid">
        {/* ... existing grid sections ... */}
      </div>
    </div>
  )
}

export default Dashboard
```

---

## Customization Tips

### Change Colors
```jsx
<OpportunityRadar 
  data={radarData}
  config={{
    radarStroke: '#ef4444',      // Red
    radarFill: 'rgba(239, 68, 68, 0.15)'
  }}
/>
```

### Adjust Size
```jsx
<OpportunityRadar 
  data={radarData}
  config={{
    height: 400  // Default is 300
  }}
/>
```

### Remove Metrics Breakdown
Just style `.radar-metrics { display: none }` in CSS if not needed.

---

## API Data Mapping Examples

### From your existing API structure:

```javascript
// If you have signals data
const technicalValue = (triggeredSignals / totalSignals) * 100

// If you have sentiment score (-1 to 1)
const sentimentValue = ((sentimentScore + 1) / 2) * 100

// If you have event signals
const volumeValue = eventSignals.volume_surge.detected ? 75 : 40

// If you have opportunity level
const trendValue = opportunityLevel === 'Strong' ? 80 : 60

// If you have confidence score (0-100)
const riskValue = Math.max(0, 100 - confidence)
```

---

## Advanced: Dynamic Updates

```jsx
// In Dashboard with real-time data
const [radarData, setRadarData] = React.useState(null)

React.useEffect(() => {
  if (data) {
    setRadarData(getRadarData(data))  // Update when data changes
  }
}, [data])

return <OpportunityRadar data={radarData} />
```

---

## Troubleshooting

### Chart not showing?
- Check browser console for errors
- Verify data format: array of objects with `subject` and `value`
- Ensure `value` is between 0-100

### Styling issues?
- Check that OpportunityRadar.css is imported
- Verify CSS custom properties are available (--bg-tertiary, etc.)
- Use browser dev tools to inspect elements

### Performance?
- Component re-renders only when data changes
- Animations are GPU-accelerated
- Safe to use multiple instances

---

## Demo with Mock Data

```jsx
const mockRadarData = [
  { subject: 'Technical', value: 85 },
  { subject: 'Sentiment', value: 62 },
  { subject: 'Volume', value: 74 },
  { subject: 'Trend', value: 90 },
  { subject: 'Risk', value: 25 }
]

export function DemoOpportunityRadar() {
  return (
    <div style={{ width: '100%', padding: '20px' }}>
      <OpportunityRadar data={mockRadarData} />
    </div>
  )
}
```

---

## Component Exports

- **OpportunityRadar.jsx** - Main component
- **OpportunityRadar.css** - Styling file

Both are located in: `frontend/src/components/OpportunityRadar/`
