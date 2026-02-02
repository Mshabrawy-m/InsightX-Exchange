"""
Trading Analysis Module
Handles stock data fetching, technical indicators, and trend analysis

Design Choices:
- yfinance API chosen for free, reliable stock data access
- Modular indicator calculations for maintainability and testing
- Plotly for interactive charts to enhance user experience
- Comprehensive error handling for robust data processing
- Trend classification system for educational risk assessment
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.config import get_trading_config, TRADING_DAYS_PER_YEAR

class TradingAnalyzer:
    """
    Class for comprehensive trading analysis
    
    Design Choices:
    - Encapsulated class for state management and configuration
    - Method separation for single responsibility principle
    - Type hints for code clarity and IDE support
    - Comprehensive return structures for downstream processing
    """
    
    def __init__(self):
        """
        Initialize trading analyzer with configuration
        
        Design Choice: Configuration injection allows for testing and flexibility
        """
        self.config = get_trading_config()
    
    def fetch_stock_data(self, ticker: str, period: str = None) -> pd.DataFrame:
        """
        Fetch stock data from Yahoo Finance
        
        Design Choice: yfinance provides free, reliable data with good historical coverage
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        
        Returns:
            DataFrame with OHLCV data
        """
        if period is None:
            period = self.config['default_period']
        
        # Normalize ticker and handle common variations
        ticker = self._normalize_ticker(ticker)
        
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            
            if data.empty:
                raise ValueError(f"No data found for ticker {ticker}")
            
            return data
            
        except Exception as e:
            raise Exception(f"Error fetching stock data: {str(e)}")
    
    def _normalize_ticker(self, ticker: str) -> str:
        """
        Normalize ticker symbol and handle common variations
        
        Args:
            ticker: Input ticker symbol
            
        Returns:
            Normalized ticker symbol
        """
        # Common ticker mappings
        ticker_mappings = {
            'GOOGLE': 'GOOGL',
            'GOOG': 'GOOGL',
            'FACEBOOK': 'META',
            'FB': 'META',
            'AMAZON': 'AMZN',
            'MICROSOFT': 'MSFT',
            'APPLE': 'AAPL',
            'TESLA': 'TSLA',
            'NETFLIX': 'NFLX',
            'BITCOIN': 'BTC-USD',
            'BTC': 'BTC-USD',
            'ETHEREUM': 'ETH-USD',
            'ETH': 'ETH-USD'
        }
        
        # Clean and normalize ticker
        ticker = ticker.upper().strip()
        
        # Check if ticker needs mapping
        if ticker in ticker_mappings:
            ticker = ticker_mappings[ticker]
        
        return ticker
    
    def calculate_sma(self, prices: pd.Series, window: int) -> pd.Series:
        """
        Calculate Simple Moving Average
        
        Args:
            prices: Price series
            window: Moving average window
        
        Returns:
            Series with SMA values
        """
        return prices.rolling(window=window).mean()
    
    def calculate_ema(self, prices: pd.Series, window: int) -> pd.Series:
        """
        Calculate Exponential Moving Average
        
        Args:
            prices: Price series
            window: EMA window
        
        Returns:
            Series with EMA values
        """
        return prices.ewm(span=window).mean()
    
    def calculate_rsi(self, data: pd.DataFrame, window: int = None) -> pd.Series:
        """
        Calculate Relative Strength Index
        
        Args:
            data: Stock data with Close prices
            window: RSI calculation window
        
        Returns:
            Series with RSI values
        """
        if window is None:
            window = self.config['rsi_period']
        
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_macd(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            data: Stock data with Close prices
        
        Returns:
            Dictionary with MACD, Signal, and Histogram series
        """
        close = data['Close']
        
        # Calculate MACD line
        ema_fast = self.calculate_ema(close, self.config['macd_fast'])
        ema_slow = self.calculate_ema(close, self.config['macd_slow'])
        macd_line = ema_fast - ema_slow
        
        # Calculate Signal line
        signal_line = self.calculate_ema(macd_line, self.config['macd_signal'])
        
        # Calculate Histogram
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def calculate_volatility(self, data: pd.DataFrame, window: int = 20) -> float:
        """
        Calculate price volatility
        
        Args:
            data: Stock data with Close prices
            window: Volatility calculation window
        
        Returns:
            Volatility as a decimal
        """
        returns = data['Close'].pct_change().dropna()
        volatility = returns.rolling(window=window).std().iloc[-1]
        
        # Annualize volatility
        volatility_annualized = volatility * np.sqrt(TRADING_DAYS_PER_YEAR)
        
        return volatility_annualized
    
    def classify_trend(self, data: pd.DataFrame, volatility: float) -> Dict[str, str]:
        """
        Classify market trend based on price action and volatility
        
        Args:
            data: Stock data with Close prices
            volatility: Current volatility level
        
        Returns:
            Dictionary with trend classification and signal
        """
        close = data['Close']
        
        # Calculate moving averages
        ma_short = self.calculate_sma(close, self.config['ma_short'])
        ma_long = self.calculate_sma(close, self.config['ma_long'])
        
        # Current price relative to moving averages
        current_price = close.iloc[-1]
        current_ma_short = ma_short.iloc[-1]
        current_ma_long = ma_long.iloc[-1]
        
        # Determine trend
        if current_price > current_ma_short > current_ma_long:
            trend = "Bullish"
            signal = "Strong uptrend - Price above both moving averages"
        elif current_price > current_ma_long and current_price < current_ma_short:
            trend = "Neutral-Bullish"
            signal = "Moderate uptrend - Price between moving averages"
        elif current_price < current_ma_short < current_ma_long:
            trend = "Bearish"
            signal = "Strong downtrend - Price below both moving averages"
        else:
            trend = "Neutral-Bearish"
            signal = "Moderate downtrend - Price between moving averages"
        
        # Adjust signal based on volatility
        if volatility > self.config.get('max_volatility_threshold', 0.3):
            signal += " (High volatility - increased risk)"
        elif volatility > 0.2:
            signal += " (Moderate volatility)"
        else:
            signal += " (Low volatility)"
        
        return {
            'trend': trend,
            'signal': signal
        }
    
    def create_price_chart(self, data: pd.DataFrame, ticker: str) -> go.Figure:
        """
        Create interactive price chart with volume
        
        Args:
            data: Stock data with OHLCV
            ticker: Stock ticker symbol
        
        Returns:
            Plotly figure object
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=(f'{ticker} Price', 'Volume'),
            row_width=[0.2, 0.7]
        )
        
        # Add candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price'
            ),
            row=1, col=1
        )
        
        # Add volume bars
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data['Volume'],
                name='Volume',
                marker_color='rgba(0,0,255,0.3)'
            ),
            row=2, col=1
        )
        
        # Update layout
        fig.update_layout(
            title=f'{ticker} Stock Price and Volume',
            yaxis_title='Price ($)',
            xaxis_rangeslider_visible=False,
            height=600
        )
        
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        
        return fig
    
    def create_technical_chart(self, data: pd.DataFrame, ticker: str, indicators: Dict) -> go.Figure:
        """
        Create technical indicators chart
        
        Args:
            data: Stock data
            ticker: Stock ticker symbol
            indicators: Dictionary with calculated indicators
        
        Returns:
            Plotly figure object
        """
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(
                f'{ticker} Price with Moving Averages',
                'RSI',
                'MACD'
            )
        )
        
        # Price and moving averages
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Close'],
                name='Close Price',
                line=dict(color='blue')
            ),
            row=1, col=1
        )
        
        if 'sma_short' in indicators:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=indicators['sma_short'],
                    name=f'SMA {self.config["ma_short"]}',
                    line=dict(color='orange')
                ),
                row=1, col=1
            )
        
        if 'sma_long' in indicators:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=indicators['sma_long'],
                    name=f'SMA {self.config["ma_long"]}',
                    line=dict(color='red')
                ),
                row=1, col=1
            )
        
        # RSI
        if 'rsi' in indicators:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=indicators['rsi'],
                    name='RSI',
                    line=dict(color='purple')
                ),
                row=2, col=1
            )
            
            # Add RSI reference lines
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # MACD
        if 'macd' in indicators:
            macd_data = indicators['macd']
            
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=macd_data['macd'],
                    name='MACD',
                    line=dict(color='blue')
                ),
                row=3, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=macd_data['signal'],
                    name='Signal',
                    line=dict(color='red')
                ),
                row=3, col=1
            )
            
            fig.add_trace(
                go.Bar(
                    x=data.index,
                    y=macd_data['histogram'],
                    name='Histogram',
                    marker_color='gray'
                ),
                row=3, col=1
            )
        
        fig.update_layout(
            title=f'{ticker} Technical Analysis',
            height=800,
            showlegend=True
        )
        
        return fig
    
    def analyze_stock(self, ticker: str, period: str = None) -> Dict:
        """
        Perform comprehensive stock analysis
        
        Args:
            ticker: Stock ticker symbol
            period: Analysis period
        
        Returns:
            Dictionary with all analysis results
        """
        try:
            # Fetch data
            data = self.fetch_stock_data(ticker, period)
            
            # Calculate indicators
            indicators = {}
            
            # Moving averages
            indicators['sma_short'] = self.calculate_sma(data['Close'], self.config['ma_short'])
            indicators['sma_long'] = self.calculate_sma(data['Close'], self.config['ma_long'])
            
            # RSI
            indicators['rsi'] = self.calculate_rsi(data)
            
            # MACD
            indicators['macd'] = self.calculate_macd(data)
            
            # Volatility
            volatility = self.calculate_volatility(data)
            
            # Trend classification
            trend_info = self.classify_trend(data, volatility)
            
            # Create charts
            price_chart = self.create_price_chart(data, ticker)
            technical_chart = self.create_technical_chart(data, ticker, indicators)
            
            # Compile results
            results = {
                'ticker': ticker,
                'period': period or self.config['default_period'],
                'data': data,
                'indicators': indicators,
                'volatility': volatility,
                'trend_info': trend_info,
                'price_chart': price_chart,
                'technical_chart': technical_chart,
                'latest_values': {
                    'price': data['Close'].iloc[-1],
                    'volume': data['Volume'].iloc[-1],
                    'rsi': indicators['rsi'].iloc[-1] if not indicators['rsi'].empty else None,
                    'macd': indicators['macd']['macd'].iloc[-1] if not indicators['macd']['macd'].empty else None,
                    'signal': indicators['macd']['signal'].iloc[-1] if not indicators['macd']['signal'].empty else None,
                    'macd_signal': 'Bullish' if indicators['macd']['macd'].iloc[-1] > indicators['macd']['signal'].iloc[-1] else 'Bearish'
                },
                'statistics': {
                    'current_price': data['Close'].iloc[-1],
                    'price_change_pct': ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100,
                    'avg_volume': data['Volume'].mean(),
                    'max_price': data['Close'].max(),
                    'min_price': data['Close'].min(),
                    'volatility': volatility
                }
            }
            
            return results
            
        except Exception as e:
            raise Exception(f"Error in stock analysis: {str(e)}")
