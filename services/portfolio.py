import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Dict


def analyze_portfolio(tickers: List[str]) -> Dict:
    tickers = [t.strip().upper() for t in tickers]

    if len(tickers) < 2:
        return {"success": False, "error": "Minimum 2 stocks required"}

    try:
        # ---- Fetch Data (6 months) ----
        data = yf.download(tickers, period="6mo")["Adj Close"]

        # If single stock → convert to DataFrame
        if isinstance(data, pd.Series):
            data = data.to_frame()

        # ---- Calculate Daily Returns ----
        returns = data.pct_change().dropna()

        # ---- Portfolio Volatility (Risk) ----
        portfolio_volatility = returns.std().mean()

        # Normalize to score (0–100)
        risk_score = min(100, round(portfolio_volatility * 1000, 2))

        # ---- Diversification (Correlation) ----
        corr_matrix = returns.corr()

        avg_corr = corr_matrix.values[np.triu_indices(len(tickers), 1)].mean()

        if avg_corr > 0.75:
            diversification = "Poor (high correlation between stocks)"
        elif avg_corr > 0.4:
            diversification = "Moderate diversification"
        else:
            diversification = "Good diversification"

        # ---- Suggestion ----
        if risk_score > 70:
            suggestion = "Reduce risk: add defensive stocks (FMCG, Pharma)"
        elif risk_score < 30:
            suggestion = "Increase growth exposure (IT, Midcaps)"
        else:
            suggestion = "Portfolio is balanced"

        return {
            "success": True,
            "portfolio_size": len(tickers),
            "risk_score": risk_score,
            "avg_correlation": round(avg_corr, 2),
            "diversification": diversification,
            "rebalance_suggestion": suggestion,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}