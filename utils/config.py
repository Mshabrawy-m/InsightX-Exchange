"""
Configuration file for InsightX Exchange
Contains API keys, settings, and constants for the application
"""

# API Configuration
OPENAI_API_KEY = "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"
OPENAI_BASE_URL = "https://api.groq.com/openai/v1"

# Default Model Configuration
DEFAULT_MODEL = "openai/gpt-oss-120b"
TEMPERATURE = 1.0
MAX_TOKENS = 8192

# Trading Analysis Settings
DEFAULT_STOCK_TICKER = "AAPL"
DEFAULT_PERIOD = "1y"
TRADING_DAYS_PER_YEAR = 252

# Technical Indicators Parameters
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
MA_SHORT = 20
MA_LONG = 50

# Marketing Analysis Settings
EXPECTED_COLUMNS = {
    'budget': 'Budget',
    'clicks': 'Clicks', 
    'conversions': 'Conversions',
    'revenue': 'Revenue'
}

# Chart Configuration
CHART_THEME = "plotly_white"
CHART_HEIGHT = 400
CHART_WIDTH = 800

# Application Settings
APP_TITLE = "InsightX Exchange"
APP_DESCRIPTION = "Marketing & Trading Analytics Platform"
APP_VERSION = "1.0.0"

# File Upload Settings
MAX_FILE_SIZE = 200  # MB
ALLOWED_EXTENSIONS = ['csv']

# Report Generation
REPORT_LOGO_PATH = "data/logo.png"
DEFAULT_FONT = "Arial"

# Cache Settings
CACHE_TTL = 3600  # seconds (1 hour)

# Language Support
SUPPORTED_LANGUAGES = ['en', 'ar']
DEFAULT_LANGUAGE = 'en'

# Risk Management
MAX_VOLATILITY_THRESHOLD = 0.3  # 30%
RISK_WARNING_LEVELS = {
    'low': 0.15,
    'medium': 0.25,
    'high': 0.35
}


def get_trading_config():
    """
    Get trading analysis configuration
    
    Returns:
        dict: Trading analysis parameters
    """
    return {
        "default_ticker": DEFAULT_STOCK_TICKER,
        "default_period": DEFAULT_PERIOD,
        "rsi_period": RSI_PERIOD,
        "macd_fast": MACD_FAST,
        "macd_slow": MACD_SLOW,
        "macd_signal": MACD_SIGNAL,
        "ma_short": MA_SHORT,
        "ma_long": MA_LONG
    }


def get_marketing_config():
    """
    Get marketing analysis configuration
    
    Returns:
        dict: Marketing analysis parameters
    """
    return {
        "expected_columns": EXPECTED_COLUMNS,
        "max_file_size": MAX_FILE_SIZE,
        "allowed_extensions": ALLOWED_EXTENSIONS
    }
