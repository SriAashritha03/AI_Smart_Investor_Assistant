"""
Stock Analysis API

Production-ready FastAPI backend for stock opportunity analysis.

Endpoints:
- POST /analyze-stock - Analyze a single stock
- GET / - API health check
- GET /docs - Interactive API documentation (Swagger UI)

Usage:
    uvicorn main:app --reload

Example curl:
    curl -X POST "http://localhost:8000/analyze-stock" \
         -H "Content-Type: application/json" \
         -d '{"ticker": "RELIANCE.NS"}'
"""

import logging
import json
import os
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from services.analyzer import analyze_stock, batch_analyze_stocks
from services.chat import process_chat_message

# Configure FFmpeg for moviepy (using imageio-ffmpeg)
try:
    import imageio_ffmpeg
    os.environ['IMAGEIO_FFMPEG_EXE'] = imageio_ffmpeg.get_ffmpeg_exe()
    import moviepy.config
    moviepy.config.IMAGEMAGICK_BINARY = imageio_ffmpeg.get_ffmpeg_exe()
except:
    pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ============================================================================
# Load Stocks Data
# ============================================================================

STOCKS = []
stocks_file = os.path.join(os.path.dirname(__file__), "stocks.json")
try:
    with open(stocks_file, "r") as f:
        data = json.load(f)
        STOCKS = data.get("stocks", [])
    logger.info(f"Loaded {len(STOCKS)} available stocks")
except FileNotFoundError:
    logger.warning(f"Stocks file not found at {stocks_file}. Stocks endpoint will be empty.")
except json.JSONDecodeError:
    logger.error(f"Error parsing stocks.json. Invalid JSON format.")

# ============================================================================
# Demo Mode Responses
# ============================================================================

DEMO_MODE_ENABLED = True

DEMO_RESPONSES = {
    "AAPL": {
        "success": True,
        "stock": "AAPL",
        "date": "2026-03-27",
        "opportunity_level": "Moderate",
        "confidence": 68,
        "action": "BUY",
        "signals_triggered": ["Uptrend", "Breakout"],
        "signal_details": [
            {"name": "Uptrend", "triggered": True, "strength": "Moderate", "reasoning": "5 consecutive up days"},
            {"name": "Breakout", "triggered": True, "strength": "Strong", "reasoning": "Price crossed 10-day high"},
            {"name": "Volume Spike", "triggered": False, "strength": "-", "reasoning": "volume 1.2x average"},
            {"name": "Price Surge", "triggered": False, "strength": "-", "reasoning": "2.3% increase - below 3%"},
        ],
        "summary": "Apple shows bulls momentum with breakout confirmation. Strong buying opportunity.",
        "data_points": 124,
        "chart_patterns": {
            "overall_strength": "Moderate",
            "pattern_count": 2,
            "patterns_detected": [
                {
                    "pattern_name": "Breakout",
                    "detected": True,
                    "strength": "Strong",
                    "current_price": 185.50,
                    "resistance_level": 182.30,
                    "breakout_margin": 1.75,
                    "volume_confirmation": True
                },
                {
                    "pattern_name": "Support",
                    "detected": True,
                    "strength": "Moderate",
                    "current_price": 185.50,
                    "support_level": 178.50,
                    "distance_from_support": 3.87,
                    "recent_bounce": True
                },
                {
                    "pattern_name": "MA Crossover",
                    "detected": False,
                    "strength": "None",
                    "crossover_type": "Golden Cross",
                    "sma50": 183.20,
                    "sma200": 184.10,
                    "ma_distance": -0.49
                }
            ],
            "success_rates": {
                "breakout": 62.5,
                "support": 58.3,
                "ma_crossover": 0.0,
                "overall": 40.3
            },
            "recommendation": "BUY",
            "recommendation_reasoning": "Strong breakout detected with volume confirmation and support holding. Dual pattern confirmation suggests good entry point.",
            "alerts": [
                {
                    "title": "📈 Uptrend Detected",
                    "message": "Stock is showing upward momentum. Bullish signal.",
                    "severity": "SUCCESS",
                    "alert_type": "SIGNAL",
                    "timestamp": "2026-03-27T10:30:00",
                    "action": "BUY"
                },
                {
                    "title": "🚀 Breakout Detected",
                    "message": "Price has broken above resistance. Strong bullish signal.",
                    "severity": "CRITICAL",
                    "alert_type": "SIGNAL",
                    "timestamp": "2026-03-27T09:15:00",
                    "action": "BUY"
                },
                {
                    "title": "🚀 Breakout Pattern",
                    "message": "Strong breakout pattern detected (Strong). Price breaking above resistance with volume confirmation.",
                    "severity": "CRITICAL",
                    "alert_type": "PATTERN",
                    "timestamp": "2026-03-27T09:00:00",
                    "action": "BUY"
                },
                {
                    "title": "⚡ Moderate BUY Signal",
                    "message": "Moderate trading opportunity with 68% confidence. Worth monitoring.",
                    "severity": "INFO",
                    "alert_type": "OPPORTUNITY",
                    "timestamp": "2026-03-27T08:00:00",
                    "action": "BUY"
                }
            ]
        }
    },
    "RELIANCE.NS": {
        "success": True,
        "stock": "RELIANCE.NS",
        "date": "2026-03-27",
        "opportunity_level": "Strong",
        "confidence": 75,
        "action": "BUY",
        "signals_triggered": ["Volume Spike", "Breakout"],
        "signal_details": [
            {"name": "Volume Spike", "triggered": True, "strength": "Strong", "reasoning": "1.8x average volume"},
            {"name": "Breakout", "triggered": True, "strength": "Strong", "reasoning": "Breakout with volume"},
            {"name": "Uptrend", "triggered": False, "strength": "-", "reasoning": "Insufficient days"},
            {"name": "Price Surge", "triggered": False, "strength": "-", "reasoning": "1.3% change"},
        ],
        "summary": "High conviction breakout. Strong volume backing with institutional interest.",
        "data_points": 124,
        "chart_patterns": {
            "overall_strength": "Strong",
            "pattern_count": 2,
            "patterns_detected": [
                {
                    "pattern_name": "Breakout",
                    "detected": True,
                    "strength": "Strong",
                    "current_price": 2854.50,
                    "resistance_level": 2793.25,
                    "breakout_margin": 2.19,
                    "volume_confirmation": True
                },
                {
                    "pattern_name": "Support",
                    "detected": False,
                    "strength": "None",
                    "current_price": 2854.50,
                    "support_level": 2680.30,
                    "distance_from_support": 6.49,
                    "recent_bounce": False
                },
                {
                    "pattern_name": "MA Crossover",
                    "detected": True,
                    "strength": "Strong",
                    "crossover_type": "Golden Cross",
                    "sma50": 2820.35,
                    "sma200": 2750.10,
                    "ma_distance": 2.56
                }
            ],
            "success_rates": {
                "breakout": 64.2,
                "support": 45.8,
                "ma_crossover": 58.5,
                "overall": 56.2
            },
            "recommendation": "BUY",
            "recommendation_reasoning": "Multiple bullish signals: Breakout with strong volume + Golden Cross. Highest conviction setup. Strong buy opportunity.",
            "alerts": [
                {
                    "title": "📊 Volume Spike",
                    "message": "Unusual trading volume detected. Increased market interest.",
                    "severity": "WARNING",
                    "alert_type": "SIGNAL",
                    "timestamp": "2026-03-27T11:00:00",
                    "action": "WATCH"
                },
                {
                    "title": "🚀 Breakout Detected",
                    "message": "Price has broken above resistance. Strong bullish signal.",
                    "severity": "CRITICAL",
                    "alert_type": "SIGNAL",
                    "timestamp": "2026-03-27T10:45:00",
                    "action": "BUY"
                },
                {
                    "title": "🚀 Breakout Pattern",
                    "message": "Strong breakout pattern detected (Strong). Price breaking above resistance with volume confirmation.",
                    "severity": "CRITICAL",
                    "alert_type": "PATTERN",
                    "timestamp": "2026-03-27T10:30:00",
                    "action": "BUY"
                },
                {
                    "title": "✨ Golden Cross",
                    "message": "Moving Average Golden Cross detected. Long-term bullish signal.",
                    "severity": "SUCCESS",
                    "alert_type": "PATTERN",
                    "timestamp": "2026-03-27T09:00:00",
                    "action": "BUY"
                },
                {
                    "title": "🎯 Strong BUY Signal",
                    "message": "Strong bullish setup with 75% confidence. High probability trade.",
                    "severity": "CRITICAL",
                    "alert_type": "OPPORTUNITY",
                    "timestamp": "2026-03-27T08:00:00",
                    "action": "BUY"
                },
                {
                    "title": "🌪️ High Volatility Alert",
                    "message": "Multiple strong patterns detected. Market volatility is high. Use tight stops.",
                    "severity": "CRITICAL",
                    "alert_type": "RISK",
                    "timestamp": "2026-03-27T07:30:00",
                    "action": "WATCH"
                }
            ]
        }
    },
}

def get_demo_response(ticker: str) -> Dict:
    """Get demo response for a stock, fallback to AAPL"""
    return DEMO_RESPONSES.get(ticker, DEMO_RESPONSES.get("AAPL"))



# ============================================================================
# FastAPI Setup
# ============================================================================

app = FastAPI(
    title="Stock Analysis API",
    description="Analyze stocks for investment opportunities using technical signals",
    version="1.0.0",
)


from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ============================================================================
# CORS Configuration
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React dev server (common)
        "http://localhost:5173",      # Vite dev server
        "http://127.0.0.1:5173",      # Vite dev server (127.0.0.1)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ============================================================================
# Request/Response Models (Pydantic)
# ============================================================================


class AnalyzeStockRequest(BaseModel):
    """Request model for stock analysis."""

    ticker: str = Field(
        ..., 
        description="Stock ticker symbol (e.g., 'RELIANCE.NS', 'AAPL')",
        example="RELIANCE.NS",
    )


class AnalyzeStockResponse(BaseModel):
    """Successful response model for stock analysis."""

    success: bool = Field(True, description="Whether analysis succeeded")
    stock: str = Field(..., description="Stock ticker symbol")
    date: str = Field(..., description="Date of analysis")
    opportunity_level: str = Field(
        ...,
        description="Investment opportunity level",
        example="Strong",
    )
    confidence: float = Field(..., description="Confidence score (0-100)")
    action: str = Field(
        ..., 
        description="Recommended action (BUY, HOLD, PASS)",
        example="BUY",
    )
    signals_triggered: list = Field(..., description="List of triggered signals")
    signal_details: list = Field(..., description="Detailed signal information")
    summary: str = Field(..., description="Human-readable opportunity summary")
    data_points: int = Field(..., description="Number of trading days analyzed")
    chart_patterns: dict = Field(..., description="Chart patterns analysis with success rates")
    alerts: list = Field(default=[], description="Smart alerts for the stock")
    news_sentiment: dict = Field(..., description="News sentiment analysis with NLP")
    event_signals: dict = Field(..., description="Event signals (price spikes, volume surges)")


class ErrorResponse(BaseModel):
    """Error response model."""

    success: bool = Field(False, description="Whether analysis succeeded")
    error: str = Field(..., description="Error message")
    stock: str = Field(..., description="Stock ticker attempted")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field("healthy", description="API status")
    service: str = Field("Stock Analysis API", description="Service name")


class StockItem(BaseModel):
    """Stock item model."""

    symbol: str = Field(..., description="Stock ticker symbol")
    name: str = Field(..., description="Company name")
    sector: str = Field(..., description="Business sector")
    market: str = Field(..., description="Stock exchange")


class StocksResponse(BaseModel):
    """Response with list of available stocks."""

    count: int = Field(..., description="Number of stocks")
    stocks: list[StockItem] = Field(..., description="List of stock items")



# ============================================================================
# Endpoints
# ============================================================================


@app.get("/", response_model=HealthResponse, tags=["Health"])
async def health_check() -> Dict:
    """
    Health check endpoint.

    Returns:
        Dict: API status and service information

    Example:
        GET http://localhost:8000/
    """
    logger.debug("Health check requested")
    return {"status": "healthy", "service": "Stock Analysis API"}


@app.get("/stocks", response_model=StocksResponse, tags=["Data"])
async def get_stocks() -> Dict:
    """
    Get list of available stocks for analysis.

    Returns curated list of popular stocks across:
    - US Technology (AAPL, MSFT, GOOGL, etc.)
    - US Finance (JPM, V, MA, etc.)
    - US Consumer & Retail (AMZN, WMT, etc.)
    - Indian Markets (RELIANCE.NS, TCS.NS, INFY.NS, etc.)

    Returns:
        Dict: Count and list of available stocks with symbol, name, sector, market

    Example:
        GET http://localhost:8000/stocks

        Response:
        {
            "count": 30,
            "stocks": [
                {
                    "symbol": "AAPL",
                    "name": "Apple Inc.",
                    "sector": "Technology",
                    "market": "NASDAQ"
                },
                ...
            ]
        }
    """
    logger.debug(f"Stocks endpoint called, returning {len(STOCKS)} stocks")
    return {"count": len(STOCKS), "stocks": STOCKS}


@app.post(
    "/analyze-stock",
    response_model=Optional[AnalyzeStockResponse],
    tags=["Analysis"],
)
async def analyze_stock_endpoint(request: AnalyzeStockRequest) -> Dict:
    """
    Analyze a stock for investment opportunities.

    Performs complete technical analysis:
    1. Fetches 6 months of historical data from Yahoo Finance
    2. Detects four trading signals (volume spike, price surge, uptrend, breakout)
    3. Classifies opportunity level (None, Weak, Moderate, Strong)
    4. Generates confidence score and recommendations

    Args:
        request (AnalyzeStockRequest): Request with stock ticker symbol

    Returns:
        Dict: Analysis results with signals, opportunity level, and confidence

    Raises:
        HTTPException: If ticker is invalid or analysis fails

    Example:
        POST /analyze-stock
        {
            "ticker": "RELIANCE.NS"
        }

        Response (200 OK):
        {
            "success": true,
            "stock": "RELIANCE.NS",
            "date": "2025-03-27",
            "opportunity_level": "Strong",
            "confidence": 75.0,
            "action": "BUY",
            "signals_triggered": ["Breakout", "Volume Spike"],
            "signal_details": [...],
            "summary": "High conviction breakout...",
            "data_points": 126
        }
    """
    ticker = request.ticker.strip().upper()

    logger.info(f"Analyze stock endpoint called for {ticker}")

    try:
        # Call analysis service
        result = analyze_stock(ticker)

        # Check if analysis was successful
        if not result.get("success", False):
            logger.warning(f"Analysis failed for {ticker}: {result.get('error')}")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": result.get("error", "Analysis failed"),
                    "stock": ticker,
                },
            )

        logger.info(f"Successfully analyzed {ticker}")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal server error", "stock": ticker},
        )


@app.post("/batch-analyze", tags=["Analysis"])
async def batch_analyze_endpoint(tickers: list[str]) -> Dict[str, Dict]:
    """
    Analyze multiple stocks in batch.

    Args:
        tickers (list[str]): List of stock ticker symbols

    Returns:
        Dict: Analysis results for each ticker

    Example:
        POST /batch-analyze
        ["RELIANCE.NS", "TCS.NS", "AAPL"]

        Response:
        {
            "RELIANCE.NS": {...},
            "TCS.NS": {...},
            "AAPL": {...}
        }
    """
    logger.info(f"Batch analysis requested for {len(tickers)} stocks")

    if not tickers or len(tickers) == 0:
        raise HTTPException(status_code=400, detail="Ticker list cannot be empty")

    if len(tickers) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 stocks per batch. Please split into multiple requests.",
        )

    try:
        results = batch_analyze_stocks(tickers)
        logger.info(f"Batch analysis completed for {len(tickers)} stocks")
        return results
    except Exception as e:
        logger.error(f"Error in batch analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Batch analysis failed")


# ============================================================================
# API Documentation and Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 80)
    print("STOCK ANALYSIS API - Starting Server")
    print("=" * 80)
    print("\n📍 API Running at: http://localhost:8000")
    print("📖 API Docs at: http://localhost:8000/docs")
    print("📊 Alternative Docs: http://localhost:8000/redoc")
    print("\n" + "=" * 80)
    print("\nExample curl request:")
    print('-' * 80)
    print("""
curl -X POST "http://localhost:8000/analyze-stock" \\
  -H "Content-Type: application/json" \\
  -d '{
    "ticker": "RELIANCE.NS"
  }'
    """)
    print("-" * 80)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
    
    
    

from services.portfolio import analyze_portfolio

class PortfolioResponse(BaseModel):
    success: bool
    portfolio_summary: dict = None
    stock_breakdown: list = None
    weaknesses: list = None
    recommendations: dict = None
    insight: str = None
    # Legacy fields for backwards compatibility
    portfolio_size: int = None
    risk_score: float = None
    avg_correlation: float = None
    diversification: str = None
    rebalance_suggestion: str = None
    error: str = None


class PortfolioRequest(BaseModel):
    tickers: list[str] = Field(..., description="List of stock tickers", example=["AAPL", "MSFT"])


@app.post(
    "/portfolio-health",
    response_model=PortfolioResponse,
    tags=["Portfolio"],
)
async def portfolio_health_endpoint(request: PortfolioRequest):

    try:
        result = analyze_portfolio(request.tickers)

        if not result.get("success"):
            logger.error(f"Portfolio analysis failed: {result.get('error')}")
            raise HTTPException(status_code=400, detail=result.get("error"))

        return result

    except HTTPException:
        raise  # Re-raise HTTPExceptions
    except Exception as e:
        error_msg = f"Portfolio analysis error: {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )


class PortfolioFitRequest(BaseModel):
    tickers: list[str] = Field(..., description="Current portfolio tickers")
    test_stock: str = Field(..., description="Stock to analyze fit for")


class PortfolioFitResponse(BaseModel):
    success: bool
    stock: str = None
    fit_score: int = None
    fit_level: str = None
    reasons: list[str] = None
    action: str = None
    confidence: int = None
    error: str = None


@app.post(
    "/portfolio-fit",
    response_model=PortfolioFitResponse,
    tags=["Portfolio"],
)
async def portfolio_fit_endpoint(request: PortfolioFitRequest):
    """
    💡 Analyze how well a new stock fits with the current portfolio.
    Provides fit score, recommendations, and reasons.
    """
    try:
        from services.portfolio import analyze_stock_fit
        
        result = analyze_stock_fit(request.tickers, request.test_stock)
        
        if not result.get("success"):
            logger.error(f"Stock fit analysis failed: {result.get('error')}")
            raise HTTPException(status_code=400, detail=result.get("error"))

        return result

    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Portfolio fit analysis error: {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )
        
from fastapi.responses import FileResponse
from fastapi import Query, HTTPException
from services.video_engine import generate_market_video, generate_structured_video_report, VIDEOS_DIR


@app.get("/generate-video")
async def generate_video(ticker: str = Query(...)):
    """
    Generate AI video for selected stock (Legacy Endpoint)
    
    Returns a simple MP4 with stock chart and price narration.
    For advanced video with insights, use /generate-structured-video instead.
    """

    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker is required")

    try:
        logger.info(f"Generating legacy video for {ticker}")
        video_path = generate_market_video(ticker)
        
        if not os.path.exists(video_path):
            raise HTTPException(
                status_code=500, 
                detail=f"Video file not created: {video_path}"
            )

        logger.info(f"✓ Video generated successfully: {video_path}")
        
        return FileResponse(
            path=video_path,
            media_type="video/mp4",
            filename=f"{ticker}_video.mp4"
        )

    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Video generation failed: {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


@app.get("/get-video/{filename}", tags=["Video"])
async def get_video(filename: str):
    """
    Serve a generated video file from the videos/ directory.
    
    Args:
        filename: Name of the video file (e.g., "video_MSFT_abc123.mp4")
        
    Returns:
        FileResponse: MP4 video file
        
    Example:
        GET /get-video/video_MSFT_abc123.mp4
    """
    try:
        import os
        from pathlib import Path
        
        # Security: validate filename to prevent path traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        video_path = os.path.join(VIDEOS_DIR, filename)
        
        # Verify file exists and is in the correct directory
        if not os.path.exists(video_path):
            raise HTTPException(status_code=404, detail=f"Video file not found: {filename}")
        
        if not os.path.isfile(video_path):
            raise HTTPException(status_code=400, detail=f"Invalid path: {filename}")
        
        logger.info(f"Serving video file: {filename}")
        return FileResponse(
            path=video_path,
            media_type="video/mp4",
            filename=filename
        )
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error serving video: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


class StructuredVideoRequest(BaseModel):
    """Request model for structured video report."""
    ticker: str = Field(..., description="Stock ticker symbol", example="AAPL")


class StructuredVideoResponse(BaseModel):
    """Response model for structured video report."""
    success: bool = Field(..., description="Whether video generation succeeded")
    ticker: str = Field(..., description="Stock ticker")
    video_path: str = Field(..., description="Path to generated MP4 video")
    frames: list = Field(..., description="List of video frames with content")
    insights: dict = Field(..., description="Extracted AI insights")
    recommendation: dict = Field(..., description="Final recommendation")
    generated_at: str = Field(..., description="ISO timestamp")
    summary: dict = Field(..., description="High-level summary")


@app.post(
    "/generate-structured-video",
    response_model=StructuredVideoResponse,
    tags=["Video"],
)
async def generate_structured_video_endpoint(request: StructuredVideoRequest) -> Dict:
    """
    Generate AI-driven structured video report with intelligent insights.
    
    Creates a professional video with:
    - **Frame 1 (Analysis)**: Trend direction, signals detected, momentum strength, short outlook
    - **Frame 2 (News)**: Key market drivers with top 2-3 headlines
    - **Frame 3 (Recommendation)**: BUY/HOLD/SELL with confidence and reasoning
    
    Each frame includes:
    - High-quality visual overlay with text
    - AI-generated narration via text-to-speech
    - Structured metadata for downstream processing
    
    Args:
        request (StructuredVideoRequest): Request with stock ticker
        
    Returns:
        Dict: Video path, frame details, insights, recommendation, and summary
        
    Example:
        POST /generate-structured-video
        {
            "ticker": "AAPL"
        }
        
        Response:
        {
            "success": true,
            "ticker": "AAPL",
            "video_path": "video_AAPL_abc123.mp4",
            "frames": [
                {
                    "type": "analysis",
                    "title": "AAPL AI Insights",
                    "image": "frame_insight_xyz.png",
                    "narration": "Based on current market analysis...",
                    "content": {...}
                },
                {
                    "type": "news",
                    "title": "AAPL Market Drivers",
                    "content": {"headlines": [...]}
                },
                {
                    "type": "recommendation",
                    "title": "AAPL Recommendation",
                    "content": {
                        "action": "BUY",
                        "confidence": "75%",
                        "reasons": [...]
                    }
                }
            ],
            "insights": {
                "trend": "🟢 BULLISH",
                "trend_direction": "Uptrend",
                "signal_detected": "Breakout, Volume Spike",
                "momentum_strength": "STRONG (75%)",
                "short_outlook": "BULLISH - Entry opportunity"
            },
            "recommendation": {
                "action": "BUY",
                "action_emoji": "🟢",
                "confidence": "75%",
                "reasons": ["Breakout pattern confirmed", "Positive sentiment", "Favorable opportunity"]
            },
            "summary": {
                "trend": "🟢 BULLISH",
                "action": "BUY",
                "confidence": "75%",
                "key_reasons": [...]
            }
        }
    """
    ticker = request.ticker.strip().upper()
    
    logger.info(f"Structured video generation requested for {ticker}")
    
    try:
        # First, analyze the stock
        logger.debug(f"Analyzing stock {ticker}...")
        analysis = analyze_stock(ticker)
        
        if not analysis.get("success", False):
            logger.warning(f"Analysis failed for {ticker}: {analysis.get('error')}")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"Analysis failed: {analysis.get('error')}",
                    "stock": ticker,
                }
            )
        
        # Generate structured video report
        logger.debug(f"Generating structured video for {ticker}...")
        report = generate_structured_video_report(ticker, analysis)
        
        if not report.get("success", False):
            logger.error(f"Video generation failed for {ticker}: {report.get('error')}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": f"Video generation failed: {report.get('error')}",
                    "stock": ticker,
                }
            )
        
        logger.info(f"✓ Successfully generated structured video for {ticker}: {report['video_path']}")
        return report
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Structured video generation error for {ticker}: {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail={"error": error_msg, "stock": ticker}
        )


# ============================================================================
# Chat Endpoint
# ============================================================================

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message for the financial assistant", example="What stocks should I buy?")


class ChatResponse(BaseModel):
    success: bool
    reply: str
    type: str = Field("general", description="Query type: stock, portfolio, comparison, general")
    suggestions: Optional[list[str]] = None
    ticker: Optional[str] = None
    tickers: Optional[list[str]] = None


@app.post(
    "/chat",
    response_model=ChatResponse,
    tags=["Chat"],
)
async def chat_endpoint(request: ChatRequest) -> Dict:
    """
    AI-Powered Financial Chat Assistant.
    
    Uses Gemini 2.5 Flash AI to provide intelligent investment advice.
    
    Supports:
    - Stock Analysis: "Should I buy AAPL?"
    - Stock Comparison: "AAPL vs MSFT?"
    - Portfolio Review: "Is my portfolio good?"
    - General Knowledge: "What is a breakout?"
    
    Features:
    - Automatic stock ticker extraction
    - Real-time stock analysis integration
    - AI-generated contextual responses
    - Investment recommendations
    
    Args:
        request (ChatRequest): User message containing investment question
        
    Returns:
        ChatResponse: AI-generated reply with type and suggestions
        
    Example:
        POST /chat
        {
            "message": "Should I buy Apple stock?"
        }
        
        Response (200 OK):
        {
            "success": true,
            "reply": "Based on AAPL analysis...",
            "type": "stock",
            "ticker": "AAPL",
            "suggestions": ["Deep analysis", "Compare stocks", ...]
        }
    """
    try:
        message = request.message.strip()
        
        if not message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        logger.info(f"Chat request received: {message[:60]}...")
        
        result = process_chat_message(message)

        if not result.get("success"):
            logger.error(f"Chat processing failed: {result.get('error')}")
            raise HTTPException(status_code=400, detail=result.get("error"))

        # Format response with all fields
        response_data = {
            "success": result.get("success", True),
            "reply": result.get("reply", "Unable to generate response"),
            "type": result.get("type", "general"),
            "suggestions": result.get("suggestions", [])
        }
        
        # Add optional fields if present
        if result.get("ticker"):
            response_data["ticker"] = result.get("ticker")
        if result.get("tickers"):
            response_data["tickers"] = result.get("tickers")
        
        logger.info(f"Chat response generated successfully (type: {response_data['type']})")
        return response_data

    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Chat error: {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )
