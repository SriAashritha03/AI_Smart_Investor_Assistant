"""
Opportunity Radar Signal Detection Module

A production-ready module for detecting trading opportunity signals
using technical analysis on historical stock data.

Signals Detected:
- Volume Spike: Current volume > 1.5x average of last 10 days
- Price Surge: Price increased > 3% over last 3 days
- Uptrend: Closing price increased consecutively for 3 days
- Breakout: Current price higher than 10-day maximum
"""

import logging
from typing import Dict, List, Optional

import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Signal Detection Thresholds (Configuration)
VOLUME_SPIKE_THRESHOLD = 1.5  # 1.5x average volume
VOLUME_LOOKBACK = 10  # Days to calculate average volume
PRICE_SURGE_THRESHOLD = 0.03  # 3% price increase
PRICE_SURGE_LOOKBACK = 3  # Days to check price surge
UPTREND_CONSECUTIVE_DAYS = 3  # Consecutive up days
BREAKOUT_LOOKBACK = 10  # Days to find maximum price


def _validate_dataframe(df: pd.DataFrame, min_rows: int = 10) -> None:
    """
    Validate that the input DataFrame has required columns and data.

    Args:
        df (pd.DataFrame): Stock data DataFrame to validate.
        min_rows (int): Minimum number of rows required for analysis.

    Raises:
        ValueError: If DataFrame is invalid or missing required columns.
        TypeError: If df is not a pandas DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df)}")

    required_columns = {"Open", "Close", "High", "Low", "Volume"}
    available_columns = set(df.columns)

    if not required_columns.issubset(available_columns):
        missing = required_columns - available_columns
        raise ValueError(
            f"DataFrame missing required columns: {missing}. "
            f"Available columns: {list(available_columns)}"
        )

    if len(df) < min_rows:
        raise ValueError(
            f"Insufficient data. Need at least {min_rows} rows, got {len(df)}"
        )

    if df.empty or df.isnull().any().any():
        raise ValueError("DataFrame contains NaN values")


def _calculate_signal_strength(ratio: float, threshold: float) -> str:
    """
    Calculate signal strength based on how much it exceeds threshold.

    Args:
        ratio (float): Actual ratio value
        threshold (float): Threshold value

    Returns:
        str: Signal strength level ('Weak', 'Moderate', 'Strong')
    """
    if ratio < threshold:
        return "None"
    
    excess_ratio = (ratio - threshold) / threshold
    
    if excess_ratio < 0.25:  # 0-25% above threshold
        return "Weak"
    elif excess_ratio < 0.75:  # 25-75% above threshold
        return "Moderate"
    else:  # 75%+ above threshold
        return "Strong"


def detect_volume_spike(df: pd.DataFrame) -> Dict:
    """
    Detect if current volume is significantly higher than recent average.

    Volume spike indicates increased market interest and potential opportunity.
    Calculated as: Current Volume > 1.5x (Average Volume of last 10 days)

    Args:
        df (pd.DataFrame): Stock data with 'Volume' column.
                          Must have at least VOLUME_LOOKBACK + 1 rows.

    Returns:
        Dict: Signal dictionary with keys:
            - signal_name (str): 'Volume Spike'
            - triggered (bool): Whether volume spike detected
            - strength (str): Signal strength ('Weak', 'Moderate', 'Strong', 'None')
            - current_volume (int): Current day volume
            - average_volume (float): Average volume of lookback period
            - ratio (float): Current volume / average volume
            - threshold (float): Detection threshold (1.5x)
            - lookback_days (int): Number of days used for average

    Example:
        >>> signal = detect_volume_spike(stock_df)
        >>> if signal['triggered']:
        ...     print(f"Volume spike detected! Ratio: {signal['ratio']:.2f}x")
    """
    try:
        # Get the most recent data point (last row)
        current_volume = float(df["Volume"].iloc[-1])

        # Calculate average volume from last N days (excluding current day)
        avg_volume = float(df["Volume"].iloc[-VOLUME_LOOKBACK - 1 : -1].mean())

        # Calculate ratio
        ratio = current_volume / avg_volume

        # Determine if spike detected
        triggered = ratio > VOLUME_SPIKE_THRESHOLD

        # Calculate signal strength
        strength = _calculate_signal_strength(ratio, VOLUME_SPIKE_THRESHOLD)

        logger.debug(
            f"Volume Spike - Current: {current_volume}, Avg: {avg_volume:.0f}, "
            f"Ratio: {ratio:.2f}x, Strength: {strength}, Triggered: {triggered}"
        )

        return {
            "signal_name": "Volume Spike",
            "triggered": triggered,
            "strength": strength,
            "current_volume": int(current_volume),
            "average_volume": round(avg_volume, 2),
            "ratio": round(ratio, 2),
            "threshold": float(VOLUME_SPIKE_THRESHOLD),
            "lookback_days": VOLUME_LOOKBACK,
        }

    except Exception as e:
        logger.error(f"Error in volume spike detection: {str(e)}")
        raise


def detect_price_surge(df: pd.DataFrame) -> Dict:
    """
    Detect if closing price surged more than 3% over recent days.

    Price surge indicates strong upward momentum and buying pressure.
    Calculated as: ((Current Close - Close N days ago) / Close N days ago) > 3%

    Args:
        df (pd.DataFrame): Stock data with 'Close' column.
                          Must have at least PRICE_SURGE_LOOKBACK + 1 rows.

    Returns:
        Dict: Signal dictionary with keys:
            - signal_name (str): 'Price Surge'
            - triggered (bool): Whether price surge detected
            - strength (str): Signal strength ('Weak', 'Moderate', 'Strong', 'None')
            - current_price (float): Current closing price
            - previous_price (float): Closing price N days ago
            - price_change_percent (float): Percentage change
            - threshold_percent (float): Detection threshold (3%)
            - lookback_days (int): Number of days analyzed

    Example:
        >>> signal = detect_price_surge(stock_df)
        >>> if signal['triggered']:
        ...     print(f"Price surge detected! Change: {signal['price_change_percent']:.2f}%")
    """
    try:
        # Get current and previous closing prices
        current_close = float(df["Close"].iloc[-1])
        previous_close = float(df["Close"].iloc[-PRICE_SURGE_LOOKBACK - 1])

        # Calculate percentage change
        price_change_percent = (
            (current_close - previous_close) / previous_close * 100
        )

        # Determine if surge detected
        threshold_pct = PRICE_SURGE_THRESHOLD * 100
        triggered = price_change_percent > threshold_pct

        # Calculate signal strength (convert percentage to ratio)
        surge_ratio = price_change_percent / threshold_pct
        strength = _calculate_signal_strength(surge_ratio, 1.0)

        logger.debug(
            f"Price Surge - Current: {current_close:.2f}, Previous: {previous_close:.2f}, "
            f"Change: {price_change_percent:.2f}%, Strength: {strength}, Triggered: {triggered}"
        )

        return {
            "signal_name": "Price Surge",
            "triggered": triggered,
            "strength": strength,
            "current_price": round(current_close, 2),
            "previous_price": round(previous_close, 2),
            "price_change_percent": round(price_change_percent, 2),
            "threshold_percent": float(threshold_pct),
            "lookback_days": PRICE_SURGE_LOOKBACK,
        }

    except Exception as e:
        logger.error(f"Error in price surge detection: {str(e)}")
        raise


def detect_uptrend(df: pd.DataFrame) -> Dict:
    """
    Detect if closing price increased consecutively for N days.

    Consecutive up days indicate sustained positive momentum.
    Validates that: Close[i] > Close[i-1] for last N consecutive days.

    Args:
        df (pd.DataFrame): Stock data with 'Close' column.
                          Must have at least UPTREND_CONSECUTIVE_DAYS + 1 rows.

    Returns:
        Dict: Signal dictionary with keys:
            - signal_name (str): 'Uptrend'
            - triggered (bool): Whether uptrend detected
            - strength (str): Signal strength ('Weak', 'Moderate', 'Strong', 'None')
            - consecutive_up_days (int): Number of consecutive up days found
            - required_days (int): Number of days required for signal
            - closing_prices (List[float]): Recent closing prices
            - price_changes (List[float]): Price changes per day

    Example:
        >>> signal = detect_uptrend(stock_df)
        >>> if signal['triggered']:
        ...     print(f"Uptrend detected! {signal['consecutive_up_days']} consecutive up days")
    """
    try:
        # Get recent closing prices
        recent_closes = df["Close"].iloc[
            -UPTREND_CONSECUTIVE_DAYS - 1 : 
        ].values

        # Calculate consecutive up days
        consecutive_up_days = 0
        price_changes = []

        for i in range(1, len(recent_closes)):
            price_change = float(recent_closes[i]) - float(recent_closes[i - 1])
            price_changes.append(round(price_change, 2))

            if float(recent_closes[i]) > float(recent_closes[i - 1]):
                consecutive_up_days += 1
            else:
                consecutive_up_days = 0  # Reset if any down day

        # Determine if uptrend detected
        triggered = consecutive_up_days >= UPTREND_CONSECUTIVE_DAYS

        # Calculate signal strength
        strength = _calculate_signal_strength(
            consecutive_up_days, UPTREND_CONSECUTIVE_DAYS
        )

        logger.debug(
            f"Uptrend - Consecutive Up Days: {consecutive_up_days}, "
            f"Required: {UPTREND_CONSECUTIVE_DAYS}, Strength: {strength}, Triggered: {triggered}"
        )

        return {
            "signal_name": "Uptrend",
            "triggered": triggered,
            "strength": strength,
            "consecutive_up_days": int(consecutive_up_days),
            "required_days": int(UPTREND_CONSECUTIVE_DAYS),
            "closing_prices": [round(float(p), 2) for p in recent_closes],
            "price_changes": price_changes,
        }

    except Exception as e:
        logger.error(f"Error in uptrend detection: {str(e)}")
        raise


def detect_breakout(df: pd.DataFrame) -> Dict:
    """
    Detect if current price is higher than the 10-day maximum.

    Breakout indicates price breaking through resistance level,
    suggesting strong upward momentum.
    Validated as: Current Close > Max(Close) of last 10 days

    Args:
        df (pd.DataFrame): Stock data with 'Close' column.
                          Must have at least BREAKOUT_LOOKBACK + 1 rows.

    Returns:
        Dict: Signal dictionary with keys:
            - signal_name (str): 'Breakout'
            - triggered (bool): Whether breakout detected
            - strength (str): Signal strength ('Weak', 'Moderate', 'Strong', 'None')
            - current_price (float): Current closing price
            - max_price (float): Maximum price in lookback period
            - price_above_max (float): How much above maximum
            - lookback_days (int): Number of days analyzed
            - max_date (str): Date when max price occurred (if available)

    Example:
        >>> signal = detect_breakout(stock_df)
        >>> if signal['triggered']:
        ...     print(f"Breakout detected! Price: {signal['current_price']} above max: {signal['max_price']}")
    """
    try:
        # Get current closing price
        current_close = float(df["Close"].iloc[-1])

        # Get maximum closing price from lookback period (excluding current day)
        lookback_closes = df["Close"].iloc[-BREAKOUT_LOOKBACK - 1 : -1]
        max_price = float(lookback_closes.max())
        max_price_date = lookback_closes.idxmax()

        # Calculate how much above maximum
        price_above_max = current_close - max_price

        # Determine if breakout detected
        triggered = current_close > max_price

        # Calculate signal strength (based on percentage above max)
        if triggered:
            pct_above_max = (price_above_max / max_price) * 100
            strength_ratio = pct_above_max / 2.0  # Use 2% as threshold
            strength = _calculate_signal_strength(strength_ratio, 1.0)
        else:
            strength = "None"

        logger.debug(
            f"Breakout - Current: {current_close:.2f}, Max: {max_price:.2f}, "
            f"Above Max: {price_above_max:.2f}, Strength: {strength}, Triggered: {triggered}"
        )

        return {
            "signal_name": "Breakout",
            "triggered": triggered,
            "strength": strength,
            "current_price": round(current_close, 2),
            "max_price": round(max_price, 2),
            "price_above_max": round(price_above_max, 2),
            "lookback_days": BREAKOUT_LOOKBACK,
            "max_date": str(max_price_date.date()) if hasattr(max_price_date, 'date') else str(max_price_date),
        }

    except Exception as e:
        logger.error(f"Error in breakout detection: {str(e)}")
        raise


def detect_signals(df: pd.DataFrame) -> List[Dict]:
    """
    Detect all opportunity radar signals for stock data.

    Main orchestration function that runs all signal detection algorithms
    and returns structured results for each signal.

    Signals Detected:
    1. Volume Spike - Current volume > 1.5x average (10 days)
    2. Price Surge - Price increased > 3% (3 days)
    3. Uptrend - Consecutive 3-day price increase
    4. Breakout - Current price > 10-day maximum

    Args:
        df (pd.DataFrame): Stock data with columns: Open, Close, High, Low, Volume.
                          Index should be DatetimeIndex (dates of trading).
                          Must have at least 11 rows of historical data.

    Returns:
        List[Dict]: List of signal dictionaries, each containing:
            - signal_name (str): Name of the signal
            - triggered (bool): Whether signal is active
            - Additional signal-specific metrics and thresholds

    Raises:
        ValueError: If DataFrame is invalid or has insufficient data
        TypeError: If df is not a pandas DataFrame

    Example:
        >>> from stock_data_fetcher import get_stock_data
        >>> from signal_detector import detect_signals
        >>> df = get_stock_data('RELIANCE.NS')
        >>> signals = detect_signals(df)
        >>> for signal in signals:
        ...     if signal['triggered']:
        ...         print(f"✓ {signal['signal_name']} TRIGGERED")
        ...     else:
        ...         print(f"✗ {signal['signal_name']} not triggered")
    """
    logger.info("Starting signal detection...")

    # Validate input data
    _validate_dataframe(df)

    try:
        # Run all signal detections
        signals = [
            detect_volume_spike(df),
            detect_price_surge(df),
            detect_uptrend(df),
            detect_breakout(df),
        ]

        # Log results
        triggered_count = sum(1 for s in signals if s["triggered"])
        logger.info(
            f"Signal detection completed. "
            f"Triggered signals: {triggered_count}/{len(signals)}"
        )

        return signals

    except Exception as e:
        logger.error(f"Error during signal detection: {str(e)}")
        raise


def print_signals_report(signals: List[Dict]) -> None:
    """
    Print a formatted report of all signals for easy visualization.

    Args:
        signals (List[Dict]): List of signal dictionaries from detect_signals().

    Example:
        >>> signals = detect_signals(df)
        >>> print_signals_report(signals)
    """
    print("\n" + "=" * 70)
    print("OPPORTUNITY RADAR - SIGNAL DETECTION REPORT")
    print("=" * 70)

    for signal in signals:
        status = "✓ TRIGGERED" if signal["triggered"] else "✗ Not Triggered"
        print(f"\n{signal['signal_name']}: {status}")
        print("-" * 70)

        # Print signal-specific details
        for key, value in signal.items():
            if key not in ["signal_name", "triggered"]:
                if isinstance(value, float):
                    print(f"  {key:.<40} {value:.2f}")
                else:
                    print(f"  {key:.<40} {value}")

    print("\n" + "=" * 70)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    try:
        # Import stock data fetcher
        from stock_data_fetcher import get_stock_data

        print("=" * 70)
        print("OPPORTUNITY RADAR - SIGNAL DETECTION SYSTEM")
        print("=" * 70)

        # Example 1: Detect signals for RELIANCE.NS
        print("\n[Example 1] Fetching RELIANCE.NS stock data...")
        reliance_df = get_stock_data("RELIANCE.NS")
        print(f"Data fetched: {len(reliance_df)} trading days")

        print("\n[Example 1] Running signal detection...")
        reliance_signals = detect_signals(reliance_df)
        print_signals_report(reliance_signals)

        # Example 2: Detect signals for APPLE (AAPL)
        print("\n" + "=" * 70)
        print("\n[Example 2] Fetching APPLE stock data...")
        apple_df = get_stock_data("AAPL")
        print(f"Data fetched: {len(apple_df)} trading days")

        print("\n[Example 2] Running signal detection...")
        apple_signals = detect_signals(apple_df)
        print_signals_report(apple_signals)

        # Example 3: Filter only triggered signals from both stocks
        print("\n" + "=" * 70)
        print("\n[Example 3] All Triggered Signals Summary")
        print("-" * 70)
        all_triggered_signals = [
            ("RELIANCE.NS", s) for s in reliance_signals if s["triggered"]
        ] + [("AAPL", s) for s in apple_signals if s["triggered"]]

        if all_triggered_signals:
            print(f"Found {len(all_triggered_signals)} triggered signal(s):\n")
            for ticker, signal in all_triggered_signals:
                print(
                    f"  ✓ {ticker:15} | {signal['signal_name']:15} | "
                    f"Strength: {signal['strength']}"
                )
        else:
            print("No signals currently triggered.")

    except Exception as e:
        logger.error(f"Error in signal detection example: {str(e)}")
        print(f"Error: {str(e)}")
