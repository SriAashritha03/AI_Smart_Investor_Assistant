"""
Stock Data Fetcher Module

A production-ready module for fetching historical stock data using yfinance.
Provides clean, validated data with comprehensive error handling and logging.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
import yfinance as yf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Configuration
DEFAULT_PERIOD = "6mo"  # Fetch at least 6 months of data
REQUIRED_COLUMNS = ["Open", "Close", "High", "Low", "Volume"]
MIN_DATA_POINTS = 100  # Ensure we have meaningful data


def validate_ticker(ticker: str) -> bool:
    """
    Validate if a ticker symbol is valid by attempting to fetch basic info.

    Args:
        ticker (str): The ticker symbol to validate (e.g., 'RELIANCE.NS', 'AAPL').

    Returns:
        bool: True if ticker is valid, False otherwise.

    Raises:
        ValueError: If ticker is empty or None.
    """
    if not ticker or not isinstance(ticker, str):
        raise ValueError("Ticker must be a non-empty string.")

    ticker = ticker.strip().upper()

    try:
        stock = yf.Ticker(ticker)
        # Attempt to fetch info to validate ticker exists
        _ = stock.info
        logger.info(f"Ticker '{ticker}' validated successfully.")
        return True
    except Exception as e:
        logger.warning(f"Ticker validation failed for '{ticker}': {str(e)}")
        return False


def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate stock data DataFrame.

    Ensures:
    - Flattens MultiIndex columns (yfinance returns MultiIndex for single ticker)
    - Only required columns are present
    - No NaN values in required columns
    - Data is sorted by date in ascending order
    - Index is a proper datetime index

    Args:
        df (pd.DataFrame): Raw stock data from yfinance.

    Returns:
        pd.DataFrame: Cleaned stock data with required columns only.

    Raises:
        ValueError: If data is empty or missing required columns.
    """
    if df.empty:
        raise ValueError("Stock data is empty. No data available for the ticker.")

    # Flatten MultiIndex columns (yfinance returns MultiIndex: (ColumnName, Ticker))
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        logger.debug("MultiIndex columns flattened.")

    # Check if required columns exist
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}. "
            f"Available columns: {list(df.columns)}"
        )

    # Select only required columns
    df = df[REQUIRED_COLUMNS].copy()

    # Remove rows with NaN values
    df = df.dropna()

    if df.empty:
        raise ValueError(
            "No valid data after cleaning. All rows contained NaN values."
        )

    # Ensure index is datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    # Sort by date in ascending order
    df = df.sort_index(ascending=True)

    logger.info(f"Data cleaned successfully. Shape: {df.shape}")
    return df


def get_stock_data(
    ticker: str, period: str = DEFAULT_PERIOD, interval: str = "1d"
) -> pd.DataFrame:
    """
    Fetch historical stock data for a given ticker.

    Retrieves historical OHLCV (Open, High, Low, Close, Volume) data from Yahoo Finance.
    Data is cleaned, validated, and returned as a pandas DataFrame with proper datetime index.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'RELIANCE.NS', 'AAPL', 'GOOGL').
                     Must include market suffix for international stocks (e.g., .NS for NSE).
        period (str, optional): Time period for historical data. Default is '6mo'.
                               Valid periods: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'.
        interval (str, optional): Data interval frequency. Default is '1d' (daily).
                                 Valid intervals: '1m', '5m', '15m', '30m', '60m', '1d', '1wk', '1mo'.

    Returns:
        pd.DataFrame: Cleaned stock data with columns: Open, Close, High, Low, Volume.
                     Index is a DatetimeIndex representing trading dates.

    Raises:
        ValueError: If ticker is invalid, empty, or no data is available.
        Exception: For network or data retrieval errors.

    Example:
        >>> df = get_stock_data('RELIANCE.NS')
        >>> print(df.head())
        >>> print(df.info())
    """
    logger.info(f"Fetching stock data for ticker: {ticker}, period: {period}")

    # Validate ticker
    if not validate_ticker(ticker):
        raise ValueError(
            f"Invalid ticker symbol: '{ticker}'. "
            "Please verify the ticker and market suffix (e.g., .NS for NSE)."
        )

    try:
        # Fetch data from Yahoo Finance
        logger.info(f"Downloading data from Yahoo Finance...")
        stock_data = yf.download(
            ticker, period=period, interval=interval, progress=False
        )

        # Clean and validate data
        cleaned_data = clean_stock_data(stock_data)

        # Validate minimum data points
        if len(cleaned_data) < MIN_DATA_POINTS:
            logger.warning(
                f"Limited data retrieved: {len(cleaned_data)} rows. "
                "Consider using a longer period for more comprehensive analysis."
            )

        logger.info(
            f"Successfully fetched stock data for {ticker}. "
            f"Total records: {len(cleaned_data)}, "
            f"Date range: {cleaned_data.index[0].date()} to {cleaned_data.index[-1].date()}"
        )

        return cleaned_data

    except Exception as e:
        logger.error(f"Error fetching stock data for {ticker}: {str(e)}")
        raise


def get_stock_data_custom_dates(
    ticker: str, start_date: str, end_date: str, interval: str = "1d"
) -> pd.DataFrame:
    """
    Fetch historical stock data for a given ticker within a custom date range.

    Provides flexibility to retrieve data for specific date ranges instead of predefined periods.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'RELIANCE.NS', 'AAPL').
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        interval (str, optional): Data interval frequency. Default is '1d' (daily).

    Returns:
        pd.DataFrame: Cleaned stock data with columns: Open, Close, High, Low, Volume.

    Raises:
        ValueError: If date format is invalid, ticker is invalid, or no data is available.

    Example:
        >>> df = get_stock_data_custom_dates('RELIANCE.NS', '2024-01-01', '2024-12-31')
        >>> print(df.head())
    """
    logger.info(
        f"Fetching stock data for {ticker} from {start_date} to {end_date}"
    )

    # Validate dates
    try:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
    except Exception as e:
        raise ValueError(
            f"Invalid date format. Use 'YYYY-MM-DD' format. Error: {str(e)}"
        )

    if start >= end:
        raise ValueError("Start date must be before end date.")

    # Validate ticker
    if not validate_ticker(ticker):
        raise ValueError(f"Invalid ticker symbol: '{ticker}'")

    try:
        # Fetch data from Yahoo Finance
        logger.info("Downloading data from Yahoo Finance...")
        stock_data = yf.download(
            ticker, start=start_date, end=end_date, interval=interval, progress=False
        )

        # Clean and validate data
        cleaned_data = clean_stock_data(stock_data)

        logger.info(
            f"Successfully fetched stock data for {ticker}. "
            f"Total records: {len(cleaned_data)}"
        )

        return cleaned_data

    except Exception as e:
        logger.error(f"Error fetching stock data for {ticker}: {str(e)}")
        raise


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    try:
        # Example 1: Fetch 6 months of data for RELIANCE (NSE)
        print("=" * 70)
        print("Example 1: Fetching 6 months of RELIANCE stock data (NSE)")
        print("=" * 70)
        reliance_data = get_stock_data("RELIANCE.NS")
        print("\nData Shape:", reliance_data.shape)
        print("\nFirst 5 rows:")
        print(reliance_data.head())
        print("\nLast 5 rows:")
        print(reliance_data.tail())
        print("\nData Summary Statistics:")
        print(reliance_data.describe())
        print("\nData Info:")
        print(reliance_data.info())

        # Example 2: Fetch data for US stock (APPLE)
        print("\n" + "=" * 70)
        print("Example 2: Fetching 6 months of Apple stock data (NASDAQ)")
        print("=" * 70)
        apple_data = get_stock_data("AAPL")
        print("\nData Shape:", apple_data.shape)
        print("\nFirst 5 rows:")
        print(apple_data.head())

        # Example 3: Fetch custom date range
        print("\n" + "=" * 70)
        print("Example 3: Fetching custom date range (1 year)")
        print("=" * 70)
        custom_data = get_stock_data_custom_dates(
            "RELIANCE.NS", "2024-01-01", "2024-12-31"
        )
        print("\nData Shape:", custom_data.shape)
        print("\nFirst 5 rows:")
        print(custom_data.head())
        print("\nDate range:", custom_data.index[0].date(), "to", custom_data.index[-1].date())

        # Example 4: Error handling - invalid ticker
        print("\n" + "=" * 70)
        print("Example 4: Error handling - Invalid ticker")
        print("=" * 70)
        try:
            invalid_data = get_stock_data("INVALID_TICKER_XYZ")
        except ValueError as e:
            print(f"Caught expected error: {e}")

    except Exception as e:
        logger.error(f"Unexpected error in examples: {str(e)}")
        print(f"Error: {str(e)}")
