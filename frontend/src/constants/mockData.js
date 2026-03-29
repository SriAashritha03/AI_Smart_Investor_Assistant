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
    news_sentiment: {
      sentiment_label: 'Positive',
      sentiment_score: 0.45,
      articles_analyzed: 8,
      confidence: 80.0,
      summary: 'Analyzed 8 recent headlines. Overall sentiment is Positive.',
      top_headlines: [
        'Apple Beats Q1 Earnings Estimates',
        'iPhone 15 Sales Surge Past Forecasts',
        'New MacBook Pro M4 Announced'
      ]
    },
    event_signals: {
      events_detected: ['Price Spike'],
      price_spike: {
        detected: true,
        change_percent: 2.3,
        direction: 'upward',
        description: 'Price moved 2.3% upward in 2 days.'
      },
      volume_surge: {
        detected: false,
        ratio: 1.2,
        average_volume: 50000000,
        current_volume: 60000000,
        description: 'Volume at 1.2x average (threshold: 1.5x).'
      },
      summary: 'Events detected: Price Spike'
    }
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
    news_sentiment: {
      sentiment_label: 'Positive',
      sentiment_score: 0.65,
      articles_analyzed: 10,
      confidence: 90.0,
      summary: 'Analyzed 10 recent headlines. Overall sentiment is Positive.',
      top_headlines: [
        'Reliance Q4 Earnings Surge',
        'Refining Unit Production Recovery',
        'New Energy Division Expansion Announced'
      ]
    },
    event_signals: {
      events_detected: ['Volume Surge'],
      price_spike: {
        detected: false,
        change_percent: 1.3,
        direction: 'upward',
        description: 'Price moved 1.3% upward in 2 days.'
      },
      volume_surge: {
        detected: true,
        ratio: 1.8,
        average_volume: 35000000,
        current_volume: 63000000,
        description: 'Volume surged to 1.8x average.'
      },
      summary: 'Events detected: Volume Surge'
    }
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
    news_sentiment: {
      sentiment_label: 'Neutral',
      sentiment_score: 0.05,
      articles_analyzed: 5,
      confidence: 50.0,
      summary: 'Analyzed 5 recent headlines. Overall sentiment is Neutral.',
      top_headlines: [
        'TCS Q4 Results Meet Expectations',
        'India Tech Hiring Expected to Rise',
        'TCS Steady on Margins'
      ]
    },
    event_signals: {
      events_detected: [],
      price_spike: {
        detected: false,
        change_percent: 0.8,
        direction: 'upward',
        description: 'Price moved 0.8% upward in 2 days.'
      },
      volume_surge: {
        detected: false,
        ratio: 0.9,
        average_volume: 20000000,
        current_volume: 18000000,
        description: 'Volume at 0.9x average (threshold: 1.5x).'
      },
      summary: 'No significant events detected.'
    }
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
    news_sentiment: {
      sentiment_label: 'Negative',
      sentiment_score: -0.35,
      articles_analyzed: 7,
      confidence: 70.0,
      summary: 'Analyzed 7 recent headlines. Overall sentiment is Negative.',
      top_headlines: [
        'Infosys Guidance Reduced for FY27',
        'Tech Spending Slowdown Concerns',
        'Client Attrition Risk Flagged'
      ]
    },
    event_signals: {
      events_detected: [],
      price_spike: {
        detected: false,
        change_percent: -0.5,
        direction: 'downward',
        description: 'Price moved 0.5% downward in 2 days.'
      },
      volume_surge: {
        detected: false,
        ratio: 0.8,
        average_volume: 15000000,
        current_volume: 12000000,
        description: 'Volume at 0.8x average (threshold: 1.5x).'
      },
      summary: 'No significant events detected.'
    }
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
    news_sentiment: {
      sentiment_label: 'Positive',
      sentiment_score: 0.55,
      articles_analyzed: 9,
      confidence: 85.0,
      summary: 'Analyzed 9 recent headlines. Overall sentiment is Positive.',
      top_headlines: [
        'Microsoft AI Leadership Affirmed',
        'Cloud Revenue Beats Estimates',
        'Copilot Integration Drives Adoption'
      ]
    },
    event_signals: {
      events_detected: ['Price Spike', 'Volume Surge'],
      price_spike: {
        detected: true,
        change_percent: 3.5,
        direction: 'upward',
        description: 'Price moved 3.5% upward in 2 days.'
      },
      volume_surge: {
        detected: true,
        ratio: 2.1,
        average_volume: 40000000,
        current_volume: 84000000,
        description: 'Volume surged to 2.1x average.'
      },
      summary: 'Events detected: Price Spike, Volume Surge'
    }
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
    news_sentiment: {
      sentiment_label: 'Positive',
      sentiment_score: 0.40,
      articles_analyzed: 6,
      confidence: 60.0,
      summary: 'Analyzed 6 recent headlines. Overall sentiment is Positive.',
      top_headlines: [
        'Tesla Q1 Deliveries Exceed Targets',
        'New Model Announcement Coming Soon',
        'Energy Division Ramp Up Ahead'
      ]
    },
    event_signals: {
      events_detected: ['Price Spike'],
      price_spike: {
        detected: true,
        change_percent: 3.7,
        direction: 'upward',
        description: 'Price moved 3.7% upward in 2 days.'
      },
      volume_surge: {
        detected: true,
        ratio: 1.6,
        average_volume: 120000000,
        current_volume: 192000000,
        description: 'Volume surged to 1.6x average.'
      },
      summary: 'Events detected: Price Spike, Volume Surge'
    }
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
