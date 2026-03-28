/* ============================================================================
   src/constants/mockData.js - Demo Mode Mock Data
   ============================================================================ */

/**
 * Complete mock analysis response for demo purposes
 * Used when Demo Mode is enabled to provide stable, predictable results
 */
export const DEMO_RESPONSES = {
  AAPL: {
    success: true,
    stock: 'AAPL',
    date: '2026-03-27',
    opportunity_level: 'Moderate',
    confidence: 68,
    action: 'BUY',
    signals_triggered: ['Uptrend', 'Breakout'],
    signal_details: [
      {
        name: 'Uptrend',
        triggered: true,
        strength: 'Moderate',
        reasoning: '5 consecutive days of price increases showing bullish momentum',
      },
      {
        name: 'Breakout',
        triggered: true,
        strength: 'Strong',
        reasoning: 'Price crossed 10-day resistance level at $175.50',
      },
      {
        name: 'Volume Spike',
        triggered: false,
        strength: '-',
        reasoning: 'Trading volume 1.2x average - slight increase but not significant',
      },
      {
        name: 'Price Surge',
        triggered: false,
        strength: '-',
        reasoning: '2.3% price increase - below 3% threshold for significant surge',
      },
    ],
    summary:
      'Apple shows strong bullish momentum with breakout confirmation. Stock has crossed 10-day resistance with 5 consecutive up days. Potential buying opportunity on any pullback.',
    data_points: 124,
  },

  'RELIANCE.NS': {
    success: true,
    stock: 'RELIANCE.NS',
    date: '2026-03-27',
    opportunity_level: 'Strong',
    confidence: 75,
    action: 'BUY',
    signals_triggered: ['Volume Spike', 'Breakout'],
    signal_details: [
      {
        name: 'Volume Spike',
        triggered: true,
        strength: 'Strong',
        reasoning: 'Current volume 1.8x average - significant institutional buying',
      },
      {
        name: 'Breakout',
        triggered: true,
        strength: 'Strong',
        reasoning: 'Price at ₹2,380 exceeds 10-day high of ₹2,350 with volume backing',
      },
      {
        name: 'Uptrend',
        triggered: false,
        strength: '-',
        reasoning: 'Only 2 consecutive up days - below 3-day minimum for uptrend',
      },
      {
        name: 'Price Surge',
        triggered: false,
        strength: '-',
        reasoning: 'Price change 1.3% - below 3% threshold',
      },
    ],
    summary:
      'High conviction breakout signal detected. Reliance showing strong volume backing with price breaking through 10-day resistance. Institutional involvement indicated. Strong buy opportunity.',
    data_points: 124,
  },

  'TCS.NS': {
    success: true,
    stock: 'TCS.NS',
    date: '2026-03-27',
    opportunity_level: 'Weak',
    confidence: 42,
    action: 'HOLD',
    signals_triggered: ['Uptrend'],
    signal_details: [
      {
        name: 'Uptrend',
        triggered: true,
        strength: 'Weak',
        reasoning: '3 consecutive days of price increases - just meeting minimum threshold',
      },
      {
        name: 'Breakout',
        triggered: false,
        strength: '-',
        reasoning: 'Current price ₹3,920 below 10-day high of ₹3,945',
      },
      {
        name: 'Volume Spike',
        triggered: false,
        strength: '-',
        reasoning: 'Current volume 0.9x average - below normal levels',
      },
      {
        name: 'Price Surge',
        triggered: false,
        strength: '-',
        reasoning: '0.8% price change - minimal movement',
      },
    ],
    summary:
      'TCS shows early upward momentum with 3-day uptrend. Limited confirmation - no volume spike or breakout. Wait for stronger signals before strong entry.',
    data_points: 124,
  },

  'INFY.NS': {
    success: true,
    stock: 'INFY.NS',
    date: '2026-03-27',
    opportunity_level: 'None',
    confidence: 15,
    action: 'PASS',
    signals_triggered: [],
    signal_details: [
      {
        name: 'Uptrend',
        triggered: false,
        strength: '-',
        reasoning: '2 up days, 1 down day - no clear uptrend pattern',
      },
      {
        name: 'Breakout',
        triggered: false,
        strength: '-',
        reasoning: 'Current price ₹2,150 below 10-day high of ₹2,165',
      },
      {
        name: 'Volume Spike',
        triggered: false,
        strength: '-',
        reasoning: 'Trading volume 0.8x average - subdued activity',
      },
      {
        name: 'Price Surge',
        triggered: false,
        strength: '-',
        reasoning: 'Price change -0.5% - slight decline',
      },
    ],
    summary:
      'No clear trading signals triggered for Infosys. Price consolidating near 10-day average. Monitor for emerging patterns before committing capital.',
    data_points: 124,
  },

  MSFT: {
    success: true,
    stock: 'MSFT',
    date: '2026-03-27',
    opportunity_level: 'Strong',
    confidence: 79,
    action: 'BUY',
    signals_triggered: ['Volume Spike', 'Breakout', 'Uptrend'],
    signal_details: [
      {
        name: 'Volume Spike',
        triggered: true,
        strength: 'Strong',
        reasoning: 'Current volume 2.1x average - strong institutional interest',
      },
      {
        name: 'Breakout',
        triggered: true,
        strength: 'Strong',
        reasoning: 'Price at $425.80 breaking above 10-day resistance of $420',
      },
      {
        name: 'Uptrend',
        triggered: true,
        strength: 'Moderate',
        reasoning: '4 consecutive days of gains showing momentum building',
      },
      {
        name: 'Price Surge',
        triggered: false,
        strength: '-',
        reasoning: '1.4% increase - below 3% threshold',
      },
    ],
    summary:
      'Microsoft displays excellent setup with multiple confirmations. Three signals aligned: strong volume, breakout, and uptrend. High-conviction entry opportunity with strong institutional backing.',
    data_points: 124,
  },

  TSLA: {
    success: true,
    stock: 'TSLA',
    date: '2026-03-27',
    opportunity_level: 'Moderate',
    confidence: 62,
    action: 'BUY',
    signals_triggered: ['Price Surge', 'Volume Spike'],
    signal_details: [
      {
        name: 'Price Surge',
        triggered: true,
        strength: 'Strong',
        reasoning: '3.7% price increase over 3 days - exceeds surge threshold',
      },
      {
        name: 'Volume Spike',
        triggered: true,
        strength: 'Moderate',
        reasoning: 'Current volume 1.6x average - good buying activity',
      },
      {
        name: 'Uptrend',
        triggered: false,
        strength: '-',
        reasoning: '2 up days, 1 consolidation - insufficient for trend confirmation',
      },
      {
        name: 'Breakout',
        triggered: false,
        strength: '-',
        reasoning: 'Price at $238 still below 10-day high of $240',
      },
    ],
    summary:
      'Tesla rallying with solid price surge and volume backing. 3.7% gain with increased trading activity. Moderate opportunity - consider position sizing due to volatility.',
    data_points: 124,
  },
};

/**
 * Get demo response for a stock
 * Falls back to AAPL if stock not in predefined responses
 * @param {string} ticker - Stock ticker symbol
 * @returns {Object} Demo analysis response
 */
export function getDemoResponse(ticker) {
  return DEMO_RESPONSES[ticker] || DEMO_RESPONSES.AAPL;
}
