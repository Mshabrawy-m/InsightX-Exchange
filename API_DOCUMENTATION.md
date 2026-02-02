# InsightX Exchange - API Documentation

## 📋 **Overview**
InsightX Exchange is a comprehensive marketing and trading analytics platform that provides real-time data analysis, technical indicators, and comprehensive reporting capabilities.

## 🚀 **Getting Started**

### **Installation**
```bash
pip install -r requirements.txt
streamlit run app.py
```

### **Access Points**
- **Main Application**: `http://localhost:8501`
- **Trading Analysis**: `/Trading_Analysis`
- **Marketing Analysis**: `/Marketing_Analysis`
- **Report Generator**: `/Report_Generator`

## 📊 **Core APIs**

### **1. Trading Analysis API**

#### **Endpoint**: Internal TradingAnalyzer

**Description**: Provides comprehensive stock analysis with technical indicators

**Parameters**:
- `ticker` (string): Stock symbol (e.g., "AAPL", "MSFT", "GOOGL")
- `period` (string): Time period ("1mo", "3mo", "6mo", "1y", "2y", "5y")

**Returns**:
```python
{
    'ticker': 'AAPL',
    'period': '1y',
    'latest_values': {
        'price': 150.25,
        'rsi': 65.43,
        'macd': 2.15,
        'signal': 1.85
    },
    'statistics': {
        'avg_volume': 50000000,
        'max_price': 180.50,
        'min_price': 120.75,
        'price_change_pct': 15.2
    },
    'volatility': 0.25,
    'trend_info': {
        'trend': 'Bullish',
        'signal': 'BUY'
    },
    'price_chart': plotly_figure,
    'technical_chart': plotly_figure
}
```

**Usage Example**:
```python
from analysis.trading import TradingAnalyzer

analyzer = TradingAnalyzer()
results = analyzer.analyze_stock("AAPL", "1y")
print(f"Current Price: ${results['latest_values']['price']:.2f}")
print(f"RSI: {results['latest_values']['rsi']:.2f}")
print(f"Trend: {results['trend_info']['trend']}")
```

#### **Technical Indicators Available**:
- **RSI** (Relative Strength Index): 14-period default
- **MACD** (Moving Average Convergence Divergence): 12/26/9 parameters
- **Moving Averages**: 20-day (short), 50-day (long)
- **Volatility**: Standard deviation of returns
- **Trend Analysis**: Bullish/Bearish/Neutral classification

### **2. Marketing Analysis API**

#### **Endpoint**: Internal MarketingAnalyzer

**Description**: Analyzes marketing campaign performance with comprehensive metrics

**Parameters**:
- `data` (DataFrame): Marketing campaign data with columns:
  - `Budget`: Campaign budget amount
  - `Clicks`: Number of clicks
  - `Conversions`: Number of conversions
  - `Revenue`: Revenue generated

**Returns**:
```python
{
    'total_metrics': {
        'total_budget': 50000.0,
        'total_revenue': 75000.0,
        'overall_roi': 50.0,
        'overall_conversion_rate': 3.5
    },
    'campaign_metrics': {
        'campaign_name': {
            'budget': 10000.0,
            'revenue': 15000.0,
            'roi': 50.0,
            'conversion_rate': 4.2,
            'cost_per_conversion': 238.10
        }
    },
    'rankings': {
        'best_roi': {'campaign': 'Campaign A', 'value': 75.0},
        'best_conversion': {'campaign': 'Campaign B', 'value': 5.2}
    }
}
```

**Usage Example**:
```python
import pandas as pd
from analysis.marketing import MarketingAnalyzer

data = pd.DataFrame({
    'Campaign': ['Facebook Ads', 'Google Ads'],
    'Budget': [5000, 8000],
    'Clicks': [1200, 2500],
    'Conversions': [45, 85],
    'Revenue': [6750, 12750]
})

analyzer = MarketingAnalyzer()
results = analyzer.get_comprehensive_analysis(data)
print(f"Overall ROI: {results['total_metrics']['overall_roi']:.2f}%")
```

#### **Marketing Metrics Available**:
- **ROI** (Return on Investment): (Revenue - Budget) / Budget * 100
- **Conversion Rate**: Conversions / Clicks * 100
- **Cost Per Conversion**: Budget / Conversions
- **Click-Through Rate**: Clicks / Impressions (if available)
- **Revenue Per Click**: Revenue / Clicks

### **3. Report Generator API**

#### **Endpoint**: Internal ReportGenerator

**Description**: Generates comprehensive PDF reports with charts and analysis

**Parameters**:
- `trading_data` (dict): Trading analysis results
- `marketing_data` (dict): Marketing analysis results
- `output_path` (string): Path to save PDF report

**Returns**:
- PDF file with comprehensive analysis report

**Usage Example**:
```python
from utils.report_generator import ReportGenerator

generator = ReportGenerator()
generator.create_comprehensive_report(
    trading_data=trading_results,
    marketing_data=marketing_results,
    output_path="analysis_report.pdf"
)
```

## 🛠️ **Configuration APIs**

### **Trading Configuration**
```python
from utils.config import get_trading_config

config = get_trading_config()
# Returns: dict with trading parameters
```

### **Marketing Configuration**
```python
from utils.config import get_marketing_config

config = get_marketing_config()
# Returns: dict with marketing parameters
```

### **Application Configuration**
```python
from utils.config import get_app_config

config = get_app_config()
# Returns: dict with app settings
```

## 📈 **Data Sources**

### **Financial Data**
- **Provider**: Yahoo Finance API
- **Endpoint**: `https://query1.finance.yahoo.com/v8/finance/chart/`
- **Data Types**: OHLCV (Open, High, Low, Close, Volume)
- **Update Frequency**: Real-time during market hours

### **Marketing Data**
- **Source**: User-uploaded CSV files
- **Required Columns**: Budget, Clicks, Conversions, Revenue
- **File Format**: CSV (UTF-8 encoded)
- **Max File Size**: 200MB

## 🔧 **Technical Specifications**

### **Dependencies**
```python
streamlit>=1.28.0      # Web framework
pandas>=2.0.0          # Data analysis
numpy>=1.24.0          # Numerical computing
yfinance>=0.2.18       # Financial data
plotly>=5.15.0         # Interactive charts
scipy>=1.10.0          # Scientific computing
reportlab>=4.0.0       # PDF generation
python-dateutil>=2.8.0 # Date utilities
requests>=2.31.0       # HTTP requests
```

### **Performance Metrics**
- **Response Time**: < 2 seconds for stock analysis
- **Data Processing**: Real-time for up to 1000 campaigns
- **Chart Rendering**: < 1 second for interactive charts
- **Report Generation**: < 5 seconds for comprehensive PDF

### **Error Handling**
- **Stock Data**: Graceful fallback for invalid tickers
- **File Upload**: Validation for CSV format and required columns
- **API Limits**: Built-in rate limiting for external APIs
- **Data Validation**: Comprehensive input sanitization

## 🔒 **Security & Limitations**

### **Data Privacy**
- **No Data Storage**: All data processed in memory only
- **Local Processing**: No external data transmission except financial APIs
- **Session Isolation**: User data isolated per session

### **Rate Limits**
- **Yahoo Finance**: 2,000 requests/hour
- **File Upload**: 200MB maximum file size
- **Concurrent Users**: No hard limit (depends on system resources)

### **Disclaimer**
- **Educational Purpose Only**: Not for live trading
- **No Financial Advice**: Analysis for informational purposes only
- **Risk Warning**: Users assume all investment risks

## 🚀 **Deployment Options**

### **Local Development**
```bash
streamlit run app.py --server.port 8501
```

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

### **Cloud Deployment**
- **Streamlit Cloud**: Direct deployment from GitHub
- **Heroku**: Using Streamlit buildpack
- **AWS**: EC2 instance with Docker
- **Azure**: App Service with container support

## 📞 **Support & Contact**

### **Documentation Updates**
- **Version**: 1.0.0
- **Last Updated**: January 27, 2026
- **Maintainer**: InsightX Exchange Team

### **Feature Requests**
- **GitHub Issues**: For bug reports and feature requests
- **Documentation**: Updates and improvements
- **Community**: User forums and discussions

---

**© 2026 InsightX Exchange - Educational Analytics Platform**
