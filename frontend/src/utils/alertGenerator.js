/**
 * Alert Generation Logic
 * Dynamically generates alerts based on stock analysis data
 */

/**
 * Generate alerts from stock analysis response
 * @param {Object} analysisData - Stock analysis object with confidence, signals, etc.
 * @param {Array} historicalAlerts - Previous alerts (optional, for tracking)
 * @returns {Array} Array of alert objects sorted by severity (HIGH → MEDIUM → LOW)
 */
export const generateAlerts = (analysisData, historicalAlerts = []) => {
  if (!analysisData) return [];

  const alerts = [];
  const timestamp = new Date();

  // Extract data with safe defaults
  const confidence = analysisData.confidence || 0;
  const signalsTriggered = analysisData.signals_triggered || [];
  const signalCount = Array.isArray(signalsTriggered) ? signalsTriggered.length : 0;
  const action = analysisData.action?.toUpperCase() || 'HOLD';
  const ticker = analysisData.stock || 'UNKNOWN';

  // Check for volume spike
  const volumeSpike = analysisData.event_signals?.volume_surge?.detected || false;
  const priceSpikeDetected = analysisData.event_signals?.price_spike?.detected || false;
  const priceChange = analysisData.event_signals?.price_spike?.change_percent || 0;

  // **RULE 1: HIGH ALERT**
  // IF confidence >= 60 AND signals_triggered >= 2
  if (confidence >= 60 && signalCount >= 2) {
    const messages = [];
    
    if (action === 'BUY') {
      messages.push("Strong bullish setup detected");
      if (volumeSpike) messages.push("Volume surge confirmed");
      if (priceSpikeDetected) messages.push(`Price action ${priceChange > 0 ? 'up' : 'down'} ${Math.abs(priceChange).toFixed(1)}%`);
    } else if (action === 'SELL') {
      messages.push("Strong bearish signal confirmed");
      if (volumeSpike) messages.push("Heavy selling volume");
    } else {
      messages.push("Strong opportunity detected - multiple signals aligned");
    }

    alerts.push({
      ticker,
      type: 'HIGH',
      message: messages.join(". "),
      confidence,
      signals: signalsTriggered,
      action,
      timestamp,
      reasoning: `${signalCount} signals with ${confidence}% confidence`,
    });
  }
  // **RULE 2: MEDIUM ALERT**
  // ELSE IF confidence >= 40 AND signals_triggered >= 1
  else if (confidence >= 40 && signalCount >= 1) {
    const messages = [];
    
    if (action === 'BUY') {
      messages.push("Emerging bullish opportunity");
    } else if (action === 'SELL') {
      messages.push("Caution: bearish signals emerging");
    } else {
      messages.push("Emerging opportunity — monitor closely");
    }

    if (volumeSpike) messages.push("Volume activity notable");

    alerts.push({
      ticker,
      type: 'MEDIUM',
      message: messages.join(". "),
      confidence,
      signals: signalsTriggered,
      action,
      timestamp,
      reasoning: `${signalCount} signal(s) with ${confidence}% confidence`,
    });
  }
  // **RULE 3: LOW ALERT**
  // ELSE IF volume_spike == true
  else if (volumeSpike) {
    alerts.push({
      ticker,
      type: 'LOW',
      message: "Unusual trading activity detected — unexpected volume surge",
      confidence: Math.min(confidence + 10, 100),
      signals: signalsTriggered,
      action: 'WATCH',
      timestamp,
      reasoning: "Volume surge detected without strong signal confirmation",
    });
  }
  // **RULE 4: Additional LOW alert for price spike without signals**
  else if (priceSpikeDetected && confidence >= 30) {
    alerts.push({
      ticker,
      type: 'LOW',
      message: `Price movement detected (${Math.abs(priceChange).toFixed(1)}%) — investigate cause`,
      confidence,
      signals: signalsTriggered,
      action: 'MONITOR',
      timestamp,
      reasoning: "Price action detected without overwhelming confirmation",
    });
  }

  // **Bonus Rule: Extreme confidence even with low signals**
  // If confidence is very high (90+), generate an alert regardless
  if (confidence >= 90 && alerts.length === 0) {
    alerts.push({
      ticker,
      type: 'MEDIUM',
      message: "Very high confidence reading — potential breakthrough move incoming",
      confidence,
      signals: signalsTriggered,
      action,
      timestamp,
      reasoning: `Extremely high confidence (${confidence}%) suggests significant move iminent`,
    });
  }

  // Sort alerts by severity: HIGH → MEDIUM → LOW
  const severityOrder = { HIGH: 0, MEDIUM: 1, LOW: 2 };
  alerts.sort((a, b) => severityOrder[a.type] - severityOrder[b.type]);

  return alerts;
};

/**
 * Get demo/mock alerts for when analysis hasn't been run
 * @returns {Array} Array of mock alert objects
 */
export const getDemoAlerts = () => {
  return [
    {
      ticker: 'NVDA',
      type: 'HIGH',
      message: 'Strong breakout detected. Multiple bullish signals aligned with positive sentiment',
      confidence: 78,
      signals: ['Breakout', 'Volume Spike', 'Uptrend'],
      action: 'BUY',
      timestamp: new Date(Date.now() - 5 * 60000), // 5 minutes ago
      reasoning: 'High confidence breakout with volume confirmation',
      isDemo: true,
    },
    {
      ticker: 'META',
      type: 'MEDIUM',
      message: 'Emerging bullish opportunity. Price testing key support level',
      confidence: 52,
      signals: ['Support Level Test'],
      action: 'MONITOR',
      timestamp: new Date(Date.now() - 15 * 60000), // 15 minutes ago
      reasoning: '1 signal with moderate confidence',
      isDemo: true,
    },
    {
      ticker: 'AMD',
      type: 'LOW',
      message: 'Unusual volume surge detected. Price action modest.',
      confidence: 35,
      signals: [],
      action: 'WATCH',
      timestamp: new Date(Date.now() - 30 * 60000), // 30 minutes ago
      reasoning: 'Spike in volume without signal confirmation',
      isDemo: true,
    },
  ];
};

/**
 * Format timestamp for display (e.g., "Just now", "5m ago", "2h ago")
 * @param {Date} date - Timestamp
 * @returns {string} Formatted time string
 */
export const formatAlertTime = (date) => {
  if (!date) return 'Recently';
  
  const now = new Date();
  const diff = Math.floor((now - new Date(date)) / 1000); // seconds

  if (diff < 60) return 'Just now';
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  
  return date.toLocaleDateString();
};

/**
 * Count alerts by type
 * @param {Array} alerts - Array of alert objects
 * @returns {Object} Count of each alert type
 */
export const countAlertsByType = (alerts = []) => {
  return {
    high: alerts.filter(a => a.type === 'HIGH').length,
    medium: alerts.filter(a => a.type === 'MEDIUM').length,
    low: alerts.filter(a => a.type === 'LOW').length,
    total: alerts.length,
  };
};
