"""
Trading Analysis Page
Provides comprehensive stock analysis with technical indicators
"""

import streamlit as st
import pandas as pd
from analysis.trading import TradingAnalyzer
from llm.client import llm_client
from datetime import datetime

def main():
    st.set_page_config(page_title="Trading Analysis", page_icon="📈", layout="wide")
    
    # Enhanced header
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0;'>📈 Trading Analysis</h1>
        <p style='color: white; margin: 10px 0 0 0; font-size: 16px;'>Comprehensive Stock Analysis with Technical Indicators</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize analyzers
    trading_analyzer = TradingAnalyzer()
    
    # Enhanced sidebar inputs
    with st.sidebar:
        st.markdown("""
        <div style='padding: 15px; background-color: #f8f9fa; border-radius: 10px; border-left: 4px solid #667eea;'>
            <h3 style='color: #667eea; margin-bottom: 15px;'>🔍 Analysis Parameters</h3>
        </div>
        """, unsafe_allow_html=True)
        
        ticker = st.text_input(
            "Stock Ticker", 
            value="AAPL",
            help="Enter stock ticker symbol (e.g., AAPL, MSFT, GOOGL, GOOGLE, META, FB, AMZN)"
        )
        
        period = st.selectbox(
            "Time Period",
            options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
            index=3,
            help="Select time period for analysis"
        )
        
        # Quick select buttons
        st.markdown("**Quick Select:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🍎 AAPL", key="aapl"):
                st.session_state.quick_ticker = "AAPL"
        with col2:
            if st.button("💻 MSFT", key="msft"):
                st.session_state.quick_ticker = "MSFT"
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🔍 GOOGL", key="googl"):
                st.session_state.quick_ticker = "GOOGL"
        with col4:
            if st.button("📱 TSLA", key="tsla"):
                st.session_state.quick_ticker = "TSLA"
        
        # Use quick ticker if set
        if 'quick_ticker' in st.session_state:
            ticker = st.session_state.quick_ticker
            del st.session_state.quick_ticker
        
        st.markdown("---")
        analyze_button = st.button("🔍 Analyze Stock", type="primary", use_container_width=True)
        
        # Market status indicator
        st.markdown("""
        <div style='padding: 10px; background-color: #d4edda; border-radius: 8px; text-align: center; margin-top: 15px;'>
            <p style='color: #155724; margin: 0; font-size: 12px;'>📊 Market Status: Real-time Data</p>
        </div>
        """, unsafe_allow_html=True)
    
    if analyze_button and ticker:
        try:
            with st.spinner("🔄 Fetching and analyzing data..."):
                # Show ticker being analyzed
                st.markdown(f"""
                <div style='padding: 15px; background-color: #e3f2fd; border-radius: 10px; border-left: 4px solid #2196f3; margin-bottom: 20px;'>
                    <h4 style='color: #1976d2; margin-bottom: 10px;'>🔍 Analyzing ticker: {ticker.upper()}</h4>
                    <p style='color: #666; margin: 0;'>Fetching data for {period} period...</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Perform analysis
                results = trading_analyzer.analyze_stock(ticker, period)
                
                # Show success message with normalized ticker
                normalized_ticker = trading_analyzer._normalize_ticker(ticker)
                st.markdown(f"""
                <div style='padding: 15px; background-color: #e8f5e8; border-radius: 10px; border-left: 4px solid #4caf50; margin-bottom: 20px;'>
                    <h4 style='color: #2e7d32; margin-bottom: 10px;'>✅ Successfully analyzed {normalized_ticker}</h4>
                    <p style='color: #666; margin: 0;'>Analysis completed for {period} period</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced metrics display
                st.markdown("## 📊 Key Metrics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div style='padding: 15px; background-color: #ffffff; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                        <h4 style='color: #667eea; margin-bottom: 10px;'>Current Price</h4>
                        <p style='font-size: 24px; font-weight: bold; color: #333; margin: 0;'>${results['latest_values']['price']:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style='padding: 15px; background-color: #ffffff; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                        <h4 style='color: #764ba2; margin-bottom: 10px;'>RSI</h4>
                        <p style='font-size: 24px; font-weight: bold; color: #333; margin: 0;'>{results['latest_values']['rsi']:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div style='padding: 15px; background-color: #ffffff; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                        <h4 style='color: #f093fb; margin-bottom: 10px;'>Volatility</h4>
                        <p style='font-size: 24px; font-weight: bold; color: #333; margin: 0;'>{results['volatility']:.2%}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    price_change = results['statistics']['price_change_pct']
                    color = '#28a745' if price_change > 0 else '#dc3545' if price_change < 0 else '#ffc107'
                    st.markdown(f"""
                    <div style='padding: 15px; background-color: #ffffff; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                        <h4 style='color: #667eea; margin-bottom: 10px;'>Price Change</h4>
                        <p style='font-size: 24px; font-weight: bold; color: {color}; margin: 0;'>{price_change:+.2f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Enhanced trend information
                st.markdown("---")
                st.markdown("## 📈 Trend Analysis")
                
                trend_col1, trend_col2 = st.columns(2)
                
                with trend_col1:
                    st.markdown(f"""
                    <div style='padding: 20px; background-color: #f8f9fa; border-radius: 10px; border-left: 4px solid #17a2b8;'>
                        <h4 style='color: #17a2b8; margin-bottom: 15px;'>📊 Trend Information</h4>
                        <p style='color: #666; margin-bottom: 10px;'><strong>Trend:</strong> {results['trend_info']['trend']}</p>
                        <p style='color: #666; margin: 0;'><strong>Signal:</strong> {results['trend_info']['signal']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with trend_col2:
                    # Risk warning based on volatility
                    if results['volatility'] > 0.3:
                        st.markdown("""
                        <div style='padding: 20px; background-color: #f8d7da; border-radius: 10px; border-left: 4px solid #dc3545;'>
                            <h4 style='color: #dc3545; margin-bottom: 15px;'>⚠️ Risk Assessment</h4>
                            <p style='color: #721c24; margin: 0;'>High Volatility - Increased Risk</p>
                        </div>
                        """, unsafe_allow_html=True)
                    elif results['volatility'] > 0.2:
                        st.markdown("""
                        <div style='padding: 20px; background-color: #fff3cd; border-radius: 10px; border-left: 4px solid #ffc107;'>
                            <h4 style='color: #856404; margin-bottom: 15px;'>⚡ Risk Assessment</h4>
                            <p style='color: #856404; margin: 0;'>Moderate Volatility</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style='padding: 20px; background-color: #d4edda; border-radius: 10px; border-left: 4px solid #28a745;'>
                            <h4 style='color: #155724; margin-bottom: 15px;'>✅ Risk Assessment</h4>
                            <p style='color: #155724; margin: 0;'>Low Volatility</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Charts with enhanced titles
                st.markdown("---")
                st.plotly_chart(results['price_chart'], use_container_width=True)
                
                st.markdown("## 📊 Technical Indicators")
                st.plotly_chart(results['technical_chart'], use_container_width=True)
                
                # Display additional analysis results
                st.markdown("---")
                st.markdown("## 📊 Analysis Summary")
                
                # AI Insights Section
                st.markdown("## 🤖 AI-Powered Insights")
                
                with st.spinner("🔄 Generating AI insights..."):
                    try:
                        # Prepare data for AI analysis with safe defaults
                        ai_data = {
                            'current_price': results['statistics'].get('current_price', 'N/A'),
                            'rsi': results['indicators'].get('rsi', 'N/A'),
                            'macd': results['indicators'].get('macd', 'N/A'),
                            'moving_averages': {
                                'short': results['indicators'].get('sma_short', 'N/A'),
                                'long': results['indicators'].get('sma_long', 'N/A')
                            },
                            'volatility': results.get('volatility', 'N/A')
                        }
                        
                        # Generate AI insights
                        ai_insights = llm_client.analyze_trading_data(ticker, ai_data)
                        
                        st.markdown("""
                        <div style='padding: 20px; background-color: #e3f2fd; border-radius: 10px; border-left: 4px solid #2196f3; margin-bottom: 20px;'>
                            <h4 style='color: #1976d2; margin-bottom: 15px;'>🧠 AI Analysis</h4>
                            <div style='color: #666; line-height: 1.6;'>{}</div>
                        </div>
                        """.format(ai_insights.strip()), unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.markdown(f"""
                        <div style='padding: 20px; background-color: #f8d7da; border-radius: 10px; border-left: 4px solid #dc3545; margin-bottom: 20px;'>
                            <h4 style='color: #dc3545; margin-bottom: 15px;'>❌ AI Insights Unavailable</h4>
                            <p style='color: #721c24; margin: 0;'>Unable to generate AI insights: {str(e)}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Enhanced Detailed Statistics
                with st.expander("📋 Detailed Statistics", expanded=False):
                    stats_df = pd.DataFrame({
                        'Metric': ['Average Volume', 'Max Price', 'Min Price', 'Total Return'],
                        'Value': [
                            f"{results['statistics']['avg_volume']:,.0f}",
                            f"${results['statistics']['max_price']:.2f}",
                            f"${results['statistics']['min_price']:.2f}",
                            f"{results['statistics']['price_change_pct']:.2f}%"
                        ]
                    })
                    st.dataframe(stats_df, use_container_width=True)
                
                # Enhanced Disclaimer
                st.markdown("---")
                st.markdown("""
                <div style='padding: 20px; background-color: #f8d7da; border-radius: 10px; border-left: 4px solid #dc3545;'>
                    <h4 style='color: #dc3545; margin-bottom: 15px;'>⚠️ IMPORTANT DISCLAIMER</h4>
                    <p style='color: #721c24; margin-bottom: 10px;'><strong>Educational Purpose Only:</strong> This analysis is for educational purposes only and does not constitute financial advice.</p>
                    <p style='color: #721c24; margin-bottom: 10px;'><strong>Risk Warning:</strong> Trading involves substantial risk of loss. Always consult with qualified financial professionals before making investment decisions.</p>
                    <p style='color: #721c24; margin: 0;'><strong>Market Data:</strong> All data is provided "as is" without warranty of any kind.</p>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.markdown(f"""
            <div style='padding: 20px; background-color: #f8d7da; border-radius: 10px; border-left: 4px solid #dc3545;'>
                <h4 style='color: #dc3545; margin-bottom: 15px;'>❌ Analysis Error</h4>
                <p style='color: #721c24; margin-bottom: 10px;'><strong>Error analyzing {ticker}:</strong> {str(e)}</p>
                <p style='color: #721c24; margin: 0;'>Please check the ticker symbol and try again.</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif not ticker:
        st.markdown("""
        <div style='padding: 40px; background-color: #f8f9fa; border-radius: 10px; text-align: center; border: 2px dashed #dee2e6;'>
            <h3 style='color: #6c757d; margin-bottom: 15px;'>👈 Get Started</h3>
            <p style='color: #6c757d; margin: 0;'>Enter a stock ticker symbol in the sidebar to begin analysis.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
