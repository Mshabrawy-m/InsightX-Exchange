# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from llm.client import llm_client

def main():
    st.set_page_config(page_title="Marketing Analysis", page_icon="📢", layout="wide")
    
    # Header with gradient styling
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0;'>📢 Marketing Analysis</h1>
        <p style='color: white; margin: 10px 0 0 0; font-size: 16px;'>Comprehensive Campaign Performance Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data Upload Section
    st.markdown("## 📁 Data Upload")
    
    st.markdown("""
    <div style='padding: 15px; background-color: #f8f9fa; border-radius: 10px; border-left: 4px solid #667eea; margin-bottom: 20px;'>
        <h3 style='color: #667eea; margin-bottom: 15px;'>📊 Upload Your Marketing Data</h3>
        <p style='color: #666; margin: 0;'>Upload a CSV file with campaign data or generate sample data to explore the analysis features.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Marketing Data (CSV)",
        type=['csv'],
        help="Upload a CSV file with columns: Budget, Clicks, Conversions, Revenue"
    )
    
    # Sample data generation
    if uploaded_file is None:
        st.markdown("""
        <div style='padding: 20px; background-color: #e3f2fd; border-radius: 10px; border-left: 4px solid #2196f3; margin-bottom: 20px;'>
            <h4 style='color: #1976d2; margin-bottom: 15px;'>👆 Quick Start Options</h4>
            <p style='color: #666; margin: 0;'>Upload your own CSV file or generate sample data to explore the analysis features.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📊 Generate Sample Data", type="primary", use_container_width=True):
                sample_data = pd.DataFrame({
                    'Campaign': ['Facebook Ads', 'Google Ads', 'LinkedIn Ads', 'Twitter Ads', 'Email Campaign'],
                    'Budget': [5000, 8000, 3000, 2000, 1500],
                    'Clicks': [1200, 2500, 800, 600, 400],
                    'Conversions': [45, 85, 25, 18, 12],
                    'Revenue': [6750, 12750, 3750, 2160, 1440]
                })
                sample_data.set_index('Campaign', inplace=True)
                st.session_state.sample_data = sample_data
                st.success("Sample data generated! Click 'Analyze Data' to proceed.")
                
                st.markdown("""
                <div style='padding: 15px; background-color: #e8f5e8; border-radius: 10px; border-left: 4px solid #4caf50; margin-bottom: 15px;'>
                    <h4 style='color: #2e7d32; margin-bottom: 10px;'>📊 Sample Marketing Data</h4>
                    <p style='color: #666; margin: 0;'>Here's your sample campaign data ready for analysis:</p>
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(sample_data, use_container_width=True)
    
    # Data processing
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if 'Campaign' in df.columns:
                df.set_index('Campaign', inplace=True)
            else:
                df.index = [f'Campaign {i+1}' for i in range(len(df))]
            
            st.session_state.uploaded_data = df
            
            st.markdown("""
            <div style='padding: 20px; background-color: #e8f5e8; border-radius: 10px; border-left: 4px solid #4caf50; margin-bottom: 15px;'>
                <h4 style='color: #2e7d32; margin-bottom: 10px;'>Data Upload Successful!</h4>
                <p style='color: #666; margin: 0;'>Your marketing data has been uploaded and is ready for analysis.</p>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
            
        except Exception as e:
            st.markdown(f"""
            <div style='padding: 20px; background-color: #f8d7da; border-radius: 10px; border-left: 4px solid #dc3545; margin-bottom: 15px;'>
                <h4 style='color: #dc3545; margin-bottom: 10px;'>Error Reading File</h4>
                <p style='color: #721c24; margin: 0;'>{str(e)}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Analysis section
    if 'uploaded_data' in st.session_state or 'sample_data' in st.session_state:
        df = st.session_state.get('uploaded_data', st.session_state.get('sample_data'))
        
        st.markdown("---")
        st.markdown("## 🔍 Analysis Results")
        
        st.markdown("""
        <div style='padding: 15px; background-color: #f8f9fa; border-radius: 10px; border-left: 4px solid #764ba2; margin-bottom: 20px;'>
            <h3 style='color: #764ba2; margin-bottom: 15px;'>📊 Marketing Analysis</h3>
            <p style='color: #666; margin: 0;'>Click the button below to perform analysis of your marketing data.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_button = st.button("📊 Analyze Data", type="primary", use_container_width=True)
        
        if analyze_button:
            with st.spinner("Analyzing marketing data..."):
                try:
                    total_budget = df['Budget'].sum()
                    total_revenue = df['Revenue'].sum()
                    overall_roi = ((total_revenue - total_budget) / total_budget * 100) if total_budget > 0 else 0
                    total_clicks = df['Clicks'].sum()
                    total_conversions = df['Conversions'].sum()
                    overall_conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
                    
                    st.session_state.analysis_results = {
                        'total_budget': total_budget,
                        'total_revenue': total_revenue,
                        'overall_roi': overall_roi,
                        'overall_conversion_rate': overall_conversion_rate
                    }
                    
                    st.markdown("""
                    <div style='padding: 20px; background-color: #e8f5e8; border-radius: 10px; border-left: 4px solid #4caf50; margin-bottom: 15px;'>
                        <h4 style='color: #2e7d32; margin-bottom: 10px;'>Analysis Completed Successfully!</h4>
                        <p style='color: #666; margin: 0;'>Your marketing data has been analyzed. View the results below.</p>
                    </div>
                    """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.markdown(f"""
                    <div style='padding: 20px; background-color: #f8d7da; border-radius: 10px; border-left: 4px solid #dc3545; margin-bottom: 15px;'>
                        <h4 style='color: #dc3545; margin-bottom: 10px;'>Analysis Error</h4>
                        <p style='color: #721c24; margin: 0;'>{str(e)}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Display results
    if 'analysis_results' in st.session_state:
        results = st.session_state.analysis_results
        
        st.markdown("---")
        st.markdown("## 📊 KPI Summary")
        
        st.markdown("""
        <div style='padding: 15px; background-color: #f8f9fa; border-radius: 10px; border-left: 4px solid #f093fb; margin-bottom: 20px;'>
            <h3 style='color: #f093fb; margin-bottom: 15px;'>📈 Key Performance Indicators</h3>
            <p style='color: #666; margin: 0;'>Overview of your marketing campaign performance metrics.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style='padding: 20px; background-color: #ffffff; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h4 style='color: #667eea; margin-bottom: 10px;'>Total Budget</h4>
                <p style='font-size: 24px; font-weight: bold; color: #333; margin: 0;'>${results['total_budget']:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='padding: 20px; background-color: #ffffff; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h4 style='color: #764ba2; margin-bottom: 10px;'>Total Revenue</h4>
                <p style='font-size: 24px; font-weight: bold; color: #333; margin: 0;'>${results['total_revenue']:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            roi_color = '#28a745' if results['overall_roi'] > 0 else '#dc3545'
            st.markdown(f"""
            <div style='padding: 20px; background-color: #ffffff; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h4 style='color: #f093fb; margin-bottom: 10px;'>Overall ROI</h4>
                <p style='font-size: 24px; font-weight: bold; color: {roi_color}; margin: 0;'>{results['overall_roi']:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='padding: 20px; background-color: #ffffff; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center;'>
                <h4 style='color: #17a2b8; margin-bottom: 10px;'>Conversion Rate</h4>
                <p style='font-size: 24px; font-weight: bold; color: #333; margin: 0;'>{results['overall_conversion_rate']:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        # AI Insights Section
        st.markdown("---")
        st.markdown("## 🤖 AI-Powered Marketing Insights")
        
        with st.spinner("🔄 Generating AI insights..."):
            try:
                # Get the current data for AI analysis
                df = st.session_state.get('uploaded_data', st.session_state.get('sample_data'))
                
                # Prepare campaign data for AI analysis
                campaign_data = []
                for idx, row in df.iterrows():
                    try:
                        campaign_name = str(idx) if isinstance(idx, (int, str)) else f'Campaign {len(campaign_data) + 1}'
                        
                        # Safely extract values with proper error handling
                        budget = float(row.get('Budget', 0)) if pd.notna(row.get('Budget', 0)) else 0
                        revenue = float(row.get('Revenue', 0)) if pd.notna(row.get('Revenue', 0)) else 0
                        clicks = float(row.get('Clicks', 0)) if pd.notna(row.get('Clicks', 0)) else 0
                        conversions = float(row.get('Conversions', 0)) if pd.notna(row.get('Conversions', 0)) else 0
                        
                        campaign_data.append({
                            'campaign': campaign_name,
                            'budget': budget,
                            'revenue': revenue,
                            'roi': ((revenue - budget) / budget * 100) if budget > 0 else 0,
                            'conversion_rate': (conversions / clicks * 100) if clicks > 0 else 0
                        })
                    except Exception as e:
                        st.warning(f"Skipping campaign {idx} due to data error: {str(e)}")
                        continue
                
                # Generate AI insights
                ai_insights = llm_client.analyze_marketing_data(campaign_data)
                
                st.markdown("""
                <div style='padding: 20px; background-color: #e3f2fd; border-radius: 10px; border-left: 4px solid #2196f3; margin-bottom: 20px;'>
                    <h4 style='color: #1976d2; margin-bottom: 15px;'>🧠 AI Marketing Analysis</h4>
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
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-top: 20px;'>
        <p style='color: #f093fb; font-weight: bold; margin: 0;'>Marketing Analysis</p>
        <p style='color: #666; margin: 5px 0;'>Comprehensive Campaign Performance Analysis Platform</p>
        <p style='color: #999; font-size: 12px; margin: 5px 0;'>Educational Purpose Only</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 15px; background-color: #fff3cd; border-radius: 10px; border-left: 4px solid #ffc107; margin-top: 10px;'>
        <h4 style='color: #856404; margin-bottom: 10px;'>Educational Disclaimer</h4>
        <p style='color: #856404; margin: 0; font-size: 14px;'>This analysis is for educational purposes only and should not be considered as financial advice.</p>
        <p style='color: #856404; margin: 5px 0 0 0; font-size: 14px;'>Always consult with qualified marketing professionals before making business decisions.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()