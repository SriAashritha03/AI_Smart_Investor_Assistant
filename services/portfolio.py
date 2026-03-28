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
        print(f"📊 Fetching data for tickers: {tickers}")
        raw_data = yf.download(tickers, period="6mo", progress=False)
        
        # Check if data was returned
        if raw_data.empty:
            return {"success": False, "error": f"No data found for tickers: {', '.join(tickers)}. Check if tickers are valid."}
        
        # Try 'Adj Close' first, then fall back to 'Close'
        if "Adj Close" in raw_data.columns:
            data = raw_data["Adj Close"]
        elif "Close" in raw_data.columns:
            data = raw_data["Close"]
            print("ℹ️ Using 'Close' price instead of 'Adj Close'")
        else:
            print(f"⚠️  Available columns: {raw_data.columns.tolist()}")
            return {"success": False, "error": f"Price data not available. Got columns: {raw_data.columns.tolist()}"}
        
        print(f"✅ Data fetched successfully: {data.shape}")

        # If single stock → convert to DataFrame
        if isinstance(data, pd.Series):
            data = data.to_frame()

        # ---- Calculate Daily Returns ----
        returns = data.pct_change().dropna()
        
        if len(returns) == 0:
            return {"success": False, "error": "Not enough data to calculate returns"}

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
        print(f"🔴 Portfolio error: {type(e).__name__}: {str(e)}")
        return {"success": False, "error": f"Portfolio analysis failed: {str(e)}"}