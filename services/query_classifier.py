"""
Query Classifier & Router

Intelligent query classification system for financial AI.
- Classifies user messages into stock | comparison | portfolio | general
- Extracts stock tickers automatically
- Returns clean JSON routing data

Classes:
- QueryType: Type constants

Functions:
- route_query(): Main router returning JSON (matches specification)
- classify_query(): Legacy wrapper for backward compatibility
"""

import re
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


class QueryType:
    """Query type constants."""
    STOCK = "stock"
    COMPARISON = "comparison"
    PORTFOLIO = "portfolio"
    GENERAL = "general"


# ============================================================================
# SIMPLE CONTEXT AWARENESS - Remember last stock mentioned
# ============================================================================
user_context = {
    "last_stock": None
}


def route_query(message: str) -> Dict:
    """
    Route user query to appropriate handler type.
    
    Spec-compliant router returning clean JSON format:
    {
        "type": "stock | comparison | portfolio | general",
        "tickers": ["AAPL", "MSFT"]  # Empty list if not applicable
    }
    
    Classification Rules:
    1. Portfolio queries → type: "portfolio"
    2. General/educational questions → type: "general"
    3. Multiple tickers or comparison keywords → type: "comparison"
    4. Single ticker → type: "stock"
    
    Args:
        message: User's input message
        
    Returns:
        Dict with "type" and "tickers" keys
        
    Examples:
        route_query("Should I buy AAPL?")
        → {"type": "stock", "tickers": ["AAPL"]}
        
        route_query("AAPL vs MSFT")
        → {"type": "comparison", "tickers": ["AAPL", "MSFT"]}
        
        route_query("Is my portfolio good?")
        → {"type": "portfolio", "tickers": []}
        
        route_query("What is RSI?")
        → {"type": "general", "tickers": []}
    """
    
    message_lower = message.lower()
    
    # Rule 1: Portfolio detection (with multi-intent handling)
    portfolio_keywords = [
        "my portfolio", "portfolio", "allocation", "diversif",
        "rebalance", "my stocks", "my holdings", "my investment",
        "asset allocation", "risk profile"
    ]
    
    # Check if portfolio query exists
    is_portfolio_query = any(keyword in message_lower for keyword in portfolio_keywords)
    
    if is_portfolio_query:
        # Extract tickers from portfolio question (e.g., "Is my portfolio good with AAPL?")
        tickers = extract_all_tickers(message)
        
        # Multi-intent handling: If portfolio + stock present, combine them
        if tickers:
            # Store first ticker in context for future reference
            user_context["last_stock"] = tickers[0]
            logger.info(f"✓ Query routed: PORTFOLIO with stocks {tickers}")
            return {
                "type": QueryType.PORTFOLIO,
                "tickers": tickers  # Include tickers for context
            }
        
        logger.info("✓ Query routed: PORTFOLIO")
        return {
            "type": QueryType.PORTFOLIO,
            "tickers": []
        }
    
    # Rule 2: General knowledge questions (check BEFORE ticker extraction!)
    # This prevents technical indicators like RSI, MACD from being treated as tickers
    general_keywords = [
        "what is", "explain", "how do", "tell me about",
        "what are", "can you", "how can",
        "breakout", "macd", "rsi", "support", "resistance",
        "dividend", "pe ratio", "market cap", "volatility",
        "bull", "bear", "trend", "signal", "momentum",
        "strategy", "technique", "method", "indicator",
        "earnings", "ipo", "ipo", "sector", "industry",
        "fundamental", "technical", "analysis"
    ]
    
    if any(keyword in message_lower for keyword in general_keywords):
        logger.info("✓ Query routed: GENERAL (knowledge question)")
        return {
            "type": QueryType.GENERAL,
            "tickers": []
        }
    
    # Rule 3: Extract tickers from message (after checking general keywords)
    tickers_in_message = extract_all_tickers(message)
    
    # Rule 4: Comparison detection - multiple tickers or comparison keywords
    # IMPORTANT: Only check comparison if tickers were EXPLICITLY mentioned in message
    comparison_keywords = ["vs", "versus", "better", "compare", "which", "prefer", "or"]
    has_comparison_keyword = any(keyword in message_lower for keyword in comparison_keywords)
    
    if len(tickers_in_message) >= 2 or (has_comparison_keyword and len(tickers_in_message) >= 1):
        # Store first ticker in context
        if tickers_in_message:
            user_context["last_stock"] = tickers_in_message[0]
        logger.info(f"✓ Query routed: COMPARISON ({', '.join(tickers_in_message[:2])})")
        return {
            "type": QueryType.COMPARISON,
            "tickers": tickers_in_message[:2]  # Compare first 2 only
        }
    
    # Rule 5: Single stock from message
    if len(tickers_in_message) == 1:
        # Store in context for future reference
        user_context["last_stock"] = tickers_in_message[0]
        logger.info(f"✓ Query routed: STOCK ({tickers_in_message[0]})")
        return {
            "type": QueryType.STOCK,
            "tickers": tickers_in_message
        }
    
    # CONTEXT AWARENESS: If no ticker found in message, use last_stock
    # This is applied AFTER comparison check to ensure context doesn't trigger comparison logic
    if not tickers_in_message and user_context["last_stock"]:
        logger.info(f"📝 Using context: last_stock = {user_context['last_stock']}")
        return {
            "type": QueryType.STOCK,
            "tickers": [user_context["last_stock"]]
        }
    
    # Default: General if unclear
    logger.info("✓ Query routed: GENERAL (default)")
    return {
        "type": QueryType.GENERAL,
        "tickers": []
    }


def classify_query(message: str) -> Tuple[str, Dict]:
    """
    Legacy wrapper for route_query() - maintains backward compatibility.
    
    Converts clean JSON format to legacy tuple format:
    (query_type, extracted_data_dict)
    
    Args:
        message: User's message
        
    Returns:
        Tuple of (query_type, extracted_data)
    """
    
    # Use the new router
    route_result = route_query(message)
    query_type = route_result["type"]
    tickers = route_result["tickers"]
    
    # Convert back to legacy format for backward compatibility
    message_clean = message.strip()
    message_lower = message.lower()
    
    if query_type == QueryType.STOCK:
        return query_type, {
            "ticker": tickers[0] if tickers else None,
            "is_stock_question": True,
            "original_message": message_clean
        }
    elif query_type == QueryType.COMPARISON:
        return query_type, {
            "tickers": tickers,
            "is_comparison": True,
            "original_message": message_clean
        }
    elif query_type == QueryType.PORTFOLIO:
        portfolio_keywords = [
            "my portfolio", "portfolio", "allocation", "diversif",
            "rebalance", "my stocks", "my holdings", "my investment",
            "asset allocation", "risk profile"
        ]
        return query_type, {
            "is_portfolio_question": True,
            "keywords": [k for k in portfolio_keywords if k in message_lower],
            "tickers": tickers  # Include extracted tickers for multi-intent
        }
    else:  # GENERAL
        return query_type, {
            "question": message_clean,
            "is_general": True
        }


def extract_all_tickers(message: str) -> List[str]:
    """
    Extract all stock tickers from message (case-insensitive).
    
    Supports formats:
    - US tickers: AAPL, aapl, Aapl
    - Indian tickers: RELIANCE.NS, reliance.ns, Reliance.NS
    
    Args:
        message: User message
        
    Returns:
        List of unique tickers found in UPPERCASE (empty if none)
    """
    # Pattern for tickers: AAPL, RELIANCE.NS, TCS.NS, etc. (CASE-INSENSITIVE)
    # Matches: 1-5 char tickers OR longer with suffix like .NS
    ticker_pattern = r'\b([a-zA-Z]{1,5})(?:\.([a-zA-Z]{2,3}))?\b|\b([a-zA-Z]{6,9})\.([a-zA-Z]{2,3})\b'
    matches = re.findall(ticker_pattern, message, re.IGNORECASE)
    
    # Common English words to filter out (expanded list)
    common_words = {
        'A', 'I', 'IT', 'IF', 'OR', 'AND', 'THE', 'IS', 'AT', 'BY', 'FOR',
        'ON', 'BE', 'IN', 'AS', 'OF', 'TO', 'US', 'UP', 'NO', 'SO', 'DO',
        'GO', 'OK', 'WE', 'ME', 'MY', 'AM', 'AN', 'ARE', 'BUY', 'SELL',
        'GET', 'BET', 'YES', 'NO', 'CAN', 'MAY', 'SAY', 'DID', 'BAD', 'HAD',
        'HOW', 'TWO', 'WAY', 'ANY', 'ALL', 'YOU', 'HER', 'HIM', 'HIS', 'OUR',
        'OUT', 'TOP', 'ADD', 'BOX', 'DAY', 'END', 'NEW', 'OLD', 'OWN', 'RUN',
        'SHOULD', 'WOULD', 'COULD', 'THAT', 'WHAT', 'WHICH', 'THIS', 'HAVE',
        'ABOUT', 'MAKE', 'TAKE', 'GOOD', 'IDEA', 'THINK', 'LOOK', 'COME',
        'JUST', 'VERY', 'EVEN', 'ONLY', 'ALSO', 'BACK', 'OVER', 'SUCH',
        'WANT', 'TELL', 'SHOW', 'KEEP', 'TURN', 'WORK', 'CALL', 'HELP',
        'LIVE', 'NEED', 'FEEL', 'KNOW', 'GIVE', 'FIND', 'MAKE', 'SEEM',
        'LIKE', 'LOVE', 'HATE', 'FEAR', 'CARE', 'HOPE', 'WISH', 'FIND',
        'WITH'  # CRITICAL: Prevent "with" from being detected as ticker
    }
    
    tickers = []
    seen = set()  # Track seen tickers (normalized)
    
    for match in matches:
        # Handle both pattern matches
        ticker = None
        
        if match[0]:  # Group 1: short ticker (1-5 chars) with optional suffix
            if match[1]:  # Has suffix like .NS or .BO
                ticker = f"{match[0]}.{match[1]}".upper()
                base = match[0].upper()
            else:
                ticker = match[0].upper()
                base = match[0].upper()
        elif match[2]:  # Group 3: long ticker (6-9 chars) with required suffix
            ticker = f"{match[2]}.{match[3]}".upper()
            base = match[2].upper()
        
        # Filter out common words and duplicates
        # CRITICAL: Also filter single-letter tickers (e.g., 'S' should not be treated as valid ticker)
        if ticker and ticker not in common_words and ticker not in seen and len(base) > 1:
            tickers.append(ticker)
            seen.add(ticker)
    
    logger.debug(f"Extracted tickers from '{message}': {tickers}")
    return tickers


def get_query_context(query_type: str, data: Dict) -> str:
    """
    Get human-readable context for logging/debugging.
    
    Args:
        query_type: Type of query (stock | comparison | portfolio | general)
        data: Extracted data dict
        
    Returns:
        Human-readable context string
    """
    if query_type == QueryType.STOCK:
        ticker = data.get('ticker')
        return f"Stock analysis for {ticker}"
    elif query_type == QueryType.COMPARISON:
        tickers = data.get('tickers', [])
        if len(tickers) >= 2:
            return f"Comparison between {' and '.join(tickers)}"
        return "Comparison query"
    elif query_type == QueryType.PORTFOLIO:
        return "Portfolio analysis"
    else:  # GENERAL
        return data.get('question', 'General knowledge question')


# ============================================================================
# CONTEXT MANAGEMENT UTILITIES
# ============================================================================

def get_last_stock() -> Optional[str]:
    """Get the last stock mentioned by user."""
    return user_context.get("last_stock")


def set_last_stock(ticker: str) -> None:
    """Manually set the last stock."""
    user_context["last_stock"] = ticker
    logger.info(f"📝 Context updated: last_stock = {ticker}")


def reset_context() -> None:
    """Clear all context (e.g., when starting new session)."""
    user_context["last_stock"] = None
    logger.info("📝 Context cleared")
