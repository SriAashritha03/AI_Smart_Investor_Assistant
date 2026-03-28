/* ============================================================================
   src/services/stockApi.js - API Service Layer
   ============================================================================ */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Analyze a single stock
 * @param {string} ticker - Stock ticker symbol (e.g., 'AAPL', 'RELIANCE.NS')
 * @returns {Promise<Object>} Analysis result with opportunity level, signals, confidence
 */
export async function analyzeStock(ticker) {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze-stock`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ticker }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to analyze stock');
    }

    return await response.json();
  } catch (error) {
    console.error('Stock analysis error:', error);
    throw error;
  }
}

/**
 * Analyze multiple stocks
 * @param {string[]} tickers - Array of stock ticker symbols
 * @returns {Promise<Object>} Batch analysis results
 */
export async function batchAnalyzeStocks(tickers) {
  try {
    const response = await fetch(`${API_BASE_URL}/batch-analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(tickers),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to analyze stocks');
    }

    return await response.json();
  } catch (error) {
    console.error('Batch analysis error:', error);
    throw error;
  }
}

/**
 * Get list of available stocks for analysis
 * @returns {Promise<Object>} List with count and stocks array
 */
export async function getAvailableStocks() {
  try {
    const response = await fetch(`${API_BASE_URL}/stocks`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error('Failed to fetch available stocks');
    }

    return await response.json();
  } catch (error) {
    console.error('Get stocks error:', error);
    throw error;
  }
}

/**
 * Health check - verify backend is running
 * @returns {Promise<boolean>} True if backend is responding
 */
export async function healthCheck() {
  try {
    const response = await fetch(`${API_BASE_URL}/`, {
      method: 'GET',
    });
    return response.ok;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
}

