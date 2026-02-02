"""
Home Page - Project Overview
Modern redesigned landing page for InsightX Exchange
"""

import streamlit as st
from datetime import datetime
from utils.styles import get_global_styles

def main():
    """Home page main function"""
    
    # Page configuration
    st.set_page_config(
        page_title="Home - InsightX Exchange",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply enhanced global styles
    st.markdown(get_global_styles(), unsafe_allow_html=True)
    
    # Additional custom styles for hero section
    st.markdown("""
    <style>
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 80px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 2px, transparent 2px);
        background-size: 30px 30px;
        opacity: 0.4;
        animation: float 25s linear infinite;
    }
    
    .hero-title {
        font-size: 3.5em;
        font-weight: 800;
        color: white;
        margin-bottom: 20px;
        position: relative;
        z-index: 2;
        text-shadow: 0 4px 15px rgba(0,0,0,0.2);
        animation: fadeInUp 1s ease-out;
    }
    
    .hero-subtitle {
        font-size: 1.4em;
        color: rgba(255,255,255,0.95);
        margin-bottom: 30px;
        position: relative;
        z-index: 2;
        animation: fadeInUp 1.2s ease-out;
    }
    
    .hero-badges {
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        position: relative;
        z-index: 2;
        animation: fadeInUp 1.4s ease-out;
    }
    
    .hero-badge {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 8px 20px;
        border-radius: 25px;
        font-size: 0.9em;
        font-weight: 600;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s ease;
    }
    
    .hero-badge:hover {
        background: rgba(255,255,255,0.3);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 25px;
        margin: 40px 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .stat-number {
        font-size: 2.5em;
        font-weight: 800;
        color: #667eea;
        margin-bottom: 10px;
        display: block;
    }
    
    .stat-label {
        color: #666;
        font-size: 1.1em;
        font-weight: 600;
    }
    
    .platform-showcase {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 60px 30px;
        border-radius: 20px;
        margin: 40px 0;
        position: relative;
    }
    
    .showcase-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
        margin-top: 40px;
    }
    
    .showcase-card {
        background: white;
        padding: 40px 30px;
        border-radius: 20px;
        text-align: center;
        transition: all 0.4s ease;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        position: relative;
        overflow: hidden;
    }
    
    .showcase-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.05), transparent);
        transform: rotate(45deg);
        transition: all 0.6s ease;
    }
    
    .showcase-card:hover::before {
        animation: shimmer 0.6s ease-out;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .showcase-card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.2);
    }
    
    .showcase-icon {
        font-size: 4em;
        margin-bottom: 20px;
        display: block;
        animation: bounce 2s infinite;
    }
    
    .showcase-title {
        font-size: 1.5em;
        font-weight: 700;
        color: #333;
        margin-bottom: 15px;
    }
    
    .showcase-description {
        color: #666;
        line-height: 1.6;
        font-size: 1em;
    }
    
    .cta-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 60px 30px;
        border-radius: 20px;
        text-align: center;
        margin: 40px 0;
        position: relative;
        overflow: hidden;
    }
    
    .cta-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .cta-title {
        font-size: 2.5em;
        font-weight: 800;
        color: white;
        margin-bottom: 20px;
        position: relative;
        z-index: 2;
    }
    
    .cta-description {
        font-size: 1.2em;
        color: rgba(255,255,255,0.9);
        margin-bottom: 30px;
        position: relative;
        z-index: 2;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .tech-stack {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        margin: 30px 0;
    }
    
    .tech-item {
        background: rgba(255,255,255,0.1);
        color: white;
        padding: 12px 25px;
        border-radius: 30px;
        font-weight: 600;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .tech-item:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5em;
        }
        
        .hero-subtitle {
            font-size: 1.2em;
        }
        
        .showcase-grid {
            grid-template-columns: 1fr;
        }
        
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🚀 InsightX Exchange</h1>
        <p class="hero-subtitle">AI-Powered Financial & Marketing Analytics Platform</p>
        <div class="hero-badges">
            <span class="hero-badge">🤖 AI-Powered</span>
            <span class="hero-badge">📊 Real-time Analysis</span>
            <span class="hero-badge">🎓 Educational Platform</span>
            <span class="hero-badge">📈 Market Insights</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Section
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <span class="stat-number">4+</span>
            <span class="stat-label">Analysis Tools</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <span class="stat-number">AI</span>
            <span class="stat-label">Intelligence</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <span class="stat-number">24/7</span>
            <span class="stat-label">Availability</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <span class="stat-number">2026</span>
            <span class="stat-label">Graduation Project</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Platform Showcase
    st.markdown("""
    <div class="platform-showcase">
        <h2 style="text-align: center; font-size: 2.5em; color: #333; margin-bottom: 20px;">
            🎯 Platform Capabilities
        </h2>
        <p style="text-align: center; color: #666; font-size: 1.2em; max-width: 800px; margin: 0 auto;">
            Comprehensive analytics platform combining AI intelligence with financial and marketing expertise
        </p>
        <div class="showcase-grid">
    """, unsafe_allow_html=True)
    
    # Feature Cards
    features = [
        {
            "icon": "📈",
            "title": "Trading Analysis",
            "description": "Advanced stock analysis with real-time data, technical indicators, and predictive analytics powered by AI."
        },
        {
            "icon": "📊", 
            "title": "Technical Indicators",
            "description": "Comprehensive technical analysis tools including RSI, MACD, Bollinger Bands, and custom indicators."
        },
        {
            "icon": "📢",
            "title": "Marketing Analytics", 
            "description": "Campaign performance analysis with ROI tracking, conversion optimization, and AI-driven insights."
        },
        {
            "icon": "🤖",
            "title": "AI Assistant",
            "description": "Intelligent chatbot specialized in trading and marketing topics with real-time market insights."
        },
        {
            "icon": "🎯",
            "title": "Risk Management",
            "description": "Advanced risk assessment tools with portfolio analysis and scenario planning capabilities."
        }
    ]
    
    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for j, feature in enumerate(features[i:i+3]):
            with cols[j]:
                st.markdown(f"""
                <div class="showcase-card">
                    <span class="showcase-icon">{feature['icon']}</span>
                    <div class="showcase-title">{feature['title']}</div>
                    <div class="showcase-description">{feature['description']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class="cta-section">
        <h2 class="cta-title">🚀 Ready to Get Started?</h2>
        <p class="cta-description">
            Navigate through our powerful analysis tools using the sidebar menu. 
            Each tool is designed to provide comprehensive insights for your financial and marketing decisions.
        </p>
        <div class="tech-stack">
            <span class="tech-item">🐍 Python</span>
            <span class="tech-item">🤖 AI/ML</span>
            <span class="tech-item">📊 Streamlit</span>
            <span class="tech-item">💹 Real-time Data</span>
            <span class="tech-item">🔍 Advanced Analytics</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Start Guide
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 40px; border-radius: 20px; margin: 30px 0;">
        <h3 style="text-align: center; color: #667eea; font-size: 2em; margin-bottom: 30px;">
            🧭 Quick Start Guide
        </h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
            <div style="background: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                <div style="font-size: 2em; margin-bottom: 15px;">1️⃣</div>
                <h4 style="color: #667eea; margin-bottom: 10px;">Choose Analysis Type</h4>
                <p style="color: #666;">Select from Trading or Marketing</p>
            </div>
            <div style="background: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                <div style="font-size: 2em; margin-bottom: 15px;">2️⃣</div>
                <h4 style="color: #667eea; margin-bottom: 10px;">Input Data</h4>
                <p style="color: #666;">Upload files or enter symbols for analysis</p>
            </div>
            <div style="background: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                <div style="font-size: 2em; margin-bottom: 15px;">3️⃣</div>
                <h4 style="color: #667eea; margin-bottom: 10px;">Get Insights</h4>
                <p style="color: #666;">View results and AI-powered recommendations</p>
            </div>
            <div style="background: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                <div style="font-size: 2em; margin-bottom: 15px;">4️⃣</div>
                <h4 style="color: #667eea; margin-bottom: 10px;">Generate Reports</h4>
                <p style="color: #666;">Create professional PDF reports</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); padding: 30px; border-radius: 15px; border-left: 5px solid #ffc107; margin: 30px 0;">
        <h3 style="color: #856404; margin-bottom: 20px;">⚠️ Important Disclaimer</h3>
        <div style="color: #856404; line-height: 1.8;">
            <p><strong>🎓 Educational Purpose:</strong> This is a graduation project demonstration for academic purposes.</p>
            <p><strong>⚠️ No Financial Advice:</strong> This platform provides analysis and decision support only, not financial advice.</p>
            <p><strong>📊 Risk Warning:</strong> All trading involves risk. Never invest more than you can afford to lose.</p>
            <p><strong>👨‍💼 Consult Professionals:</strong> Always consult with qualified financial advisors before making investment decisions.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin-top: 20px;'>
        <p style='color: #667eea; font-weight: bold; font-size: 1.2em; margin: 0;'>🎓 Graduation Project | AI Engineering Department</p>
        <p style='color: #666; margin: 10px 0; font-size: 1.1em;'>© 2026 InsightX Exchange - Educational Purpose Only</p>
        <p style='color: #666; margin: 5px 0;'>Contact: insightxexchange@gmail.com</p>
        <p style='color: #999; font-size: 0.9em; margin: 5px 0;'>Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
        <div style="margin-top: 15px;">
            <span style="background: #667eea; color: white; padding: 5px 15px; border-radius: 15px; margin: 0 5px; font-size: 0.8em;">🤖 AI-Powered</span>
            <span style="background: #764ba2; color: white; padding: 5px 15px; border-radius: 15px; margin: 0 5px; font-size: 0.8em;">📊 Analytics</span>
            <span style="background: #f093fb; color: white; padding: 5px 15px; border-radius: 15px; margin: 0 5px; font-size: 0.8em;">🎓 Educational</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
