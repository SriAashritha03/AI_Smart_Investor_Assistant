"""
Session Memory Manager

Maintains conversation context across chat interactions.
Tracks user's previous stocks and portfolio for better context awareness.
"""

import logging
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


class SessionMemory:
    """
    Manage session-level context and memory during chat conversations.
    
    Features:
    - Track last analyzed stock
    - Remember portfolio stocks
    - Support context references (e.g., "should I buy this?" referring to last stock)
    """
    
    def __init__(self):
        """Initialize empty session memory."""
        self.last_stock: Optional[str] = None
        self.portfolio: List[str] = []
        self.comparison_history: List[tuple] = []
        self.interaction_count: int = 0
    
    def update_last_stock(self, ticker: str) -> None:
        """
        Record that user asked about a stock.
        
        Args:
            ticker: Stock ticker symbol
        """
        if ticker and ticker != self.last_stock:
            self.last_stock = ticker
            logger.info(f"Memory: Updated last_stock to {ticker}")
    
    def update_portfolio(self, tickers: List[str]) -> None:
        """
        Update portfolio context.
        
        Args:
            tickers: List of stock tickers in portfolio
        """
        if tickers:
            self.portfolio = tickers
            logger.info(f"Memory: Updated portfolio with {len(tickers)} stocks")
    
    def add_comparison(self, ticker1: str, ticker2: str) -> None:
        """
        Record a comparison for context.
        
        Args:
            ticker1: First stock in comparison
            ticker2: Second stock in comparison
        """
        self.comparison_history.append((ticker1, ticker2))
        logger.info(f"Memory: Recorded comparison {ticker1} vs {ticker2}")
    
    def get_last_stock(self) -> Optional[str]:
        """
        Get the last stock user asked about.
        
        Returns:
            Stock ticker or None
        """
        return self.last_stock
    
    def get_portfolio(self) -> List[str]:
        """
        Get remembered portfolio.
        
        Returns:
            List of portfolio tickers
        """
        return self.portfolio
    
    def resolve_ambiguous_reference(self, text: str) -> Optional[str]:
        """
        Resolve phrases like "this stock", "it", "this" to actual ticker.
        
        Args:
            text: User message text
            
        Returns:
            Resolved ticker or None
        """
        # Check for ambiguous references
        if any(word in text.lower() for word in ["this stock", "it", "this", "that one", "this one"]):
            if self.last_stock:
                logger.info(f"Memory: Resolved ambiguous reference to {self.last_stock}")
                return self.last_stock
        
        return None
    
    def increment_interaction(self) -> None:
        """Track number of interactions in session."""
        self.interaction_count += 1
    
    def reset(self) -> None:
        """Clear session memory (for testing or new session)."""
        self.last_stock = None
        self.portfolio = []
        self.comparison_history = []
        self.interaction_count = 0
        logger.info("Memory: Session reset")
    
    def get_summary(self) -> Dict:
        """
        Get current memory state summary.
        
        Returns:
            Dictionary with session context
        """
        return {
            "last_stock": self.last_stock,
            "portfolio": self.portfolio,
            "comparison_count": len(self.comparison_history),
            "interaction_count": self.interaction_count
        }


# Global session memory instance
_session_memory = SessionMemory()


def get_session_memory() -> SessionMemory:
    """
    Get global session memory instance.
    
    Returns:
        SessionMemory instance
    """
    return _session_memory


def reset_session() -> None:
    """Reset session memory (between conversations)."""
    _session_memory.reset()
