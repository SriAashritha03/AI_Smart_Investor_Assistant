"""
Stock Analysis Service Module

Orchestrates the complete stock analysis workflow:
1. Fetches historical stock data
2. Detects trading signals
3. Generates opportunity classification
4. Returns complete analysis as structured JSON

This is the business logic layer that combines all analysis modules.
"""

import logging
from typing import Dict

from chart_patterns import analyze_chart_patterns
from signal_detector import detect_signals
from stock_data_fetcher import get_stock_data
from opportunity_radar import generate_opportunity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def analyze_stock(ticker: str) -> Dict:
    """
    Perform complete stock analysis and generate opportunity report.

    Orchestrates the full analysis workflow:
    1. Validates and fetches 6 months of historical stock data
    2. Detects four trading signals (volume spike, price surge, uptrend, breakout)
    3. Classifies opportunity level based on signal combination
    4. Generates confidence score and investment recommendation

    Args:
        ticker (str): Stock ticker symbol (e.g., 'RELIANCE.NS', 'AAPL', 'GOOGL').
                     Must include market prefix for international stocks (e.g., .NS for NSE).

    Returns:
        Dict: Complete analysis report with structure:
            {
                "success": bool,
                "stock": str,
                "date": str,
                "opportunity_level": str,
                "confidence": float,
                "action": str,
                "signals_triggered": List[str],
                "signal_details": List[Dict],
                "summary": str,
                "data_points": int,
                "error": str (only if success=False)
            }

    Error Response (success=False):
        {
            "success": False,
            "error": "Error description",
            "stock": str (ticker attempted)
        }

    Example:
        >>> result = analyze_stock('RELIANCE.NS')
        >>> if result['success']:
        ...     print(f"Opportunity: {result['opportunity_level']}, "
        ...           f"Confidence: {result['confidence']}%")
        ... else:
        ...     print(f"Error: {result['error']}")
    """
    logger.info(f"Starting analysis for {ticker}")

    try:
        # Step 1: Fetch historical stock data
        logger.debug(f"Fetching stock data for {ticker}...")
        stock_data = get_stock_data(ticker)
        data_points = len(stock_data)
        logger.info(f"Fetched {data_points} trading days of data")

        # Step 2: Detect trading signals
        logger.debug("Detecting trading signals...")
        signals = detect_signals(stock_data)
        triggered_count = sum(1 for s in signals if s["triggered"])
        logger.info(f"Detected {triggered_count} triggered signal(s)")

        # Step 2.5: Analyze chart patterns
        logger.debug("Analyzing chart patterns...")
        chart_patterns = analyze_chart_patterns(stock_data, ticker)
        logger.info(f"Chart pattern analysis complete. Strength: {chart_patterns['overall_pattern_strength']}")

        # Step 3: Generate opportunity classification
        logger.debug("Generating opportunity classification...")
        opportunity = generate_opportunity(stock_data, signals, ticker)
        logger.info(
            f"Analysis complete. Opportunity: {opportunity['opportunity_level']}, "
            f"Confidence: {opportunity['confidence']}%"
        )

        # Step 4: Build comprehensive response
        response = {
            "success": True,
            "stock": opportunity["stock"],
            "date": opportunity["date"],
            "opportunity_level": opportunity["opportunity_level"],
            "confidence": opportunity["confidence"],
            "action": opportunity["action"],
            "signals_triggered": opportunity["signals_triggered"],
            "signal_details": opportunity["signal_details"],
            "summary": opportunity["summary"],
            "data_points": data_points,
            "chart_patterns": {
                "overall_strength": chart_patterns["overall_pattern_strength"],
                "patterns_detected": chart_patterns["patterns_detected"],
                "success_rates": chart_patterns["success_rates"],
                "pattern_count": chart_patterns["pattern_count"],
                "recommendation": chart_patterns["recommendation"],
                "recommendation_reasoning": chart_patterns["recommendation_reasoning"],
            }
        }

        logger.info(f"Analysis completed successfully for {ticker}")
        return response

    except ValueError as e:
        # Invalid ticker or data issue
        logger.warning(f"Validation error for {ticker}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "stock": ticker,
        }

    except Exception as e:
        # Unexpected error
        logger.error(f"Unexpected error analyzing {ticker}: {str(e)}")
        return {
            "success": False,
            "error": f"Analysis failed: {str(e)}",
            "stock": ticker,
        }


def batch_analyze_stocks(tickers: list) -> Dict[str, Dict]:
    """
    Analyze multiple stocks in batch.

    Args:
        tickers (list): List of ticker symbols to analyze.

    Returns:
        Dict: Dictionary with ticker as key and analysis result as value.

    Example:
        >>> results = batch_analyze_stocks(['RELIANCE.NS', 'TCS.NS', 'AAPL'])
        >>> for ticker, result in results.items():
        ...     if result['success']:
        ...         print(f"{ticker}: {result['opportunity_level']}")
    """
    logger.info(f"Starting batch analysis for {len(tickers)} stocks")

    results = {}
    for ticker in tickers:
        results[ticker] = analyze_stock(ticker)

    logger.info(f"Batch analysis completed for {len(tickers)} stocks")
    return results
