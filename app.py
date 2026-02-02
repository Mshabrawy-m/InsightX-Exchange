"""
Marketing & Trading Analytics Platform
Main Streamlit Application - Entry point for the InsightX Exchange platform

Design Choices:
- Multi-page architecture using Streamlit's built-in navigation for scalability
- Wide layout to accommodate complex visualizations and data tables
- Expanded sidebar by default for better navigation experience
- Centralized configuration through page settings for consistency
"""

import streamlit as st
from datetime import datetime
from utils.styles import get_global_styles, get_page_header, get_info_box

# Configure page settings
# Design Choice: Centralized configuration ensures consistent branding and UX across all pages
st.set_page_config(
    page_title="InsightX Exchange",
    page_icon="📊",
    layout="wide",  # Wide layout chosen to accommodate complex charts and data tables
    initial_sidebar_state="expanded"  # Expanded sidebar improves navigation UX
)

# Apply global styles
st.markdown(get_global_styles(), unsafe_allow_html=True)


def main():
    """Main application entry point - Navigation hub for all features"""
    
    # Enhanced sidebar navigation with consistent styling
    with st.sidebar:
        st.markdown(get_page_header("InsightX Exchange", "Analytics Platform", "📊"), unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(get_info_box(
            "Navigation Guide", 
            "Use the pages selector above to navigate through different analysis tools and features.",
            "🧭"
        ), unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(get_info_box(
            "Available Pages", 
            "Choose from Trading Analysis, Marketing Analysis, and AI Chatbot.",
            "📚"
        ), unsafe_allow_html=True)
        
        st.markdown("""
        <div style='padding: 10px; background-color: #ffffff; border-radius: 8px; border: 1px solid #e9ecef; margin-bottom: 8px;'>
            <p style='color: #667eea; margin: 0; font-weight: bold;'>🏠 Home</p>
            <p style='color: #666; margin: 0; font-size: 12px;'>Platform overview & getting started</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='padding: 10px; background-color: #ffffff; border-radius: 8px; border: 1px solid #e9ecef; margin-bottom: 8px;'>
            <p style='color: #764ba2; margin: 0; font-weight: bold;'>📈 Trading Analysis</p>
            <p style='color: #666; margin: 0; font-size: 12px;'>Stock analysis & technical indicators</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='padding: 10px; background-color: #ffffff; border-radius: 8px; border: 1px solid #e9ecef; margin-bottom: 8px;'>
            <p style='color: #f093fb; margin: 0; font-weight: bold;'>📢 Marketing Analysis</p>
            <p style='color: #666; margin: 0; font-size: 12px;'>Campaign performance & ROI analysis</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='padding: 10px; background-color: #ffffff; border-radius: 8px; border: 1px solid #e9ecef; margin-bottom: 8px;'>
            <p style='color: #17a2b8; margin: 0; font-weight: bold;'>🤖 AI Chatbot</p>
            <p style='color: #666; margin: 0; font-size: 12px;'>Marketing & trading Q&A assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        
        st.markdown("---")
        st.markdown("""
        <div style='padding: 15px; background-color: #e3f2fd; border-radius: 10px; border-left: 4px solid #2196f3;'>
            <h4 style='color: #1976d2; margin-bottom: 10px;'>💡 Quick Tip</h4>
            <p style='color: #666; margin: 0; font-size: 12px;'>Start with the Home page to explore all features!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced main content area with consistent styling
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0;'>Welcome to InsightX Exchange</h1>
        <p style='color: white; margin: 10px 0 0 0; font-size: 18px;'>Financial & Marketing Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation instruction with enhanced styling
    st.markdown("""
    <div style='padding: 20px; background-color: #f8f9fa; border-radius: 10px; border-left: 4px solid #667eea; margin-bottom: 20px;'>
        <h3 style='color: #667eea; margin-bottom: 15px;'>🧭 Getting Started</h3>
        <p style='color: #666; margin: 0; font-size: 16px;'>👈 Select a page from the sidebar to begin your analysis journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature overview cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='padding: 20px; background-color: #ffffff; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 15px;'>
            <h4 style='color: #667eea; margin-bottom: 15px;'>📈 Trading Features</h4>
            <ul style='color: #666; line-height: 1.6;'>
                <li>✅ Real-time stock data analysis</li>
                <li>✅ Technical indicators (RSI, MACD, Moving Averages)</li>
                <li>✅ Volatility calculations</li>
                <li>✅ Trend analysis & signals</li>
                <li>✅ AI-powered trading insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='padding: 20px; background-color: #ffffff; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 15px;'>
            <h4 style='color: #764ba2; margin-bottom: 15px;'>🤖 AI Capabilities</h4>
            <ul style='color: #666; line-height: 1.6;'>
                <li>✅ Intelligent chatbot assistant</li>
                <li>✅ Bilingual support (English/Arabic)</li>
                <li>✅ Intent detection & context awareness</li>
                <li>✅ Educational responses</li>
                <li>✅ Performance optimization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='padding: 20px; background-color: #ffffff; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 15px;'>
            <h4 style='color: #f093fb; margin-bottom: 15px;'>📢 Marketing Features</h4>
            <ul style='color: #666; line-height: 1.6;'>
                <li>✅ Campaign performance metrics</li>
                <li>✅ ROI and conversion analysis</li>
                <li>✅ KPI calculations (CTR, CPA, etc.)</li>
                <li>✅ Interactive visualizations</li>
                <li>✅ Performance rankings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    
    # Platform info with enhanced styling
    st.markdown("---")
    st.markdown("""
    <div style='padding: 20px; background-color: #e8f5e8; border-radius: 10px; border-left: 4px solid #4caf50; margin-bottom: 20px;'>
        <h3 style='color: #2e7d32; margin-bottom: 15px;'>🎯 Platform Overview</h3>
        <p style='color: #666; margin: 0; font-size: 16px;'><strong>LLM-Based Marketing & Trading Assistant</strong></p>
        <p style='color: #666; margin: 10px 0 0 0; line-height: 1.6;'>
            This intelligent assistant combines advanced machine learning with financial and marketing analytics 
            to provide comprehensive insights for decision-making support. Whether you're analyzing stock performance, 
            evaluating marketing campaigns, or need AI-powered insights, InsightX Exchange has you covered.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick start guide
    st.markdown("""
    <div style='padding: 20px; background-color: #fff3cd; border-radius: 10px; border-left: 4px solid #ffc107; margin-bottom: 20px;'>
        <h3 style='color: #856404; margin-bottom: 15px;'>🚀 Quick Start Guide</h3>
        <ol style='color: #856404; line-height: 1.8; font-weight: bold;'>
            <li>Navigate to any page using the sidebar</li>
            <li>Upload data or enter symbols for analysis</li>
            <li>View interactive results and insights</li>
            <li>Get AI-powered recommendations</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer with enhanced styling
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-top: 20px;'>
        <p style='color: #667eea; font-weight: bold; margin: 0;'>🎓 Graduation Project | AI Engineering Department</p>
        <p style='color: #666; margin: 5px 0;'>© 2026 InsightX Exchange - Educational Purpose Only</p>
        <p style='color: #666; margin: 5px 0;'>Contact: insightxexchange@gmail.com</p>
        <p style='color: #999; font-size: 12px; margin: 5px 0;'>Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
