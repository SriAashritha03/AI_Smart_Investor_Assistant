"""
Financial Assistant Chat Service

Handles conversational queries about stocks, portfolios, and investments.
Integrates with Gemini AI for intelligent responses based on stock analysis.
Supports: stock analysis, portfolio review, stock comparison, general questions
"""

import logging
from typing import Dict
from services.analyzer import analyze_stock
from services.portfolio import analyze_portfolio
from services.gemini_chat import (
    generate_investment_advice,
    compare_stocks,
    analyze_portfolio_with_gemini,
    analyze_stock_portfolio_combo,
    answer_general_question,
    validate_ticker
)
from services.query_classifier import classify_query, QueryType, get_query_context
from services.financial_kb import get_answer
from services.memory import get_session_memory

logger = logging.getLogger(__name__)


def process_chat_message(user_message: str) -> Dict:
    """
    Process user chat message with intelligent query classification.
    
    Handles four types of queries:
    1. STOCK - Single stock analysis
    2. COMPARISON - Compare multiple stocks
    3. PORTFOLIO - Portfolio health analysis
    4. GENERAL - General financial knowledge
    
    Uses Gemini 2.5 Flash for all AI-powered responses.
    
    Args:
        user_message: User's question or statement
        
    Returns:
        Dict with success status, reply, type, and suggestions
    """
    
    if not user_message or not user_message.strip():
        return {
            "success": False,
            "error": "Message cannot be empty",
            "type": "general"
        }
    
    try:
        logger.info(f"Processing chat message: {user_message[:60]}...")
        
        # Track interaction in session memory
        get_session_memory().increment_interaction()
        
        # Classify the query
        query_type, query_data = classify_query(user_message)
        logger.info(f"Query classified as: {query_type} - {get_query_context(query_type, query_data)}")
        
        # ============================================================
        # STOCK QUERIES - Single stock analysis
        # ============================================================
        if query_type == QueryType.STOCK:
            ticker = query_data.get('ticker')
            
            # Check for missing ticker (critical edge case)
            if not ticker:
                return {
                    "success": True,
                    "type": QueryType.STOCK,
                    "reply": "I couldn't identify the stock. Which one do you mean? Try asking like:\n\n• \"Should I buy AAPL?\"\n• \"What about MSFT?\"\n• \"Is GOOGL a good buy?\"",
                    "suggestions": ["Specify a ticker", "Portfolio analysis", "General questions"]
                }
            
            if not validate_ticker(ticker):
                return {
                    "success": True,
                    "type": QueryType.STOCK,
                    "reply": f"❌ Invalid ticker: {ticker}\n\nValid format examples:\n• US stocks: AAPL, MSFT, GOOGL\n• Indian stocks: RELIANCE.NS, TCS.NS\n\nTry with a valid ticker.",
                    "suggestions": ["Try another ticker", "Portfolio advice", "General questions"]
                }
            
            try:
                # Analyze stock
                analysis = analyze_stock(ticker)
                
                if analysis.get("success"):
                    logger.info(f"✅ Stock analysis successful: {ticker}")
                    
                    # Update session memory with analyzed stock
                    get_session_memory().update_last_stock(ticker)
                    
                    # Generate Gemini-powered advice
                    advice = generate_investment_advice(
                        user_message,
                        analysis,
                        query_type=QueryType.STOCK
                    )
                    
                    return {
                        "success": True,
                        "type": QueryType.STOCK,
                        "reply": advice,
                        "ticker": ticker,
                        "suggestions": [
                            f"- Deeper {ticker} analysis",
                            f"- Compare {ticker} with others",
                            f"- Add {ticker} to portfolio?",
                            "- Risk analysis"
                        ]
                    }
                else:
                    error = analysis.get("error", "Analysis failed")
                    logger.warning(f"❌ Stock analysis error for {ticker}: {error}")
                    
                    return {
                        "success": True,
                        "type": QueryType.STOCK,
                        "reply": f"🔍 Couldn't analyze {ticker}: {error}\n\nTry:\n• Different ticker\n• Portfolio review\n• General finance questions",
                        "suggestions": ["Try another stock", "Portfolio analysis", "General questions"]
                    }
                    
            except Exception as e:
                logger.error(f"❌ Analysis exception for {ticker}: {type(e).__name__}: {str(e)}")
                return {
                    "success": True,
                    "type": QueryType.STOCK,
                    "reply": f"⚠️ Error analyzing {ticker}: {str(e)[:80]}\n\nTry asking about:\n• Another stock\n• Portfolio management\n• General finance topics",
                    "suggestions": ["Try another ticker", "Portfolio advice", "General questions"]
                }
        
        # ============================================================
        # COMPARISON QUERIES - Compare multiple stocks
        # ============================================================
        elif query_type == QueryType.COMPARISON:
            tickers = query_data.get('tickers', [])
            
            if len(tickers) < 2:
                return {
                    "success": True,
                    "type": QueryType.COMPARISON,
                    "reply": "📊 To compare stocks, I need at least 2. Try asking:\n\n• \"AAPL vs MSFT?\"\n• \"Which is better: GOOGL or META?\"\n• \"Compare NFLX with TSLA\"",
                    "suggestions": ["Stock analysis", "Portfolio review", "General advice"]
                }
            
            ticker1, ticker2 = tickers[0], tickers[1]
            
            try:
                # CRITICAL FIX: Use parallel execution to prevent timeout
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=2) as executor:
                    future1 = executor.submit(analyze_stock, ticker1)
                    future2 = executor.submit(analyze_stock, ticker2)
                    analysis1 = future1.result(timeout=25)
                    analysis2 = future2.result(timeout=25)
                
                if analysis1.get("success") and analysis2.get("success"):
                    logger.info(f"✅ Comparison analysis successful: {ticker1} vs {ticker2}")
                    
                    # Update session memory
                    memory = get_session_memory()
                    memory.update_last_stock(ticker1)  # Remember first stock from comparison
                    memory.add_comparison(ticker1, ticker2)
                    
                    # Generate comparison using Gemini
                    comparison = compare_stocks(user_message, analysis1, analysis2)
                    
                    return {
                        "success": True,
                        "type": QueryType.COMPARISON,
                        "reply": comparison,
                        "tickers": [ticker1, ticker2],
                        "suggestions": [
                            f"- Deep dive: {ticker1}",
                            f"- Deep dive: {ticker2}",
                            "- Add to portfolio?",
                            "- Risk comparison"
                        ]
                    }
                else:
                    failed = ticker1 if not analysis1.get("success") else ticker2
                    logger.warning(f"❌ Comparison failed for {failed}")
                    
                    return {
                        "success": True,
                        "type": QueryType.COMPARISON,
                        "reply": f"📊 Couldn't analyze {failed}. Try different tickers or ask for general advice.",
                        "suggestions": ["Try different stocks", "Single stock analysis", "General questions"]
                    }
                    
            except Exception as e:
                logger.error(f"❌ Comparison exception: {type(e).__name__}: {str(e)}")
                return {
                    "success": True,
                    "type": QueryType.COMPARISON,
                    "reply": f"⚠️ Error comparing stocks: {str(e)[:80]}\n\nTry asking about individual stocks or portfolio management.",
                    "suggestions": ["Analyze one stock", "Portfolio review", "General advice"]
                }
        
        # ============================================================
        # PORTFOLIO QUERIES - Portfolio analysis + Multi-intent
        # ============================================================
        elif query_type == QueryType.PORTFOLIO:
            try:
                # Check for multi-intent: Portfolio + specific stock
                tickers = query_data.get('tickers', [])
                
                # Multi-intent: "Is my portfolio good with AAPL?" or "Should I add AAPL to my portfolio?"
                if tickers:
                    ticker = tickers[0]
                    logger.info(f"✅ Multi-intent detected: Portfolio + Stock {ticker}")
                    
                    # Analyze both portfolio and specific stock
                    stock_analysis = analyze_stock(ticker)
                    demo_portfolio = ["AAPL", "MSFT", "GOOGL"]
                    portfolio_analysis = analyze_portfolio(demo_portfolio)
                    
                    if stock_analysis.get("success") and portfolio_analysis.get("success"):
                        # Use combo function to combine both analyses
                        advice = analyze_stock_portfolio_combo(
                            user_message,
                            stock_analysis,
                            portfolio_analysis,
                            ticker
                        )
                        get_session_memory().update_last_stock(ticker)
                        get_session_memory().update_portfolio(demo_portfolio)
                        
                        return {
                            "success": True,
                            "type": QueryType.PORTFOLIO,
                            "reply": advice,
                            "ticker": ticker,
                            "suggestions": [
                                f"- Deep analysis of {ticker}",
                                "- Portfolio rebalancing tips",
                                "- Alternative stocks",
                                "- Risk management"
                            ]
                        }
                
                # Standard portfolio-only analysis
                # Note: For now, using demo portfolio - in production would get user's holdings
                demo_portfolio = ["AAPL", "MSFT", "GOOGL"]
                
                portfolio_result = analyze_portfolio(demo_portfolio)
                
                if portfolio_result.get("success"):
                    logger.info("✅ Portfolio analysis successful")
                    
                    # Update session memory with portfolio
                    get_session_memory().update_portfolio(demo_portfolio)
                    
                    # Generate Gemini-powered portfolio advice
                    advice = analyze_portfolio_with_gemini(user_message, portfolio_result)
                    
                    return {
                        "success": True,
                        "type": QueryType.PORTFOLIO,
                        "reply": advice,
                        "portfolio_size": portfolio_result.get('portfolio_size'),
                        "risk_score": portfolio_result.get('risk_score'),
                        "suggestions": [
                            "- Rebalance portfolio",
                            "- Add defensive stocks",
                            "- Reduce concentration",
                            "- Review allocation"
                        ]
                    }
                else:
                    error = portfolio_result.get("error", "Analysis failed")
                    logger.warning(f"❌ Portfolio analysis error: {error}")
                    
                    return {
                        "success": True,
                        "type": QueryType.PORTFOLIO,
                        "reply": f"📊 Portfolio analysis unavailable: {error}\n\nTry:\n• Analyzing specific stocks\n• General investment advice\n• Risk management tips",
                        "suggestions": ["Stock analysis", "Risk management", "General advice"]
                    }
                    
            except Exception as e:
                logger.error(f"❌ Portfolio exception: {type(e).__name__}: {str(e)}")
                return {
                    "success": True,
                    "type": QueryType.PORTFOLIO,
                    "reply": f"⚠️ Error analyzing portfolio: {str(e)[:80]}\n\nTry:\n• Asking about specific stocks\n• General investment strategies\n• Risk profile questions",
                    "suggestions": ["Stock analysis", "General advice", "Risk questions"]
                }
        
        # ============================================================
        # GENERAL QUERIES - Financial knowledge (trader-focused via Gemini)
        # ============================================================
        elif query_type == QueryType.GENERAL:
            try:
                # IMPORTANT: Always use Gemini for trader-focused answers
                # Skip KB to ensure consistent, conversational trader-style responses
                # (Bypass: kb_answer = get_answer(user_message))
                
                logger.info("✅ Using Gemini for trader-focused answer (skipping textbook KB)")
                
                # Generate Gemini-powered general answer (trader-oriented, NOT textbook)
                answer = answer_general_question(user_message)
                
                return {
                    "success": True,
                    "type": QueryType.GENERAL,
                    "reply": answer,
                    "suggestions": [
                        "- Stock analysis",
                        "- Portfolio review",
                        "- Related concepts",
                        "- Practical examples"
                    ]
                }
                
            except Exception as e:
                logger.error(f"❌ General question exception: {type(e).__name__}: {str(e)}")
                return {
                    "success": True,
                    "type": QueryType.GENERAL,
                    "reply": f"📚 Let me help with financial concepts!\n\n{str(e)[:100]}\n\nTry asking about specific stocks or portfolio management.",
                    "suggestions": ["Stock analysis", "Portfolio advice", "Risk management"]
                }
    
    except Exception as e:
        logger.error(f"❌ Critical error in chat processing: {type(e).__name__}: {str(e)}")
        return {
            "success": True,
            "type": "general",
            "reply": f"⚠️ I encountered an issue processing your request.\n\nPlease try:\n• Asking about a specific stock\n• Portfolio questions\n• General finance topics\n\nError: {str(e)[:60]}",
            "suggestions": ["Stock analysis", "Portfolio review", "General questions"]
        }
