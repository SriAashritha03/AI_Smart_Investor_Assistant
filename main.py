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
    portfolio_size: int
    risk_score: float
    avg_correlation: float
    diversification: str
    rebalance_suggestion: str


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
        
from fastapi.responses import FileResponse
from fastapi import Query, HTTPException
from services.video_engine import generate_market_video


@app.get("/generate-video")
async def generate_video(ticker: str = Query(...)):
    """
    Generate AI video for selected stock
    """

    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker is required")

    try:
        video_path = generate_market_video(ticker)

        return FileResponse(
            path=video_path,
            media_type="video/mp4",
            filename="video.mp4"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))