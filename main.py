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
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from services.analyzer import analyze_stock, batch_analyze_stocks

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ============================================================================
# FastAPI Setup
# ============================================================================

app = FastAPI(
    title="Stock Analysis API",
    description="Analyze stocks for investment opportunities using technical signals",
    version="1.0.0",
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


class ErrorResponse(BaseModel):
    """Error response model."""

    success: bool = Field(False, description="Whether analysis succeeded")
    error: str = Field(..., description="Error message")
    stock: str = Field(..., description="Stock ticker attempted")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field("healthy", description="API status")
    service: str = Field("Stock Analysis API", description="Service name")


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
