import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from services.analyzer import analyze_stock


def get_stock_sector(ticker: str) -> str:
    """Fetch sector information for a stock"""
    try:
        stock = yf.Ticker(ticker)
        sector = stock.info.get('sector', 'Unknown')
        return sector if sector else 'Unknown'
    except:
        return 'Unknown'


def analyze_portfolio(tickers: List[str]) -> Dict:
    """
    AI-powered portfolio intelligence system that analyzes each stock
    and generates data-driven recommendations.
    """
    tickers = [t.strip().upper() for t in tickers]

    if len(tickers) < 2:
        return {"success": False, "error": "Minimum 2 stocks required"}

    try:
        print(f"📊 Portfolio Intelligence System - Analyzing {len(tickers)} stocks...")
        
        # ===== TASK 1: STOCK-LEVEL ANALYSIS =====
        print("\n📈 TASK 1: Analyzing individual stocks...")
        stock_breakdown = []
        buy_count = 0
        sell_count = 0
        hold_count = 0
        total_confidence = 0
        
        for ticker in tickers:
            print(f"  • Analyzing {ticker}...")
            analysis = analyze_stock(ticker)
            
            if analysis.get("success"):
                stock_info = {
                    "stock": ticker,
                    "sector": get_stock_sector(ticker),
                    "confidence": analysis.get("confidence", 0),
                    "action": analysis.get("action", "HOLD"),
                    "signals": analysis.get("signals_triggered", []),
                    "opportunity": analysis.get("opportunity_level", "Unknown"),
                    "summary": analysis.get("summary", ""),
                    "news_sentiment": analysis.get("news_sentiment", {}).get("sentiment_label", "Neutral"),
                }
                stock_breakdown.append(stock_info)
                
                # Track action distribution
                action = analysis.get("action", "HOLD")
                if action == "BUY":
                    buy_count += 1
                elif action == "SELL":
                    sell_count += 1
                else:
                    hold_count += 1
                
                total_confidence += analysis.get("confidence", 0)
        
        avg_confidence = round(total_confidence / len(stock_breakdown), 1) if stock_breakdown else 0
        
        # ===== TASK 2: PORTFOLIO DIAGNOSIS =====
        print("\n🔍 TASK 2: Portfolio diagnosis...")
        
        # Fetch price data for correlation analysis
        raw_data = yf.download(tickers, period="6mo", progress=False)
        if "Adj Close" in raw_data.columns:
            data = raw_data["Adj Close"]
        elif "Close" in raw_data.columns:
            data = raw_data["Close"]
        else:
            return {"success": False, "error": "Could not fetch price data"}
        
        if isinstance(data, pd.Series):
            data = data.to_frame()
        
        returns = data.pct_change().dropna()
        
        # Calculate metrics
        portfolio_volatility = returns.std().mean()
        risk_score = min(100, round(portfolio_volatility * 1000, 2))
        
        corr_matrix = returns.corr()
        avg_corr = corr_matrix.values[np.triu_indices(len(tickers), 1)].mean() if len(tickers) > 1 else 0
        
        # Sector concentration
        sectors = [info["sector"] for info in stock_breakdown]
        sector_counts = {}
        for sector in sectors:
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
        
        sector_concentration = max(sector_counts.values()) / len(tickers) if tickers else 0
        
        # Detect weaknesses
        weaknesses = []
        
        if sector_concentration > 0.6:
            concentrated_sector = [s for s, c in sector_counts.items() if c == max(sector_counts.values())][0]
            weaknesses.append(f"Over-concentrated in {concentrated_sector} sector ({int(sector_concentration * 100)}%)")
        
        # Fix: Account for portfolio size in diversification assessment
        if len(tickers) < 4:
            weaknesses.append(f"Limited diversification due to small portfolio size ({len(tickers)} assets)")
        elif avg_corr > 0.75:
            weaknesses.append("High correlation between holdings (low diversification)")
        
        if buy_count == 0 and sell_count > 0:
            weaknesses.append("Portfolio lacks strong growth signals and shows bearish bias — consider rebalancing toward higher-confidence opportunities")
        
        if risk_score > 70:
            weaknesses.append(f"High portfolio volatility ({risk_score}) — consider hedging with lower-volatility assets")
        
        growth_signals = sum(1 for s in stock_breakdown if s["signals"] and any("uptrend" in sig.lower() or "breakout" in sig.lower() for sig in s["signals"]))
        if growth_signals == 0 and len(stock_breakdown) > 0:
            weaknesses.append("Limited growth catalysts - portfolio lacks upside momentum")
        
        if len(weaknesses) == 0:
            weaknesses.append("Portfolio is well-balanced with appropriate risk-reward profile")
        
        # ===== TASK 3 & 4: DYNAMIC RECOMMENDATIONS =====
        print("\n💡 TASK 3 & 4: Generating recommendations...")
        
        recommendations = generate_recommendations(
            stock_breakdown=stock_breakdown,
            risk_score=risk_score,
            avg_corr=avg_corr,
            sector_concentration=sector_concentration,
            buy_count=buy_count,
            sell_count=sell_count,
            hold_count=hold_count
        )
        
        # ===== TASK 5: PORTFOLIO SUMMARY =====
        # Fix diversification: proper correlation → diversification mapping
        if avg_corr < 0.3:
            diversification = "High"
        elif avg_corr < 0.7:
            diversification = "Moderate"
        else:
            diversification = "Low"
        
        # Confidence insight
        if avg_confidence > 70:
            confidence_insight = f"Strong conviction portfolio (avg confidence {avg_confidence}%) — clear trade signals"
        elif avg_confidence > 40:
            confidence_insight = f"Moderate conviction portfolio (avg confidence {avg_confidence}%) — mixed signals"
        else:
            confidence_insight = f"Low conviction portfolio (avg confidence {avg_confidence}%) — lacks strong signals for entry"
        
        portfolio_summary = {
            "portfolio_size": len(tickers),
            "avg_confidence": avg_confidence,
            "confidence_insight": confidence_insight,
            "risk_score": risk_score,
            "avg_correlation": round(avg_corr, 2),
            "sector_concentration": round(sector_concentration, 2),
            "action_distribution": {
                "buy": buy_count,
                "sell": sell_count,
                "hold": hold_count
            },
            "diversification": diversification,
        }
        
        # Generate overall insight
        insight = generate_portfolio_insight(portfolio_summary, stock_breakdown, weaknesses)
        
        # ===== TASK 7: STRUCTURED OUTPUT =====
        return {
            "success": True,
            "portfolio_summary": portfolio_summary,
            "stock_breakdown": stock_breakdown,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "insight": insight,
        }

    except Exception as e:
        print(f"🔴 Portfolio error: {type(e).__name__}: {str(e)}")
        return {"success": False, "error": f"Portfolio analysis failed: {str(e)}"}


def generate_recommendations(
    stock_breakdown: List[Dict],
    risk_score: float,
    avg_corr: float,
    sector_concentration: float,
    buy_count: int,
    sell_count: int,
    hold_count: int
) -> Dict:
    """
    Generate realistic recommendations with add/reduce/monitor structure.
    - Never remove all stocks
    - Use 'reduce' instead of 'remove'
    - Add 'monitor' for uncertain positions
    """
    add_stocks = []
    reduce_stocks = []
    monitor_stocks = []
    reasoning = []
    portfolio_tickers = [s["stock"] for s in stock_breakdown]
    priority = "MEDIUM"
    
    # Analysis: Growth signals
    growth_signals = sum(1 for s in stock_breakdown if s["signals"] and any("uptrend" in sig.lower() or "breakout" in sig.lower() for sig in s["signals"]))
    has_growth = growth_signals > 0
    
    # Analysis: Sentiment
    positive_sentiment = sum(1 for s in stock_breakdown if s["news_sentiment"] == "Positive")
    negative_sentiment = sum(1 for s in stock_breakdown if s["news_sentiment"] == "Negative")
    
    # Logic 1: Low growth → add growth stocks
    if not has_growth and len(stock_breakdown) > 0:
        add_stocks.extend(["AAPL", "NVDA", "MSFT"])
        reasoning.append("Limited growth signals — add high-confidence growth assets")
        priority = "HIGH"
    
    # Logic 2: High correlation → add diversification
    if avg_corr > 0.75:
        add_stocks.extend(["JNJ", "UNH", "PG"])
        reasoning.append("High correlation — add uncorrelated defensive assets")
        priority = "HIGH"
    
    # Logic 3: High risk → suggest hedging
    if risk_score > 70:
        if "PG" not in add_stocks and "JNJ" not in add_stocks:
            add_stocks.extend(["PG", "JNJ"])
        reasoning.append(f"High volatility ({risk_score}) — add stability")
    
    # Logic 4: Over-concentrated sector → reduce weakest
    if sector_concentration > 0.6 and len(stock_breakdown) > 1:
        weak_in_sector = [s for s in stock_breakdown if s["confidence"] < 40]
        if weak_in_sector:
            reduce_stocks.append(weak_in_sector[0]["stock"])
            reasoning.append(f"Sector concentration — reduce weaker position")
    
    # Logic 5: Multiple sell signals → reduce weakest, monitor others
    if sell_count > buy_count and sell_count > 0 and len(stock_breakdown) > 1:
        worst_stocks = sorted(stock_breakdown, key=lambda x: x["confidence"])
        reduce_stocks.append(worst_stocks[0]["stock"])
        if len(worst_stocks) > 1:
            monitor_stocks.extend([s["stock"] for s in worst_stocks[1:2]])
        reasoning.append("Multiple sell signals — reduce weakest, monitor others")
        priority = "HIGH"
    elif sell_count > buy_count and len(stock_breakdown) == 1:
        monitor_stocks.extend(portfolio_tickers)
    
    # Logic 6: Sentiment context
    if negative_sentiment >= positive_sentiment and negative_sentiment > 0:
        reasoning.append("Mixed/bearish sentiment — rebalance toward higher-confidence growth")
        priority = "HIGH"
    
    # Deduplicate and clean
    add_stocks = list(set(add_stocks))
    reduce_stocks = list(set(reduce_stocks))
    monitor_stocks = list(set(monitor_stocks) - set(reduce_stocks))
    
    # Filter out stocks already in portfolio
    add_stocks = [s for s in add_stocks if s not in portfolio_tickers][:3]
    
    # Ensure we never reduce ALL stocks
    if len(reduce_stocks) >= len(portfolio_tickers):
        reduce_stocks = reduce_stocks[:max(0, len(portfolio_tickers) - 1)]
    
    if not reasoning:
        reasoning.append("Portfolio is balanced — maintain current allocation")
    
    return {
        "add": add_stocks,
        "reduce": reduce_stocks,
        "monitor": monitor_stocks,
        "reasoning": " • ".join(reasoning),
        "priority": priority,
    }


def generate_portfolio_insight(
    summary: Dict,
    stock_breakdown: List[Dict],
    weaknesses: List[str]
) -> str:
    """Generate structured insight: bias + sentiment + conviction + diversification context."""
    
    insight_parts = []
    
    # Bias interpretation
    buy = summary["action_distribution"]["buy"]
    sell = summary["action_distribution"]["sell"]
    hold = summary["action_distribution"]["hold"]
    
    if sell > buy:
        bias = "Bearish bias"
    elif buy > sell:
        bias = "Bullish bias"
    else:
        bias = "Neutral bias"
    
    # Sentiment interpretation
    sentiments = [s["news_sentiment"] for s in stock_breakdown]
    positive = sentiments.count("Positive")
    negative = sentiments.count("Negative")
    neutral = sentiments.count("Neutral")
    
    if positive > 0 and negative > 0:
        sentiment_text = "mixed sentiment signals"
    elif negative > positive:
        sentiment_text = "negative sentiment bias"
    elif positive > negative:
        sentiment_text = "positive sentiment bias"
    else:
        sentiment_text = "neutral sentiment"
    
    insight_parts.append(f"{bias} driven by technical weakness despite {sentiment_text}")
    
    # Conviction context
    if summary["avg_confidence"] > 70:
        conviction = "High conviction"
    elif summary["avg_confidence"] > 40:
        conviction = "Moderate conviction"
    else:
        conviction = "Low conviction"
    
    insight_parts.append(f"{conviction} portfolio ({summary['avg_confidence']}% avg)")
    
    # Diversification context - account for portfolio size
    if summary["portfolio_size"] < 4:
        div_text = f"Limited diversification due to small size ({summary['portfolio_size']} assets)"
    elif summary["avg_correlation"] < 0.3:
        div_text = "Excellent diversification"
    elif summary["avg_correlation"] < 0.7:
        div_text = "Good correlation (low overlap)"
    else:
        div_text = "Weak diversification (high overlap)"
    
    insight_parts.append(div_text)
    
    # Action recommendation
    if sell > buy and summary["avg_confidence"] < 50:
        insight_parts.append("Opportunity to rebalance toward higher-confidence growth assets")
    
    return " • ".join(insight_parts) if insight_parts else "Portfolio analysis complete"


def analyze_stock_fit(portfolio_tickers: List[str], test_stock: str) -> Dict:
    """
    Analyze how well a new stock fits with existing portfolio.
    Smart fit scoring based on correlation, growth complement, and sector diversity.
    """
    test_stock = test_stock.strip().upper()
    portfolio_tickers = [t.strip().upper() for t in portfolio_tickers]
    
    try:
        print(f"\n🎯 Analyzing fit of {test_stock} with portfolio...")
        
        # Analyze test stock
        test_analysis = analyze_stock(test_stock)
        if not test_analysis.get("success"):
            return {
                "success": False,
                "error": f"Could not analyze {test_stock}"
            }
        
        # Fetch price data for correlation
        all_tickers = portfolio_tickers + [test_stock]
        raw_data = yf.download(all_tickers, period="6mo", progress=False)
        
        if "Adj Close" in raw_data.columns:
            data = raw_data["Adj Close"]
        elif "Close" in raw_data.columns:
            data = raw_data["Close"]
        else:
            return {"success": False, "error": "Could not fetch price data"}
        
        if isinstance(data, pd.Series):
            data = data.to_frame()
        
        returns = data.pct_change().dropna()
        
        # Calculate correlations with portfolio stocks
        test_column = test_stock if test_stock in returns.columns else test_stock.replace('.NS', '')
        if test_column not in returns.columns:
            test_column = [c for c in returns.columns if test_stock in str(c)][0] if any(test_stock in str(c) for c in returns.columns) else None
        
        if test_column is None:
            return {"success": False, "error": "Test stock data not found"}
        
        corr_with_portfolio = returns[test_column].corrwith(returns[[c for c in returns.columns if c != test_column]])
        avg_new_corr = corr_with_portfolio.mean() if len(corr_with_portfolio) > 0 else 0.5
        
        # Portfolio current correlation
        portfolio_returns = returns[[c for c in returns.columns if c != test_column]]
        portfolio_corr = portfolio_returns.corr()
        current_avg_corr = portfolio_corr.values[np.triu_indices(len(portfolio_returns.columns), 1)].mean() if len(portfolio_returns.columns) > 1 else 0
        
        # Fit score calculation
        fit_score = 50
        fit_reasons = []
        
        # Reason 1: Correlation impact
        if avg_new_corr < current_avg_corr - 0.1:
            fit_score += 25
            fit_reasons.append(f"✅ Reduces portfolio correlation ({avg_new_corr:.2f} vs {current_avg_corr:.2f})")
        elif avg_new_corr < current_avg_corr + 0.1:
            fit_score += 10
            fit_reasons.append(f"~  Maintains correlation ({avg_new_corr:.2f})")
        else:
            fit_score -= 10
            fit_reasons.append(f"❌ Increases correlation ({avg_new_corr:.2f} vs {current_avg_corr:.2f})")
        
        # Reason 2: Growth signals
        if test_analysis.get("action") == "BUY":
            fit_score += 15
            fit_reasons.append(f"✅ Buy signal - adds growth momentum")
        elif test_analysis.get("action") == "SELL":
            fit_score -= 15
            fit_reasons.append(f"❌ Sell signal - contradicts rebalancing goal")
        
        # Reason 3: Confidence
        confidence = test_analysis.get("confidence", 0)
        if confidence > 75:
            fit_score += 10
            fit_reasons.append(f"✅ High confidence ({confidence}%)")
        elif confidence < 40:
            fit_score -= 10
            fit_reasons.append(f"❌ Low confidence ({confidence}%)")
        
        # Reason 4: Sector diversity
        test_sector = get_stock_sector(test_stock)
        portfolio_sectors = [get_stock_sector(t) for t in portfolio_tickers]
        if test_sector not in portfolio_sectors or portfolio_sectors.count(test_sector) == 1:
            fit_score += 10
            fit_reasons.append(f"✅ Adds sector diversity ({test_sector})")
        else:
            sector_count = portfolio_sectors.count(test_sector)
            fit_score -= 5
            fit_reasons.append(f"⚠️  Increases {test_sector} concentration")
        
        fit_score = min(100, max(0, fit_score))
        
        fit_level = (
            "Excellent Fit" if fit_score > 75
            else "Good Fit" if fit_score > 55
            else "Moderate Fit" if fit_score > 35
            else "Poor Fit"
        )
        
        return {
            "success": True,
            "stock": test_stock,
            "fit_score": fit_score,
            "fit_level": fit_level,
            "reasons": fit_reasons,
            "action": test_analysis.get("action"),
            "confidence": test_analysis.get("confidence", 0),
        }
        
    except Exception as e:
        print(f"❌ Stock fit analysis error: {type(e).__name__}: {str(e)}")
        return {"success": False, "error": f"Could not analyze fit: {str(e)}"}