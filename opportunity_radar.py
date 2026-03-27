"""
Opportunity Radar System

Combines detected trading signals to identify investment opportunities.
Generates structured opportunity classifications with confidence scores.

Opportunity Classifications:
- Strong: Breakout + Volume Spike (high conviction)
- Moderate: Price Surge + Uptrend (solid opportunity)
- Weak: Single signal triggered (limited confirmation)
- None: No signals triggered (pass)
"""

import json
import logging
from typing import Dict, List, Optional

import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Opportunity Configuration
OPPORTUNITY_CONFIG = {
    "Strong": {
        "confidence_min": 70,
        "confidence_max": 80,
        "description": "High conviction opportunity",
    },
    "Moderate": {
        "confidence_min": 50,
        "confidence_max": 70,
        "description": "Solid opportunity with confirmation",
    },
    "Weak": {
        "confidence_min": 30,
        "confidence_max": 50,
        "description": "Limited signal confirmation",
    },
    "None": {
        "confidence_min": 0,
        "confidence_max": 20,
        "description": "Insufficient signals",
    },
}


def _classify_opportunity(signals: List[Dict]) -> tuple[str, List[str]]:
    """
    Classify opportunity level based on signal combination logic.

    Classification Rules:
    - Strong: breakout AND volume spike both triggered
    - Moderate: (price surge AND uptrend) OR (3+ signals triggered)
    - Weak: 1-2 signals triggered (excluding above patterns)
    - None: no signals triggered

    Args:
        signals (List[Dict]): List of signal dictionaries from detect_signals().

    Returns:
        tuple: (opportunity_level: str, triggered_signals: List[str])
    """
    # Extract triggered signals
    triggered = [s["signal_name"] for s in signals if s["triggered"]]
    triggered_count = len(triggered)

    # No signals triggered
    if triggered_count == 0:
        return "None", []

    # Check for Strong pattern: Breakout + Volume Spike
    has_breakout = "Breakout" in triggered
    has_volume_spike = "Volume Spike" in triggered

    if has_breakout and has_volume_spike:
        logger.debug("Opportunity classified as STRONG (Breakout + Volume Spike)")
        return "Strong", triggered

    # Check for Moderate pattern: Price Surge + Uptrend
    has_price_surge = "Price Surge" in triggered
    has_uptrend = "Uptrend" in triggered

    if (has_price_surge and has_uptrend) or (triggered_count >= 3):
        logger.debug(
            f"Opportunity classified as MODERATE (Multiple confirmations: {triggered})"
        )
        return "Moderate", triggered

    # Default to Weak for 1-2 signals without strong patterns
    logger.debug(f"Opportunity classified as WEAK ({triggered_count} signal(s))")
    return "Weak", triggered


def _generate_summary(
    opportunity_level: str, signals: List[Dict], ticker: str
) -> str:
    """
    Generate a concise, human-readable summary of the opportunity.

    Args:
        opportunity_level (str): Opportunity classification (Strong/Moderate/Weak/None).
        signals (List[Dict]): List of signal dictionaries.
        ticker (str): Stock ticker symbol.

    Returns:
        str: 1-2 line summary explanation.
    """
    triggered_signals = [s for s in signals if s["triggered"]]

    if opportunity_level == "Strong":
        strength_indicators = []
        for sig in triggered_signals:
            if sig["signal_name"] == "Breakout":
                strength_indicators.append(
                    f"price broke through the {sig['lookback_days']}-day resistance level"
                )
            elif sig["signal_name"] == "Volume Spike":
                strength_indicators.append(f"trading volume surged {sig['ratio']:.1f}x average")

        summary_details = ", ".join(strength_indicators)
        summary = f"High conviction breakout: {summary_details}. Strong buy signal with institutional volume backing."
        return summary

    elif opportunity_level == "Moderate":
        if len(triggered_signals) >= 2:
            trend_indicators = []
            for sig in triggered_signals[:2]:
                if sig["signal_name"] == "Price Surge":
                    trend_indicators.append(f"price up {sig.get('price_change_percent', '?')}%")
                elif sig["signal_name"] == "Uptrend":
                    trend_indicators.append(f"{sig.get('consecutive_up_days', '?')}-day uptrend")
            
            if trend_indicators:
                return f"Solid momentum confirmed: {', '.join(trend_indicators)}. Multiple signals aligned for continued upside."
            return f"Multiple confirmations detected. Solid opportunity with good technical alignment."
        return "Solid momentum building with multiple technical confirmations. Consider entry on pullback."

    elif opportunity_level == "Weak":
        if triggered_signals:
            signal = triggered_signals[0]
            signal_name = signal["signal_name"]
            
            if signal_name == "Uptrend":
                days = signal.get("consecutive_up_days", "?")
                return f"Stock shows early upward momentum with a weak {days}-day uptrend. Additional confirmation needed before strong entry."
            elif signal_name == "Volume Spike":
                ratio = signal.get("ratio", "?")
                return f"Isolated volume spike detected ({ratio}x) but lacks price confirmation. Monitor for follow-through."
            elif signal_name == "Price Surge":
                return f"Price gained {signal.get('price_change_percent', '?')}% but without sustained trend confirmation. Wait for stronger pattern."
            elif signal_name == "Breakout":
                return f"Early breakout attempt but volume not yet confirming. Watch for sustained move above resistance."
            
            return f"Single early signal ({signal_name}) detected. Limited confirmation—await stronger confirmation."
        return "Awaiting stronger signals for entry. No clear opportunity at this time."

    else:  # None
        return f"No trading signals triggered for {ticker}. Monitor for emerging technical patterns."


def _calculate_confidence_score(
    opportunity_level: str, signals: List[Dict]
) -> float:
    """
    Calculate confidence score based on opportunity level and signal strength.

    For each opportunity level, applies a base confidence and adjusts based on
    the strength of underlying signals. Weak signals with strong underlying values
    get boosted; weak signals with weak values stay lower.

    Args:
        opportunity_level (str): Classified opportunity level.
        signals (List[Dict]): List of signal dictionaries with strength info.

    Returns:
        float: Confidence score between 0-100.
    """
    config = OPPORTUNITY_CONFIG.get(opportunity_level, OPPORTUNITY_CONFIG["None"])
    base_min = config["confidence_min"]
    base_max = config["confidence_max"]

    # Use midpoint of range as base confidence
    base_confidence = (base_min + base_max) / 2

    # Apply signal strength bonuses
    triggered_signals = [s for s in signals if s["triggered"]]
    signal_strength_bonus = 0
    signal_strength_penalty = 0

    for signal in triggered_signals:
        strength = signal.get("strength", "None")
        if strength == "Strong":
            signal_strength_bonus += 5  # +5% for strong signals
        elif strength == "Moderate":
            signal_strength_bonus += 2  # +2% for moderate signals
        elif strength == "Weak":
            # For weak signals with weak strength, apply slight penalty
            signal_strength_penalty -= 3  # -3% for weak signals

    # For Weak opportunity level, refine based on signal quality
    if opportunity_level == "Weak" and triggered_signals:
        signal = triggered_signals[0]
        strength = signal.get("strength", "None")
        
        # If weak signal but underlying value is strong, boost confidence
        if strength == "Strong":
            signal_strength_bonus += 8  # Extra boost for strong underlying value
        elif strength == "Moderate":
            signal_strength_bonus += 5  # Moderate boost

    # Cap the final confidence between min and max range
    final_confidence = base_confidence + signal_strength_bonus + signal_strength_penalty
    final_confidence = min(final_confidence, base_max)
    final_confidence = max(final_confidence, base_min)

    logger.debug(
        f"Confidence calculated: base={base_confidence:.1f}%, "
        f"bonus={signal_strength_bonus}%, penalty={signal_strength_penalty}%, "
        f"final={final_confidence:.1f}%"
    )

    return round(final_confidence, 1)


def generate_opportunity(
    df: pd.DataFrame, signals: List[Dict], ticker: str
) -> Dict:
    """
    Generate structured opportunity classification from trading signals.

    Main function that combines signal analysis, classifies opportunity level,
    generates summary explanation, and calculates confidence score.

    Args:
        df (pd.DataFrame): Stock data (used for context, validation).
        signals (List[Dict]): List of signal dictionaries from detect_signals().
        ticker (str): Stock ticker symbol (e.g., 'RELIANCE.NS', 'AAPL').

    Returns:
        Dict: Opportunity record with structure:
            {
                "stock": str,
                "date": str (most recent trading date),
                "opportunity_level": str,
                "confidence": float (0-100),
                "signals_triggered": List[str],
                "signal_details": List[Dict],
                "summary": str,
                "action": str (BUY/HOLD/PASS)
            }

    Example:
        >>> from stock_data_fetcher import get_stock_data
        >>> from signal_detector import detect_signals
        >>> from opportunity_radar import generate_opportunity
        >>> 
        >>> df = get_stock_data('RELIANCE.NS')
        >>> signals = detect_signals(df)
        >>> opp = generate_opportunity(df, signals, 'RELIANCE.NS')
        >>> print(opp['opportunity_level'], opp['confidence'])
    """
    logger.info(f"Generating opportunity for {ticker}")

    try:
        # Classify opportunity and extract triggered signals
        opportunity_level, triggered_signal_names = _classify_opportunity(signals)

        # Generate summary explanation
        summary = _generate_summary(opportunity_level, signals, ticker)

        # Calculate confidence score
        confidence = _calculate_confidence_score(opportunity_level, signals)

        # Determine action
        if opportunity_level == "Strong":
            action = "BUY"
        elif opportunity_level == "Moderate":
            action = "BUY"
        elif opportunity_level == "Weak":
            action = "HOLD"
        else:
            action = "PASS"

        # Get most recent date from DataFrame
        most_recent_date = str(df.index[-1].date()) if len(df) > 0 else "Unknown"

        # Build signal details with strength info and reasoning
        signal_details = []
        for s in signals:
            detail = {
                "name": s["signal_name"],
                "triggered": s["triggered"],
                "strength": s.get("strength", "N/A"),
            }
            
            # Add reasoning/explanation for each signal
            if s["triggered"]:
                if s["signal_name"] == "Volume Spike":
                    detail["reasoning"] = f"Current volume {s['ratio']:.1f}x the average (10-day)"
                elif s["signal_name"] == "Price Surge":
                    detail["reasoning"] = f"Price increased {s['price_change_percent']:.2f}% over 3 days"
                elif s["signal_name"] == "Uptrend":
                    detail["reasoning"] = f"{s['consecutive_up_days']} consecutive days of price increases"
                elif s["signal_name"] == "Breakout":
                    detail["reasoning"] = f"Price at {s['current_price']} exceeds 10-day high of {s['max_price']}"
            else:
                detail["reasoning"] = "Not triggered"
            
            signal_details.append(detail)

        # Construct opportunity record
        opportunity = {
            "stock": ticker,
            "date": most_recent_date,
            "opportunity_level": opportunity_level,
            "confidence": confidence,
            "signals_triggered": triggered_signal_names,
            "signal_details": signal_details,
            "summary": summary,
            "action": action,
        }

        logger.info(
            f"Opportunity generated: {opportunity_level} "
            f"(confidence: {confidence}%, action: {action})"
        )

        return opportunity

    except Exception as e:
        logger.error(f"Error generating opportunity for {ticker}: {str(e)}")
        raise


def print_opportunity_report(opportunity: Dict) -> None:
    """
    Print a formatted, visual report of the opportunity analysis.

    Args:
        opportunity (Dict): Opportunity record from generate_opportunity().

    Example:
        >>> opp = generate_opportunity(df, signals, 'RELIANCE.NS')
        >>> print_opportunity_report(opp)
    """
    print("\n" + "=" * 80)
    print("OPPORTUNITY RADAR - INVESTMENT OPPORTUNITY REPORT")
    print("=" * 80)

    # Stock and date
    print(f"\nStock Symbol: {opportunity['stock']:.<50} {opportunity['date']}")

    # Opportunity Level and Action
    level = opportunity["opportunity_level"]
    confidence = opportunity["confidence"]
    action = opportunity["action"]

    # Color coding (via text indicators)
    if level == "Strong":
        level_indicator = "🟢 STRONG OPPORTUNITY"
    elif level == "Moderate":
        level_indicator = "🟡 MODERATE OPPORTUNITY"
    elif level == "Weak":
        level_indicator = "🔵 WEAK SIGNAL"
    else:
        level_indicator = "⚫ NO OPPORTUNITY"

    print(f"\n{level_indicator}")
    print(f"Confidence Score: {confidence}%")
    print(f"Recommended Action: {action}")

    # Triggered Signals
    print(f"\nTriggered Signals ({len(opportunity['signals_triggered'])}):")
    if opportunity["signals_triggered"]:
        for signal_name in opportunity["signals_triggered"]:
            print(f"  ✓ {signal_name}")
    else:
        print("  (None)")

    # Signal Details Table
    print(f"\nSignal Analysis:")
    print("-" * 80)
    for detail in opportunity["signal_details"]:
        status_icon = "✓" if detail["triggered"] else "✗"
        strength = detail["strength"] if detail["triggered"] else "-"
        reasoning = detail.get("reasoning", "")
        print(
            f"  {status_icon} {detail['name']:.<25} "
            f"Strength: {strength:.<10}"
        )
        if reasoning:
            print(f"     └─ {reasoning}")

    # Summary
    print(f"\nSummary:")
    print(f"  {opportunity['summary']}")

    print("\n" + "=" * 80)


def export_opportunity_json(opportunity: Dict, filename: str = None) -> str:
    """
    Export opportunity record as JSON string or file.

    Args:
        opportunity (Dict): Opportunity record from generate_opportunity().
        filename (str, optional): File path to save JSON. If None, returns string.

    Returns:
        str: JSON string representation of opportunity.

    Example:
        >>> opp = generate_opportunity(df, signals, 'RELIANCE.NS')
        >>> json_str = export_opportunity_json(opp)
        >>> export_opportunity_json(opp, 'opportunity.json')
    """
    json_str = json.dumps(opportunity, indent=2)

    if filename:
        try:
            with open(filename, "w") as f:
                f.write(json_str)
            logger.info(f"Opportunity exported to {filename}")
        except Exception as e:
            logger.error(f"Error exporting opportunity to file: {str(e)}")

    return json_str


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    try:
        # Import required modules
        from signal_detector import detect_signals
        from stock_data_fetcher import get_stock_data

        print("=" * 80)
        print("OPPORTUNITY RADAR SYSTEM - COMPLETE WORKFLOW DEMONSTRATION")
        print("=" * 80)

        # ====== Example 1: RELIANCE.NS ======
        print("\n[Example 1] Analyzing RELIANCE.NS")
        print("-" * 80)

        # Step 1: Fetch stock data
        print("1. Fetching 6 months of historical data...")
        reliance_df = get_stock_data("RELIANCE.NS")
        print(f"   ✓ Fetched {len(reliance_df)} trading days")

        # Step 2: Detect signals
        print("2. Detecting trading signals...")
        reliance_signals = detect_signals(reliance_df)
        triggered = sum(1 for s in reliance_signals if s["triggered"])
        print(f"   ✓ Found {triggered} triggered signal(s)")

        # Step 3: Generate opportunity
        print("3. Generating opportunity classification...")
        reliance_opp = generate_opportunity(reliance_df, reliance_signals, "RELIANCE.NS")
        print(f"   ✓ Opportunity level: {reliance_opp['opportunity_level']}")

        # Display report
        print_opportunity_report(reliance_opp)

        # Export as JSON
        json_reliance = export_opportunity_json(reliance_opp)
        print("\nJSON Export (RELIANCE.NS):")
        print(json_reliance)

        # ====== Example 2: APPLE (AAPL) ======
        print("\n" + "=" * 80)
        print("\n[Example 2] Analyzing APPLE (AAPL)")
        print("-" * 80)

        # Step 1: Fetch stock data
        print("1. Fetching 6 months of historical data...")
        apple_df = get_stock_data("AAPL")
        print(f"   ✓ Fetched {len(apple_df)} trading days")

        # Step 2: Detect signals
        print("2. Detecting trading signals...")
        apple_signals = detect_signals(apple_df)
        triggered = sum(1 for s in apple_signals if s["triggered"])
        print(f"   ✓ Found {triggered} triggered signal(s)")

        # Step 3: Generate opportunity
        print("3. Generating opportunity classification...")
        apple_opp = generate_opportunity(apple_df, apple_signals, "AAPL")
        print(f"   ✓ Opportunity level: {apple_opp['opportunity_level']}")

        # Display report
        print_opportunity_report(apple_opp)

        # ====== Example 3: Comparative Summary ======
        print("\n" + "=" * 80)
        print("\n[Example 3] Comparative Opportunity Summary")
        print("-" * 80)
        print(f"\n{'Stock':<15} {'Opportunity':<15} {'Confidence':<12} {'Action':<10}")
        print("-" * 80)
        print(
            f"{reliance_opp['stock']:<15} "
            f"{reliance_opp['opportunity_level']:<15} "
            f"{reliance_opp['confidence']}%{'':<9} "
            f"{reliance_opp['action']:<10}"
        )
        print(
            f"{apple_opp['stock']:<15} "
            f"{apple_opp['opportunity_level']:<15} "
            f"{apple_opp['confidence']}%{'':<9} "
            f"{apple_opp['action']:<10}"
        )

        # ====== Example 4: High-Confidence Opportunities ======
        print("\n" + "=" * 80)
        print("\n[Example 4] High-Confidence Opportunities (>65%)")
        print("-" * 80)

        opportunities = [reliance_opp, apple_opp]
        high_confidence = [opp for opp in opportunities if opp["confidence"] > 65]

        if high_confidence:
            print(f"\nFound {len(high_confidence)} high-confidence opportunity/opportunities:\n")
            for opp in high_confidence:
                print(f"  ✓ {opp['stock']:15} | Level: {opp['opportunity_level']:10} | {opp['summary']}")
        else:
            print("\nNo high-confidence opportunities found at this time.")

    except Exception as e:
        logger.error(f"Error in opportunity radar example: {str(e)}")
        print(f"Error: {str(e)}")
