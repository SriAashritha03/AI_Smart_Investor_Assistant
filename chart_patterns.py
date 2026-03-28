"""
Chart Pattern Intelligence Module

Detects chart patterns (breakout, support, moving average crossover)
and calculates historical success rates based on backtesting.

Patterns Detected:
- Breakout: Price breaks above resistance with confirmation
- Support: Price bounces from support level with reversal
- MA Crossover: Golden Cross (SMA50 > SMA200) / Death Cross (SMA50 < SMA200)

Success Rate: Percentage of times pattern led to 5%+ price increase within 10 days.
"""

import logging
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Pattern Configuration
MA_SHORT = 50  # Medium-term moving average
MA_LONG = 200  # Long-term moving average
PROFIT_TARGET = 0.05  # 5% price increase target
LOOKFORWARD_DAYS = 10  # Days to check for profit target
BREAKOUT_THRESHOLD = 0.02  # 2% above resistance
SUPPORT_THRESHOLD = 0.02  # 2% above support level


def _calculate_moving_averages(df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """Calculate moving averages, adjusting window if insufficient data."""
    sma50 = df["Close"].rolling(window=min(MA_SHORT, len(df))).mean()
    
    # Use adaptive window for SMA200 if insufficient data
    ma_long_window = min(MA_LONG, max(50, len(df) // 2))
    sma200 = df["Close"].rolling(window=ma_long_window).mean()
    
    return sma50, sma200


def _calculate_support_resistance(df: pd.DataFrame, window: int = 20) -> Tuple[float, float]:

    support = df["Low"].iloc[-window:].min()
    resistance = df["High"].iloc[-window:].max()
    return float(support), float(resistance)


def detect_breakout_pattern(df: pd.DataFrame) -> Dict:
    """
    Detect breakout pattern: Current price breaks above resistance significantly.

    Breakout confirmed when:
    - Current close > 20-day resistance level × (1 + BREAKOUT_THRESHOLD)
    - With above-average volume

    Args:
        df (pd.DataFrame): Stock data with 'Close', 'High', 'Volume' columns.

    Returns:
        Dict: Pattern detection with keys:
            - pattern_name (str): 'Breakout'
            - detected (bool): Whether pattern detected
            - current_price (float): Current closing price
            - resistance_level (float): Resistance level breached
            - breakout_margin (float): Percentage above resistance
            - volume_confirmation (bool): Volume above average
            - strength (str): Pattern strength (Strong/Moderate/Weak)
    """
    try:
        current_price = float(df["Close"].iloc[-1])
        support, resistance = _calculate_support_resistance(df)

        # Check if price breaks above resistance
        breakout_threshold_price = resistance * (1 + BREAKOUT_THRESHOLD)
        breakout_detected = current_price > breakout_threshold_price

        # Volume confirmation
        current_volume = float(df["Volume"].iloc[-1])
        avg_volume = float(df["Volume"].iloc[-20:].mean())
        volume_confirmed = current_volume > (avg_volume * 1.3)

        # Calculate breakout margin
        breakout_margin = ((current_price - resistance) / resistance) * 100 if resistance > 0 else 0

        # Determine strength
        if breakout_detected and volume_confirmed:
            if breakout_margin > 5:
                strength = "Strong"
            elif breakout_margin > 2:
                strength = "Moderate"
            else:
                strength = "Weak"
        else:
            strength = "None"

        logger.debug(
            f"Breakout Pattern - Current: {current_price}, Resistance: {resistance}, "
            f"Margin: {breakout_margin:.2f}%, Volume Confirmed: {volume_confirmed}, "
            f"Detected: {breakout_detected}"
        )

        return {
            "pattern_name": "Breakout",
            "detected": breakout_detected,
            "current_price": round(current_price, 2),
            "resistance_level": round(resistance, 2),
            "breakout_margin": round(breakout_margin, 2),
            "volume_confirmation": volume_confirmed,
            "strength": strength,
        }

    except Exception as e:
        logger.error(f"Error in breakout pattern detection: {str(e)}")
        raise


def detect_support_pattern(df: pd.DataFrame) -> Dict:
    """
    Detect support bounce pattern: Price bounces from support level with potential reversal.

    Support confirmed when:
    - Current close > 20-day support level × (1 + SUPPORT_THRESHOLD)
    - Recent low near support (within 2%)

    Args:
        df (pd.DataFrame): Stock data with 'Close', 'Low' columns.

    Returns:
        Dict: Pattern detection with keys:
            - pattern_name (str): 'Support'
            - detected (bool): Whether pattern detected
            - current_price (float): Current closing price
            - support_level (float): Support level identified
            - distance_from_support (float): Price distance from support (%)
            - recent_bounce (bool): Recent bounce from support
            - strength (str): Pattern strength (Strong/Moderate/Weak)
    """
    try:
        current_price = float(df["Close"].iloc[-1])
        support, _ = _calculate_support_resistance(df)

        # Check if price bounced above support
        support_threshold_price = support * (1 + SUPPORT_THRESHOLD)
        support_detected = current_price > support_threshold_price

        # Check for recent bounce (low within 2% of support)
        recent_low = float(df["Low"].iloc[-5:].min())
        bounce_confirmed = abs(recent_low - support) / support < 0.02 if support > 0 else False

        # Calculate distance from support
        distance_from_support = ((current_price - support) / support) * 100 if support > 0 else 0

        # Determine strength
        if support_detected and bounce_confirmed:
            if distance_from_support > 3:
                strength = "Strong"
            elif distance_from_support > 1:
                strength = "Moderate"
            else:
                strength = "Weak"
        else:
            strength = "None"

        logger.debug(
            f"Support Pattern - Current: {current_price}, Support: {support}, "
            f"Distance: {distance_from_support:.2f}%, Bounce: {bounce_confirmed}, "
            f"Detected: {support_detected}"
        )

        return {
            "pattern_name": "Support",
            "detected": support_detected,
            "current_price": round(current_price, 2),
            "support_level": round(support, 2),
            "distance_from_support": round(distance_from_support, 2),
            "recent_bounce": bounce_confirmed,
            "strength": strength,
        }

    except Exception as e:
        logger.error(f"Error in support pattern detection: {str(e)}")
        raise


def detect_ma_crossover_pattern(df: pd.DataFrame) -> Dict:
    """
    Detect moving average crossover patterns.

    Golden Cross: SMA50 > SMA200 (bullish signal)
    Death Cross: SMA50 < SMA200 (bearish signal)

    Args:
        df (pd.DataFrame): Stock data with 'Close' column.

    Returns:
        Dict: Pattern detection with keys:
            - pattern_name (str): 'MA Crossover'
            - crossover_type (str): 'Golden Cross' or 'Death Cross' or 'None'
            - detected (bool): Whether crossover just occurred
            - sma50 (float): 50-day moving average
            - sma200 (float): 200-day moving average
            - ma_distance (float): Distance between MAs (%)
            - strength (str): Pattern strength (Strong/Moderate/Weak)
    """
    try:
        sma50, sma200 = _calculate_moving_averages(df)

        # Get current values (last valid values)
        current_sma50 = float(sma50.iloc[-1])
        current_sma200 = float(sma200.iloc[-1])
        previous_sma50 = float(sma50.iloc[-2]) if len(sma50) > 1 else current_sma50
        previous_sma200 = float(sma200.iloc[-2]) if len(sma200) > 1 else current_sma200

        # Determine crossover type
        if current_sma50 > current_sma200:
            crossover_type = "Golden Cross"
            just_crossed = previous_sma50 <= previous_sma200
        elif current_sma50 < current_sma200:
            crossover_type = "Death Cross"
            just_crossed = previous_sma50 >= previous_sma200
        else:
            crossover_type = "None"
            just_crossed = False

        # Calculate MA distance
        ma_distance = ((current_sma50 - current_sma200) / current_sma200) * 100 if current_sma200 > 0 else 0

        # Determine strength
        if just_crossed:
            strength = "Strong"  # Fresh crossover
            detected = True
        elif crossover_type != "None" and abs(ma_distance) > 2:
            strength = "Moderate"
            detected = True
        elif crossover_type != "None":
            strength = "Weak"
            detected = True
        else:
            strength = "None"
            detected = False

        logger.debug(
            f"MA Crossover Pattern - Type: {crossover_type}, SMA50: {current_sma50:.2f}, "
            f"SMA200: {current_sma200:.2f}, Distance: {ma_distance:.2f}%, "
            f"Just Crossed: {just_crossed}"
        )

        return {
            "pattern_name": "MA Crossover",
            "crossover_type": crossover_type,
            "detected": detected,
            "sma50": round(current_sma50, 2),
            "sma200": round(current_sma200, 2),
            "ma_distance": round(ma_distance, 2),
            "strength": strength,
        }

    except Exception as e:
        logger.error(f"Error in MA crossover pattern detection: {str(e)}")
        raise


def _backtest_pattern(df: pd.DataFrame, pattern_indices: List[int]) -> Tuple[int, float]:
    """
    Backtest a pattern to calculate historical success rate.

    Success = Price increased by PROFIT_TARGET% within LOOKFORWARD_DAYS from pattern occurrence.

    Args:
        df (pd.DataFrame): Stock data with 'Close' column.
        pattern_indices (List[int]): List of indices where pattern was detected.

    Returns:
        Tuple[int, float]: (successful_patterns, success_rate %)
    """
    if not pattern_indices:
        return 0, 0.0

    successful_count = 0

    for idx in pattern_indices:
        # Skip if not enough future data
        if idx + LOOKFORWARD_DAYS >= len(df):
            continue

        entry_price = float(df["Close"].iloc[idx])
        future_prices = df["Close"].iloc[idx + 1 : idx + LOOKFORWARD_DAYS + 1]

        # Check if price reached profit target
        max_future_price = float(future_prices.max())
        price_increase = (max_future_price - entry_price) / entry_price

        if price_increase >= PROFIT_TARGET:
            successful_count += 1

    # Calculate success rate
    valid_pattern_count = min(len(pattern_indices), len(df) - LOOKFORWARD_DAYS)
    success_rate = (successful_count / valid_pattern_count * 100) if valid_pattern_count > 0 else 0

    logger.debug(
        f"Backtest Results - Total Patterns: {valid_pattern_count}, "
        f"Successful: {successful_count}, Success Rate: {success_rate:.1f}%"
    )

    return successful_count, round(success_rate, 1)


def calculate_breakout_success_rate(df: pd.DataFrame) -> float:
    """
    Calculate historical success rate for breakout patterns.

    Identifies past breakout patterns and checks if they led to 5%+ gains.

    Args:
        df (pd.DataFrame): Stock data with 'Close', 'High', 'Low', 'Volume' columns.

    Returns:
        float: Success rate percentage (0-100)
    """
    try:
        support_resistance_list = []

        # Calculate support/resistance for rolling windows
        for i in range(20, len(df)):
            window_df = df.iloc[i - 20 : i]
            support, resistance = _calculate_support_resistance(window_df)
            support_resistance_list.append((support, resistance))

        # Find breakout patterns
        breakout_indices = []
        for i in range(len(support_resistance_list)):
            actual_idx = i + 20
            if actual_idx >= len(df):
                break

            current_price = float(df["Close"].iloc[actual_idx])
            support, resistance = support_resistance_list[i]
            breakout_threshold = resistance * (1 + BREAKOUT_THRESHOLD)

            if current_price > breakout_threshold:
                current_volume = float(df["Volume"].iloc[actual_idx])
                avg_volume = float(df["Volume"].iloc[max(0, actual_idx - 20) : actual_idx].mean())

                if current_volume > avg_volume * 1.3:
                    breakout_indices.append(actual_idx)

        # Backtest
        _, success_rate = _backtest_pattern(df, breakout_indices)
        logger.info(f"Breakout pattern success rate: {success_rate}%")
        return success_rate

    except Exception as e:
        logger.warning(f"Error calculating breakout success rate: {str(e)}")
        return 0.0


def calculate_support_success_rate(df: pd.DataFrame) -> float:
    """
    Calculate historical success rate for support bounce patterns.

    Args:
        df (pd.DataFrame): Stock data with 'Close', 'Low' columns.

    Returns:
        float: Success rate percentage (0-100)
    """
    try:
        support_bounce_indices = []

        # Find support bounces
        for i in range(20, len(df)):
            window_df = df.iloc[i - 20 : i]
            support, _ = _calculate_support_resistance(window_df)
            current_price = float(df["Close"].iloc[i])
            recent_low = float(df["Low"].iloc[max(0, i - 5) : i].min())

            support_threshold = support * (1 + SUPPORT_THRESHOLD)

            if current_price > support_threshold and abs(recent_low - support) / support < 0.02:
                support_bounce_indices.append(i)

        # Backtest
        _, success_rate = _backtest_pattern(df, support_bounce_indices)
        logger.info(f"Support pattern success rate: {success_rate}%")
        return success_rate

    except Exception as e:
        logger.warning(f"Error calculating support success rate: {str(e)}")
        return 0.0


def calculate_ma_crossover_success_rate(df: pd.DataFrame) -> float:
    """
    Calculate historical success rate for MA crossover patterns.

    Args:
        df (pd.DataFrame): Stock data with 'Close' column.

    Returns:
        float: Success rate percentage (0-100)
    """
    try:
        sma50, sma200 = _calculate_moving_averages(df)

        crossover_indices = []

        # Find golden crosses and death crosses
        for i in range(1, len(df)):
            if pd.isna(sma50.iloc[i]) or pd.isna(sma200.iloc[i]):
                continue

            prev_sma50 = float(sma50.iloc[i - 1])
            prev_sma200 = float(sma200.iloc[i - 1])
            curr_sma50 = float(sma50.iloc[i])
            curr_sma200 = float(sma200.iloc[i])

            # Golden cross (bullish) - focus on this for success rate
            if prev_sma50 <= prev_sma200 and curr_sma50 > curr_sma200:
                crossover_indices.append(i)

        # Backtest
        _, success_rate = _backtest_pattern(df, crossover_indices)
        logger.info(f"MA Crossover success rate: {success_rate}%")
        return success_rate

    except Exception as e:
        logger.warning(f"Error calculating MA crossover success rate: {str(e)}")
        return 0.0


def _generate_pattern_recommendation(
    patterns_detected: List[Dict], success_rates: Dict
) -> tuple[str, str]:
    """
    Generate buy/sell/hold recommendation based on detected patterns and success rates.

    Logic:
    - BUY: Breakout detected with high success, or multiple bullish patterns
    - SELL: Death Cross detected with low success rate
    - HOLD: Mixed signals or weak patterns
    - WAIT: No clear patterns

    Args:
        patterns_detected (List[Dict]): List of detected patterns
        success_rates (Dict): Success rates for each pattern

    Returns:
        tuple: (recommendation: str, reasoning: str)
    """
    breakout = patterns_detected[0]  # Breakout is first
    support = patterns_detected[1]   # Support is second
    ma_crossover = patterns_detected[2]  # MA Crossover is third

    breakout_detected = breakout.get("detected", False)
    support_detected = support.get("detected", False)
    ma_detected = ma_crossover.get("detected", False)
    ma_type = ma_crossover.get("crossover_type", "None")

    breakout_sr = success_rates.get("breakout", 0)
    support_sr = success_rates.get("support", 0)
    ma_sr = success_rates.get("ma_crossover", 0)
    overall_sr = success_rates.get("overall", 0)

    detected_count = sum(
        1 for p in [breakout_detected, support_detected, ma_detected] if p
    )

    # Rule 1: Strong breakout with good success rate = BUY
    if (
        breakout_detected
        and breakout.get("strength") in ["Strong", "Moderate"]
        and breakout_sr > 50
    ):
        reasoning = (
            f"Strong breakout detected with {breakout_sr}% success rate. "
            f"Price breaking above resistance with volume confirmation. BUY SIGNAL."
        )
        return "BUY", reasoning

    # Rule 2: Golden Cross (SMA50 > SMA200) = STRONG BUY
    if ma_detected and ma_type == "Golden Cross" and ma_sr > 40:
        reasoning = (
            f"Golden Cross detected (bullish crossover) with {ma_sr}% success rate. "
            f"Short-term trend above long-term trend. STRONG BUY SIGNAL."
        )
        return "BUY", reasoning

    # Rule 3: Death Cross (SMA50 < SMA200) with low success = SELL
    if ma_detected and ma_type == "Death Cross":
        reasoning = (
            f"Death Cross detected (bearish crossover). "
            f"Short-term trend below long-term trend. SELL/AVOID SIGNAL."
        )
        return "SELL", reasoning

    # Rule 4: Multiple bullish patterns = HOLD with bullish bias
    if detected_count >= 2 and not (ma_type == "Death Cross"):
        reasoning = (
            f"Multiple patterns detected ({detected_count}). "
            f"Overall success rate: {overall_sr}%. Mixed signals suggest holding. "
            f"Wait for breakout confirmation."
        )
        return "HOLD", reasoning

    # Rule 5: Support bounce with good success = HOLD (wait for breakout)
    if (
        support_detected
        and support.get("strength") in ["Strong", "Moderate"]
        and support_sr > 50
    ):
        reasoning = (
            f"Support bounce detected with {support_sr}% success rate. "
            f"Price holding above support. HOLD and watch for breakout above resistance."
        )
        return "HOLD", reasoning

    # Rule 6: Low success rate overall = WAIT
    if overall_sr < 20:
        reasoning = (
            f"Overall success rate very low ({overall_sr}%). "
            f"Weak pattern setup. WAIT for stronger signals."
        )
        return "WAIT", reasoning

    # Default: Weak signals = HOLD
    reasoning = (
        f"Weak pattern signals detected. "
        f"Overall success rate: {overall_sr}%. "
        f"HOLD position and monitor for breakthrough."
    )
    return "HOLD", reasoning


def analyze_chart_patterns(df: pd.DataFrame, ticker: str) -> Dict:
    """
    Comprehensive chart pattern analysis with detected patterns and success rates.

    Main orchestration function that:
    1. Detects all chart patterns
    2. Calculates historical success rates via backtesting
    3. Generates buy/sell/hold recommendation
    4. Returns structured results

    Args:
        df (pd.DataFrame): Stock data with all required columns.
        ticker (str): Stock ticker symbol.

    Returns:
        Dict: Comprehensive pattern analysis with structure:
            {
                "stock": str,
                "patterns_detected": List[Dict],
                "success_rates": {
                    "breakout": float,
                    "support": float,
                    "ma_crossover": float,
                    "overall": float
                },
                "overall_pattern_strength": str,
                "recommendation": str,
                "recommendation_reasoning": str
            }

    Example:
        >>> from stock_data_fetcher import get_stock_data
        >>> from chart_patterns import analyze_chart_patterns
        >>> df = get_stock_data('RELIANCE.NS')
        >>> analysis = analyze_chart_patterns(df, 'RELIANCE.NS')
        >>> print(analysis['recommendation'])
    """
    logger.info(f"Starting chart pattern analysis for {ticker}")

    try:
        # Detect patterns
        breakout = detect_breakout_pattern(df)
        support = detect_support_pattern(df)
        ma_crossover = detect_ma_crossover_pattern(df)

        patterns_detected = [breakout, support, ma_crossover]

        # Calculate success rates via backtesting
        breakout_success = calculate_breakout_success_rate(df)
        support_success = calculate_support_success_rate(df)
        ma_success = calculate_ma_crossover_success_rate(df)

        # Calculate overall success rate (average of detected patterns)
        detected_patterns = [p for p in patterns_detected if p.get("detected", False)]
        if detected_patterns:
            overall_success = (breakout_success + support_success + ma_success) / 3
        else:
            overall_success = 0.0

        success_rates = {
            "breakout": round(breakout_success, 1),
            "support": round(support_success, 1),
            "ma_crossover": round(ma_success, 1),
            "overall": round(overall_success, 1),
        }

        # Determine overall pattern strength
        detected_count = sum(1 for p in patterns_detected if p.get("detected", False))
        if detected_count >= 2 and overall_success > 60:
            overall_strength = "Strong"
        elif detected_count >= 1 and overall_success > 40:
            overall_strength = "Moderate"
        else:
            overall_strength = "Weak"

        # Generate recommendation
        recommendation, reasoning = _generate_pattern_recommendation(
            patterns_detected, success_rates
        )

        result = {
            "stock": ticker,
            "patterns_detected": patterns_detected,
            "success_rates": success_rates,
            "overall_pattern_strength": overall_strength,
            "pattern_count": detected_count,
            "recommendation": recommendation,
            "recommendation_reasoning": reasoning,
        }

        logger.info(
            f"Chart pattern analysis completed for {ticker}: {overall_strength} "
            f"(Recommendation: {recommendation})"
        )
        return result

    except Exception as e:
        logger.error(f"Error in chart pattern analysis: {str(e)}")
        raise


def print_chart_patterns_report(analysis: Dict) -> None:
    """
    Print a formatted report of chart pattern analysis and success rates.

    Args:
        analysis (Dict): Analysis result from analyze_chart_patterns().

    Example:
        >>> analysis = analyze_chart_patterns(df, 'RELIANCE.NS')
        >>> print_chart_patterns_report(analysis)
    """
    print("\n" + "=" * 80)
    print("CHART PATTERN INTELLIGENCE - PATTERN ANALYSIS REPORT")
    print("=" * 80)

    print(f"\nStock: {analysis['stock']}")
    print(f"Overall Pattern Strength: {analysis['overall_pattern_strength']}")
    print(f"Patterns Detected: {analysis['pattern_count']}")

    # Recommendation Section (HIGHLIGHTED)
    print("\n" + "=" * 80)
    recommendation = analysis.get("recommendation", "HOLD")
    reasoning = analysis.get("recommendation_reasoning", "No analysis available")
    
    # Color code recommendations
    if recommendation == "BUY":
        rec_display = "🟢 BUY"
    elif recommendation == "SELL":
        rec_display = "🔴 SELL / AVOID"
    elif recommendation == "WAIT":
        rec_display = "🟡 WAIT FOR SIGNALS"
    else:
        rec_display = "🟠 HOLD"
    
    print(f"RECOMMENDATION: {rec_display}")
    print("=" * 80)
    print(f"Reasoning: {reasoning}\n")

    # Success Rates
    print(f"Historical Success Rates (Backtested):")
    print("-" * 80)
    sr = analysis["success_rates"]
    print(f"  Breakout Pattern Success Rate:      {sr['breakout']:>6.1f}%")
    print(f"  Support Pattern Success Rate:       {sr['support']:>6.1f}%")
    print(f"  MA Crossover Success Rate:          {sr['ma_crossover']:>6.1f}%")
    print(f"  Overall Success Rate:               {sr['overall']:>6.1f}%")

    # Pattern Details
    print(f"\nDetected Patterns:")
    print("-" * 80)
    for pattern in analysis["patterns_detected"]:
        if pattern.get("detected", False):
            name = pattern["pattern_name"]
            strength = pattern.get("strength", "None")
            print(f"  ✓ {name:.<40} {strength}")
        else:
            name = pattern["pattern_name"]
            print(f"  ✗ {name:.<40} Not detected")

    # Pattern Details
    print(f"\nDetailed Pattern Information:")
    print("-" * 80)
    for pattern in analysis["patterns_detected"]:
        print(f"\n{pattern['pattern_name']}:")
        for key, value in pattern.items():
            if key not in ["pattern_name"]:
                print(f"  {key}: {value}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        from stock_data_fetcher import get_stock_data

        print("=" * 80)
        print("Chart Pattern Intelligence - Example Usage")
        print("=" * 80)

        # Fetch data
        print("\nFetching stock data...")
        df = get_stock_data("RELIANCE.NS")

        # Analyze patterns
        print("Analyzing chart patterns...")
        analysis = analyze_chart_patterns(df, "RELIANCE.NS")

        # Print report
        print_chart_patterns_report(analysis)

    except Exception as e:
        logger.error(f"Error in example: {str(e)}")
        print(f"Error: {str(e)}")
