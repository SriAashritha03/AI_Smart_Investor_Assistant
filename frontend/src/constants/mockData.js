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
    chart_patterns: {
      overall_strength: 'Moderate',
      pattern_count: 2,
      patterns_detected: [
        {
          pattern_name: 'Breakout',
          detected: true,
          strength: 'Strong',
          current_price: 185.50,
          resistance_level: 182.30,
          breakout_margin: 1.75,
          volume_confirmation: true,
        },
        {
          pattern_name: 'Support',
          detected: true,
          strength: 'Moderate',
          current_price: 185.50,
          support_level: 178.50,
          distance_from_support: 3.87,
          recent_bounce: true,
        },
        {
          pattern_name: 'MA Crossover',
          detected: false,
          strength: 'None',
          crossover_type: 'None',
          sma50: 183.20,
          sma200: 184.10,
          ma_distance: -0.49,
        },
      ],
      success_rates: {
        breakout: 62.5,
        support: 58.3,
        ma_crossover: 0.0,
        overall: 40.3,
      },
      recommendation: 'BUY',
      recommendation_reasoning:
        'Strong breakout detected with volume confirmation and support holding. Dual pattern confirmation suggests good entry point.',
    },
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
    chart_patterns: {
      overall_strength: 'Strong',
      pattern_count: 2,
      patterns_detected: [
        {
          pattern_name: 'Breakout',
          detected: true,
          strength: 'Strong',
          current_price: 2854.50,
          resistance_level: 2793.25,
          breakout_margin: 2.19,
          volume_confirmation: true,
        },
        {
          pattern_name: 'Support',
          detected: false,
          strength: 'None',
          current_price: 2854.50,
          support_level: 2680.30,
          distance_from_support: 6.49,
          recent_bounce: false,
        },
        {
          pattern_name: 'MA Crossover',
          detected: true,
          strength: 'Strong',
          crossover_type: 'Golden Cross',
          sma50: 2820.35,
          sma200: 2750.10,
          ma_distance: 2.56,
        },
      ],
      success_rates: {
        breakout: 64.2,
        support: 45.8,
        ma_crossover: 58.5,
        overall: 56.2,
      },
      recommendation: 'BUY',
      recommendation_reasoning:
        'Multiple bullish signals: Breakout with strong volume + Golden Cross. Highest conviction setup. Strong buy opportunity.',
    },
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
    chart_patterns: {
      overall_strength: 'Weak',
      pattern_count: 1,
      patterns_detected: [
        {
          pattern_name: 'Breakout',
          detected: false,
          strength: 'None',
          current_price: 3920.0,
          resistance_level: 3945.0,
          breakout_margin: -0.63,
          volume_confirmation: false,
        },
        {
          pattern_name: 'Support',
          detected: true,
          strength: 'Weak',
          current_price: 3920.0,
          support_level: 3885.0,
          distance_from_support: 0.9,
          recent_bounce: true,
        },
        {
          pattern_name: 'MA Crossover',
          detected: false,
          strength: 'None',
          crossover_type: 'None',
          sma50: 3915.0,
          sma200: 3950.0,
          ma_distance: -0.89,
        },
      ],
      success_rates: {
        breakout: 0.0,
        support: 22.5,
        ma_crossover: 0.0,
        overall: 7.5,
      },
      recommendation: 'HOLD',
      recommendation_reasoning:
        'Weak support detected but no strong patterns. Overall success rate very low. Wait for breakout confirmation before considering entry.',
    },
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
    chart_patterns: {
      overall_strength: 'Weak',
      pattern_count: 0,
      patterns_detected: [
        {
          pattern_name: 'Breakout',
          detected: false,
          strength: 'None',
          current_price: 2150.0,
          resistance_level: 2165.0,
          breakout_margin: -0.69,
          volume_confirmation: false,
        },
        {
          pattern_name: 'Support',
          detected: false,
          strength: 'None',
          current_price: 2150.0,
          support_level: 2130.0,
          distance_from_support: 0.94,
          recent_bounce: false,
        },
        {
          pattern_name: 'MA Crossover',
          detected: false,
          strength: 'None',
          crossover_type: 'None',
          sma50: 2155.0,
          sma200: 2145.0,
          ma_distance: 0.47,
        },
      ],
      success_rates: {
        breakout: 0.0,
        support: 0.0,
        ma_crossover: 0.0,
        overall: 0.0,
      },
      recommendation: 'WAIT',
      recommendation_reasoning:
        'No patterns detected and 0% success rate. Price consolidating without clear direction. Wait for stronger signals before taking any position.',
    },
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
    chart_patterns: {
      overall_strength: 'Strong',
      pattern_count: 2,
      patterns_detected: [
        {
          pattern_name: 'Breakout',
          detected: true,
          strength: 'Strong',
          current_price: 445.75,
          resistance_level: 438.50,
          breakout_margin: 1.66,
          volume_confirmation: true,
        },
        {
          pattern_name: 'Support',
          detected: true,
          strength: 'Strong',
          current_price: 445.75,
          support_level: 425.20,
          distance_from_support: 4.85,
          recent_bounce: true,
        },
        {
          pattern_name: 'MA Crossover',
          detected: true,
          strength: 'Strong',
          crossover_type: 'Golden Cross',
          sma50: 442.30,
          sma200: 435.50,
          ma_distance: 1.57,
        },
      ],
      success_rates: {
        breakout: 68.0,
        support: 65.0,
        ma_crossover: 62.0,
        overall: 65.0,
      },
      recommendation: 'BUY',
      recommendation_reasoning:
        'Excellent setup with triple confirmation: Strong breakout, solid support hold, and Golden Cross. High conviction buy with 65% historical success rate.',
    },
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
    chart_patterns: {
      overall_strength: 'Moderate',
      pattern_count: 1,
      patterns_detected: [
        {
          pattern_name: 'Breakout',
          detected: false,
          strength: 'None',
          current_price: 238.0,
          resistance_level: 240.0,
          breakout_margin: -0.83,
          volume_confirmation: false,
        },
        {
          pattern_name: 'Support',
          detected: true,
          strength: 'Moderate',
          current_price: 238.0,
          support_level: 228.5,
          distance_from_support: 4.15,
          recent_bounce: true,
        },
        {
          pattern_name: 'MA Crossover',
          detected: false,
          strength: 'Weak',
          crossover_type: 'None',
          sma50: 235.0,
          sma200: 232.50,
          ma_distance: 1.07,
        },
      ],
      success_rates: {
        breakout: 0.0,
        support: 51.5,
        ma_crossover: 35.0,
        overall: 28.8,
      },
      recommendation: 'HOLD',
      recommendation_reasoning:
        'Support is holding but no breakout yet. Price surge is positive but needs confirmation. Wait for breakout above $240 resistance for stronger entry.',
    },
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
