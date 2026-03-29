"""
Ticker Extraction Service

Extracts stock ticker symbols from natural language questions.
"""

import re
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


def extract_tickers(question: str) -> List[str]:
    """
    Extract stock ticker symbols from question.
    
    Supports:
    - US stocks: AAPL, MSFT, TSLA, GOOGL, etc.
    - Indian stocks: RELIANCE.NS, TCS.NS, INFY.NS, etc.
    - Other formats: ASIANPAINT.BO, etc.
    
    Args:
        question: User's question
        
    Returns:
        List of extracted tickers (uppercase)
    """
    
    if not question:
        return []
    
    # Pattern for tickers: AAPL, RELIANCE.NS, TCS.NS, etc.
    # Matches: 1-9 uppercase letters, optionally followed by dot and 1-3 uppercase letters
    ticker_pattern = r'\b([A-Z]{1,9})(?:\.([A-Z]{1,3}))?\b'
    
    matches = re.findall(ticker_pattern, question)
    tickers = []
    
    for match in matches:
        if match[1]:  # Has suffix like .NS or .BO
            ticker = f"{match[0]}.{match[1]}"
            base = match[0]
        else:
            ticker = match[0]
            base = match[0]
        
        # Filter out common words that look like tickers
        if is_common_word(ticker):
            continue
            
        # CRITICAL: Validate ticker - must be 2-5 chars (not single letter like "S")
        if not (2 <= len(base) <= 5):
            continue
            
        tickers.append(ticker)
    
    return list(set(tickers))  # Remove duplicates


def is_common_word(word: str) -> bool:
    """
    Filter out common English words that match ticker pattern.
    
    Args:
        word: Potential ticker
        
    Returns:
        True if word is common English word, False otherwise
    """
    
    common_words = {
        'A', 'I', 'IT', 'IF', 'OR', 'AND', 'THE', 'IS', 'AT', 'BY', 'FOR',
        'ON', 'BE', 'IN', 'AS', 'OF', 'TO', 'US', 'UP', 'NO', 'SO', 'DO',
        'GO', 'OK', 'WE', 'ME', 'MY', 'AM', 'AN', 'ARE', 'BUY', 'SELL',
        'GET', 'BET', 'YES', 'NO', 'CAN', 'MAY', 'SAY', 'DID', 'BAD', 'HAD',
        'HOW', 'TWO', 'WAY', 'ANY', 'ALL', 'YOU', 'HER', 'HIM', 'HIS', 'OUR',
        'OUT', 'TOP', 'ADD', 'BOX', 'DAY', 'END', 'NEW', 'OLD', 'OWN', 'RUN'
    }
    
    return word.upper() in common_words


def get_primary_ticker(question: str) -> Optional[str]:
    """
    Extract the primary (first mentioned) ticker from question.
    
    Args:
        question: User's question
        
    Returns:
        First ticker found, or None
    """
    
    tickers = extract_tickers(question)
    
    # Validate ticker: must be 2-5 chars, all alpha, no single letter
    valid_tickers = []
    for ticker in tickers:
        base_ticker = ticker.split('.')[0]  # Get main part before .NS
        if base_ticker and 1 < len(base_ticker) <= 5 and base_ticker.isalpha():
            valid_tickers.append(ticker)
    
    return valid_tickers[0] if valid_tickers else None


def format_ticker_inquiry(ticker: str) -> str:
    """
    Format ticker for display and logging.
    
    Args:
        ticker: Stock ticker
        
    Returns:
        Formatted ticker string
    """
    
    return ticker.upper().strip()
