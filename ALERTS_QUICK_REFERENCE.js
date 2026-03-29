#!/usr/bin/env node

/**
 * OPPORTUNITY ALERTS SYSTEM - Quick Reference Guide
 * 
 * This file shows how to use and test the alert system.
 */

// ============================================================================
// IMPORT & SETUP
// ============================================================================

import { generateAlerts, getDemoAlerts, formatAlertTime, countAlertsByType } from './alertGenerator'

// ============================================================================
// 1. GENERATING ALERTS FROM ANALYSIS DATA
// ============================================================================

console.log('\n=== 1. Alert Generation Examples ===\n')

// Example analysis data from backend
const analysisData1 = {
  stock: 'AAPL',
  confidence: 75,
  signals_triggered: ['Breakout', 'Volume Spike'],
  action: 'BUY',
  event_signals: {
    volume_surge: { detected: true },
    price_spike: { detected: true, change_percent: 2.5 }
  }
}

const alerts1 = generateAlerts(analysisData1)
console.log('✓ HIGH Alert Generated:')
console.log(JSON.stringify(alerts1[0], null, 2))

// ============================================================================
// 2. DEMO ALERTS
// ============================================================================

console.log('\n=== 2. Demo Alert Examples ===\n')

const demoAlerts = getDemoAlerts()
console.log(`Generated ${demoAlerts.length} demo alerts:`)
demoAlerts.forEach((alert, i) => {
  console.log(`  ${i + 1}. ${alert.ticker} - ${alert.type} - ${alert.message.substring(0, 40)}...`)
})

// ============================================================================
// 3. TIMESTAMP FORMATTING
// ============================================================================

console.log('\n=== 3. Timestamp Formatting ===\n')

const now = new Date()
const oneMinuteAgo = new Date(now - 60 * 1000)
const oneHourAgo = new Date(now - 60 * 60 * 1000)

console.log(`Now: ${formatAlertTime(now)}`)
console.log(`1m ago: ${formatAlertTime(oneMinuteAgo)}`)
console.log(`1h ago: ${formatAlertTime(oneHourAgo)}`)

// ============================================================================
// 4. ALERT COUNT STATISTICS
// ============================================================================

console.log('\n=== 4. Alert Statistics ===\n')

const allAlerts = [
  ...generateAlerts({ confidence: 75, signals_triggered: ['Signal1', 'Signal2'], stock: 'AAPL' }),
  ...generateAlerts({ confidence: 50, signals_triggered: ['Signal1'], stock: 'MSFT' }),
  ...generateAlerts({ confidence: 30, signals_triggered: [], event_signals: { volume_surge: { detected: true } }, stock: 'GOOGL' }),
]

const stats = countAlertsByType(allAlerts)
console.log(`Alert Summary:`)
console.log(`  HIGH: ${stats.high}`)
console.log(`  MEDIUM: ${stats.medium}`)
console.log(`  LOW: ${stats.low}`)
console.log(`  TOTAL: ${stats.total}`)

// ============================================================================
// 5. RULE REFERENCE
// ============================================================================

console.log('\n=== 5. Alert Generation Rules ===\n')

console.log('RULE 1: HIGH ALERT')
console.log('  Condition: confidence >= 60 AND signals_triggered >= 2')
console.log('  Example: 75% confidence, 2+ signals')
console.log()

console.log('RULE 2: MEDIUM ALERT')
console.log('  Condition: confidence >= 40 AND signals_triggered >= 1')
console.log('  Example: 52% confidence, 1 signal')
console.log()

console.log('RULE 3: LOW ALERT')
console.log('  Condition: volume_spike == true')
console.log('  Example: Unusual volume without strong signals')
console.log()

console.log('RULE 4: EXTREME CONFIDENCE')
console.log('  Condition: confidence >= 90 AND no alerts generated')
console.log('  Example: 92% confidence with no other triggers')

// ============================================================================
// 6. COLOR CODING
// ============================================================================

console.log('\n=== 6. Alert Type Styling ===\n')

const styles = {
  HIGH: { icon: '🔴', color: '#F4511E', bg: 'Red' },
  MEDIUM: { icon: '🟡', color: '#FFA600', bg: 'Orange' },
  LOW: { icon: '🔵', color: '#00B4D8', bg: 'Cyan' },
}

Object.entries(styles).forEach(([type, style]) => {
  console.log(`${style.icon} ${type.padEnd(7)} - Color: ${style.color} (${style.bg})`)
})

// ============================================================================
// 7. USAGE IN REACT COMPONENT
// ============================================================================

console.log('\n=== 7. React Component Usage ===\n')

const reactCode = `
import { generateAlerts, getDemoAlerts } from './utils/alertGenerator'
import OpportunityAlerts from './components/Alerts/OpportunityAlerts'

function DashboardPage() {
  // After analysis...
  const result = await analyzeStock(ticker)
  
  // Generate alerts!
  const alerts = generateAlerts(result)
  
  // Pass to component
  return (
    <OpportunityAlerts 
      alerts={alerts}
      showDemo={alerts.length === 0}
    />
  )
}
`

console.log(reactCode)

// ============================================================================
// 8. ALERT OBJECT SCHEMA
// ============================================================================

console.log('\n=== 8. Alert Object Schema ===\n')

const alertSchema = {
  ticker: 'AAPL',                      // Stock ticker
  type: 'HIGH',                        // HIGH | MEDIUM | LOW
  message: 'Strong opportunity detected',  // User-friendly message
  confidence: 75,                      // 0-100%
  signals: ['Breakout', 'Volume'],    // Triggered signals
  action: 'BUY',                       // BUY | SELL | HOLD | MONITOR
  timestamp: new Date(),               // When alert was generated
  reasoning: '2 signals with 75% confidence',  // Why alert triggered
  isDemo: false,                       // Demo mode indicator
}

console.log(JSON.stringify(alertSchema, null, 2))

// ============================================================================
// 9. INTEGRATION CHECKLIST
// ============================================================================

console.log('\n=== 9. Integration Checklist ===\n')

const checklist = [
  '[ ] Import alertGenerator in DashboardPage.jsx',
  '[ ] Call generateAlerts(analysisResult) after analysis',
  '[ ] Pass alerts to Dashboard component',
  '[ ] Dashboard passes to OpportunityAlerts component',
  '[ ] Header receives alerts for notification badge',
  '[ ] Test demo mode with getDemoAlerts()',
  '[ ] Test color coding in browser',
  '[ ] Test responsive design on mobile',
  '[ ] Verify alert count updates',
  '[ ] Check console for no errors',
]

checklist.forEach(item => console.log(item))

// ============================================================================
// 10. TESTING SCENARIOS
// ============================================================================

console.log('\n=== 10. Test Scenarios ===\n')

const testScenarios = [
  {
    scenario: 'Strong Bullish',
    input: { confidence: 78, signals_triggered: ['Breakout', 'Uptrend'], stock: 'BTC' },
    expected: 'HIGH',
  },
  {
    scenario: 'Moderate Signal',
    input: { confidence: 55, signals_triggered: ['Support'], stock: 'ETH' },
    expected: 'MEDIUM',
  },
  {
    scenario: 'Volume Spike Only',
    input: { confidence: 25, signals_triggered: [], event_signals: { volume_surge: { detected: true } }, stock: 'SOL' },
    expected: 'LOW',
  },
  {
    scenario: 'No Alert',
    input: { confidence: 35, signals_triggered: [], event_signals: { volume_surge: { detected: false } }, stock: 'DOGE' },
    expected: 'NONE',
  },
]

testScenarios.forEach(({ scenario, input, expected }) => {
  const alerts = generateAlerts(input)
  const alertType = alerts.length > 0 ? alerts[0].type : 'NONE'
  const pass = alertType === expected ? '✓' : '✗'
  console.log(`${pass} ${scenario.padEnd(20)} → Expected: ${expected.padEnd(6)} Got: ${alertType}`)
})

console.log('\n=== All Examples Complete ===\n')
