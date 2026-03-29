"""
Financial Knowledge Base

Simple Q&A database for general financial knowledge questions.
Used when no specific stock analysis is needed.
"""

FINANCIAL_KNOWLEDGE = {
    # Technical Indicators
    "breakout": "A breakout occurs when a stock's price moves above resistance (upper limit) or below support (lower limit). It signals potential trend continuation. High volume confirms breakout strength.",
    
    "support": "Support is a price level where a stock tends to find buyers and stops falling. It's like a floor. When price dips to support and bounces back up, it's a bullish signal.",
    
    "resistance": "Resistance is a price level where a stock tends to find sellers and stops rising. It's like a ceiling. Breaking above resistance opens doors to higher prices.",
    
    "macd": "MACD (Moving Average Convergence Divergence) is a momentum indicator. It compares fast and slow moving averages. Bullish when MACD crosses above signal line. Helps identify trend changes.",
    
    "rsi": "RSI (Relative Strength Index) measures momentum on a scale of 0-100. RSI > 70 = overbought (potential sell), RSI < 30 = oversold (potential buy). Helps time entries/exits.",
    
    "moving average": "A moving average smooths price data to identify trends. MA20 (fast) and MA50 (slow). When fast MA crosses above slow MA = bullish. Helps filter noise from price movements.",
    
    "volume": "Volume is the number of shares traded. High volume = strong conviction. Confirm breakouts with volume. Low volume on breakouts = weak signal. Volume trends should align with price trends.",
    
    # Portfolio Concepts
    "diversification": "Spreading investments across different stocks, sectors, and asset types reduces risk. Don't put all eggs in one basket. Mix growth and defensive stocks. Target: correlation < 0.5 between holdings.",
    
    "asset allocation": "Dividing portfolio between stocks, bonds, and other assets based on risk tolerance. Conservative: 30% stocks/70% bonds. Moderate: 60/40. Aggressive: 80/20. Rebalance quarterly.",
    
    "rebalancing": "Adjusting portfolio back to target allocation. Sell winners that increased share, buy laggards. Rebalance quarterly to maintain risk profile. Locks in gains, prevents overconcentration.",
    
    "correlation": "Measure of how stocks move together (-1 to +1). Low correlation = good diversification. High correlation = redundant holdings. Target: < 0.5 correlation between stocks.",
    
    # Trading Concepts
    "bull market": "Rising market with optimism. Characterized by higher highs and higher lows. Volume increases. Last bull run lifted indices 40%+ in 2 years. Buyers in control.",
    
    "bear market": "Declining market with pessimism. Characterized by lower highs and lower lows. Volume decreases. Usually defined as 20%+ decline. Sellers in control.",
    
    "momentum": "Strength of price trend. Measured by RSI, MACD, rate of change. Stocks with strong momentum tend to continue trending. Buy on rising momentum, sell on declining momentum.",
    
    "volatility": "Measure of price swings. High volatility = large swings, risky. Low volatility = stable, safer. VIX measures market volatility. Use volatility to size positions appropriately.",
    
    "stop loss": "Predetermined price to exit losing position, limiting downside. Example: buy at 100, set stop at 95 (5% loss limit). Never risk > 2% of portfolio on single trade.",
    
    "take profit": "Target price to lock in gains. Example: buy at 100, target at 115 (15% profit). Helps avoid greed. Lock in profits at resistance levels.",
    
    "dollar cost averaging": "Investing fixed amount regularly regardless of price. Smooths volatility impact. Reduces timing risk. Good for long-term investors, passive strategies.",
    
    # Valuation
    "pe ratio": "Price-to-Earnings ratio = Stock Price / Earnings Per Share. Low P/E = potentially undervalued. High P/E = expensive or growing fast. Compare within same sector.",
    
    "dividend yield": "Annual dividend / stock price. Higher yield = more income. Mature companies pay dividends. Growing companies reinvest (lower/no yield). Balance income vs growth.",
    
    "earnings": "Company profit after expenses. EPS = Earnings Per Share. Growing earnings = positive signal. Track quarterly earnings growth. Compare to industry average.",
    
    # Risk Management
    "risk": "Possibility of losing money. Always inversely related to potential returns. Know your risk tolerance. Diversify to manage risk. Use stop losses to limit downside.",
    
    "position sizing": "How much to invest in each stock. Never risk > 2% of total portfolio on single position. Size = (Risk % * Portfolio) / (Entry - Stop Loss). Key to long-term success.",
    
    "hedge": "Strategy to offset losses. Buy protective puts, sell covered calls. Reduces upside but limits downside. Used to protect gains, not for trading.",
    
    "margin": "Borrowing funds to trade. Amplifies gains and losses. Risky for beginners. Requires collateral. Can trigger margin calls if position moves against you.",
}


def get_answer(question: str) -> str:
    """
    Get simplified answer to general financial question.
    
    Args:
        question: Financial question
        
    Returns:
        Simple, educational answer
    """
    
    question_lower = question.lower()
    
    # Extract keywords
    for keyword, answer in FINANCIAL_KNOWLEDGE.items():
        if keyword in question_lower:
            return f"📚 **{keyword.title()}**\n\n{answer}"
    
    # Default if no match
    return None


def suggest_related_topics(question: str) -> list:
    """
    Suggest related financial topics for learning.
    
    Args:
        question: User question
        
    Returns:
        List of related topics
    """
    
    # Map topics to related topics
    related_map = {
        "breakout": ["moving average", "support", "resistance", "volume"],
        "support": ["resistance", "breakout", "momentum"],
        "macd": ["rsi", "momentum", "moving average"],
        "rsi": ["macd", "momentum", "overbought", "oversold"],
        "diversification": ["correlation", "asset allocation", "risk"],
        "portfolio": ["diversification", "asset allocation", "rebalancing"],
    }
    
    question_lower = question.lower()
    
    for topic, related in related_map.items():
        if topic in question_lower:
            return related[:3]  # Return top 3
    
    return []
