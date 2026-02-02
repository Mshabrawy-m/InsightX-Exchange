"""
Marketing Analysis Module
Handles campaign data analysis, KPI calculations, and performance metrics
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from utils.config import get_marketing_config

class MarketingAnalyzer:
    """Class for comprehensive marketing campaign analysis"""
    
    def __init__(self):
        """Initialize marketing analyzer with configuration"""
        self.config = get_marketing_config()
    
    def validate_data(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate uploaded marketing data
        
        Args:
            df: DataFrame with marketing data
        
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        required_columns = list(self.config['expected_columns'].values())
        
        # Check if required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Check for empty data
        if df.empty:
            errors.append("No data found in the uploaded file")
        
        # Check for negative values in key metrics
        numeric_columns = ['Budget', 'Clicks', 'Conversions', 'Revenue']
        for col in numeric_columns:
            if col in df.columns:
                if (df[col] < 0).any():
                    errors.append(f"Negative values found in {col} column")
        
        # Check for zero values that would cause division errors
        if 'Clicks' in df.columns and (df['Clicks'] == 0).any():
            errors.append("Zero values found in Clicks column - cannot calculate conversion rate")
        
        if 'Budget' in df.columns and (df['Budget'] == 0).any():
            errors.append("Zero values found in Budget column - cannot calculate ROI")
        
        if 'Conversions' in df.columns and (df['Conversions'] == 0).any():
            errors.append("Zero values found in Conversions column - cannot calculate cost per conversion")
        
        return len(errors) == 0, errors
    
    def calculate_kpis(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate marketing KPIs
        
        Args:
            df: DataFrame with raw marketing data
        
        Returns:
            DataFrame with calculated KPIs
        """
        df = df.copy()
        
        # Click-Through Rate (CTR) = Clicks / Total Clicks * 100
        # Since we don't have impressions, we'll use relative CTR
        total_clicks = df['Clicks'].sum()
        df['CTR'] = (df['Clicks'] / total_clicks) * 100
        
        # Conversion Rate = Conversions / Clicks * 100
        df['Conversion_Rate'] = (df['Conversions'] / df['Clicks']) * 100
        
        # Cost per Click (CPC) = Budget / Clicks
        df['CPC'] = df['Budget'] / df['Clicks']
        
        # Cost per Conversion = Budget / Conversions
        df['Cost_per_Conversion'] = df['Budget'] / df['Conversions']
        
        # Return on Investment (ROI) = (Revenue - Budget) / Budget * 100
        df['ROI'] = ((df['Revenue'] - df['Budget']) / df['Budget']) * 100
        
        # Revenue per Click = Revenue / Clicks
        df['Revenue_per_Click'] = df['Revenue'] / df['Clicks']
        
        # Profit = Revenue - Budget
        df['Profit'] = df['Revenue'] - df['Budget']
        
        # Profit Margin = Profit / Revenue * 100
        df['Profit_Margin'] = (df['Profit'] / df['Revenue']) * 100
        
        return df
    
    def get_summary_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate summary statistics for marketing data
        
        Args:
            df: DataFrame with marketing KPIs
        
        Returns:
            Dictionary with summary statistics
        """
        numeric_columns = [
            'Budget', 'Clicks', 'Conversions', 'Revenue', 'CTR', 
            'Conversion_Rate', 'ROI', 'Cost_per_Conversion', 'Profit'
        ]
        
        summary = {}
        for col in numeric_columns:
            if col in df.columns:
                summary[col] = {
                    'total': df[col].sum(),
                    'average': df[col].mean(),
                    'median': df[col].median(),
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'std': df[col].std()
                }
        
        return summary
    
    def generate_performance_overview_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Generate enhanced performance overview chart with better formatting
        
        Args:
            df: DataFrame with marketing data
        
        Returns:
            Plotly figure object
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                '<b>💰 Budget vs Revenue</b>',
                '<b>📊 Clicks to Conversions</b>',
                '<b>🎯 ROI Performance</b>',
                '<b>📈 Conversion Rate</b>'
            ),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]],
            vertical_spacing=0.2,
            horizontal_spacing=0.15
        )
        
        # Budget vs Revenue (with better colors and formatting)
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['Budget'],
            name='Budget',
            marker=dict(color='#3498db', opacity=0.8, line=dict(color='#2980b9', width=1)),
            hovertemplate='<b>%{x}</b><br>Budget: $%{y:,.2f}<extra></extra>'
        ), row=1, col=1)
        
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['Revenue'],
            name='Revenue',
            marker=dict(color='#2ecc71', opacity=0.8, line=dict(color='#27ae60', width=1)),
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
        ), row=1, col=1)
        
        # Add profit/loss indicator
        profit_loss = df['Revenue'] - df['Budget']
        fig.add_trace(go.Scatter(
            x=df.index,
            y=profit_loss,
            mode='markers',
            name='Profit/Loss',
            marker=dict(
                size=10,
                color=['green' if x > 0 else 'red' for x in profit_loss],
                symbol=['triangle-up' if x > 0 else 'triangle-down' for x in profit_loss]
            ),
            hovertemplate='<b>%{x}</b><br>Profit/Loss: $%{y:,.2f}<extra></extra>'
        ), row=1, col=1)
        
        # Clicks to Conversion Funnel (enhanced)
        fig.add_trace(go.Funnel(
            y=df.index,
            x=df['Clicks'],
            name='Clicks',
            textposition='inside',
            textinfo='value+percent initial',
            marker=dict(color='#e74c3c', line=dict(color='#c0392b', width=2)),
            hovertemplate='<b>%{y}</b><br>Clicks: %{x:,.0f}<extra></extra>'
        ), row=1, col=2)
        
        fig.add_trace(go.Funnel(
            y=df.index,
            x=df['Conversions'],
            name='Conversions',
            textposition='inside',
            textinfo='value+percent previous',
            marker=dict(color='#f39c12', line=dict(color='#e67e22', width=2)),
            hovertemplate='<b>%{y}</b><br>Conversions: %{x:,.0f}<extra></extra>'
        ), row=1, col=2)
        
        # ROI Performance (enhanced with thresholds)
        roi_colors = ['#27ae60' if x >= 50 else '#f39c12' if x >= 10 else '#e74c3c' if x >= 0 else '#c0392b' for x in df['ROI']]
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['ROI'],
            name='ROI (%)',
            marker=dict(
                color=roi_colors,
                line=dict(color='black', width=1),
                opacity=0.8
            ),
            hovertemplate='<b>%{x}</b><br>ROI: %{y:.2f}%<extra></extra>'
        ), row=2, col=1)
        
        # Add ROI threshold lines
        fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.7, row=2, col=1)
        fig.add_hline(y=10, line_dash="dash", line_color="orange", opacity=0.7, row=2, col=1)
        fig.add_hline(y=50, line_dash="dash", line_color="green", opacity=0.7, row=2, col=1)
        
        # Conversion Rate Trend (enhanced)
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Conversion_Rate'],
            mode='lines+markers',
            name='Conversion Rate (%)',
            line=dict(color='#9b59b6', width=3, dash='solid'),
            marker=dict(size=8, color='#8e44ad', line=dict(color='black', width=1)),
            hovertemplate='<b>%{x}</b><br>Conversion Rate: %{y:.2f}%<extra></extra>'
        ), row=2, col=2)
        
        # Add average conversion rate line
        avg_conv_rate = df['Conversion_Rate'].mean()
        fig.add_hline(y=avg_conv_rate, line_dash="dot", line_color="gray", opacity=0.7, row=2, col=2)
        
        fig.update_layout(
            title={
                'text': '📊 Marketing Campaign Performance Dashboard',
                'x': 0.5,
                'xanchor': 'center',
                'font': dict(size=18, color='black'),
                'pad': {'t': 20, 'b': 20}
            },
            template='plotly_white',
            height=800,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,  # Position below the plot area
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            ),
            font=dict(size=10),
            margin=dict(l=50, r=50, t=80, b=120)  # Increased bottom margin
        )
        
        # Update y-axes labels
        fig.update_yaxes(title_text="Amount ($)", row=1, col=1)
        fig.update_yaxes(title_text="Count", row=1, col=2)
        fig.update_yaxes(title_text="ROI (%)", row=2, col=1)
        fig.update_yaxes(title_text="Conversion Rate (%)", row=2, col=2)
        
        # Update x-axes labels
        fig.update_xaxes(title_text="Campaign", row=2, col=1)
        fig.update_xaxes(title_text="Campaign", row=2, col=2)
        
        return fig
    
    def generate_kpi_comparison_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Generate enhanced KPI comparison chart with better visualization
        
        Args:
            df: DataFrame with marketing KPIs
        
        Returns:
            Plotly figure object
        """
        # Select key KPIs for comparison
        kpi_columns = ['CTR', 'Conversion_Rate', 'ROI', 'Cost_per_Conversion']
        kpi_data = df[kpi_columns].copy()
        
        # Create subplots for better comparison
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                '<b>📊 Click-Through Rate</b>',
                '<b>🎯 Conversion Rate</b>',
                '<b>💰 ROI Performance</b>',
                '<b>💸 Cost per Conversion</b>'
            ),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]],
            vertical_spacing=0.2,
            horizontal_spacing=0.15
        )
        
        # CTR Chart
        fig.add_trace(go.Bar(
            x=kpi_data.index,
            y=kpi_data['CTR'],
            name='CTR (%)',
            marker=dict(
                color=['#3498db' if x >= 2 else '#e74c3c' for x in kpi_data['CTR']],
                opacity=0.8,
                line=dict(color='black', width=1)
            ),
            hovertemplate='<b>%{x}</b><br>CTR: %{y:.2f}%<extra></extra>'
        ), row=1, col=1)
        
        # Add industry average CTR line (2%)
        fig.add_hline(y=2, line_dash="dash", line_color="orange", opacity=0.7, row=1, col=1)
        
        # Conversion Rate Chart
        fig.add_trace(go.Bar(
            x=kpi_data.index,
            y=kpi_data['Conversion_Rate'],
            name='Conversion Rate (%)',
            marker=dict(
                color=['#2ecc71' if x >= 3 else '#f39c12' for x in kpi_data['Conversion_Rate']],
                opacity=0.8,
                line=dict(color='black', width=1)
            ),
            hovertemplate='<b>%{x}</b><br>Conversion Rate: %{y:.2f}%<extra></extra>',
            showlegend=False
        ), row=1, col=2)
        
        # Add industry average conversion rate line (3%)
        fig.add_hline(y=3, line_dash="dash", line_color="purple", opacity=0.7, row=1, col=2)
        
        # ROI Chart
        roi_colors = ['#27ae60' if x >= 50 else '#f39c12' if x >= 10 else '#e74c3c' if x >= 0 else '#c0392b' for x in kpi_data['ROI']]
        fig.add_trace(go.Bar(
            x=kpi_data.index,
            y=kpi_data['ROI'],
            name='ROI (%)',
            marker=dict(
                color=roi_colors,
                opacity=0.8,
                line=dict(color='black', width=1)
            ),
            hovertemplate='<b>%{x}</b><br>ROI: %{y:.2f}%<extra></extra>',
            showlegend=False
        ), row=2, col=1)
        
        # Add ROI threshold lines
        fig.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.7, row=2, col=1)
        fig.add_hline(y=10, line_dash="dash", line_color="orange", opacity=0.7, row=2, col=1)
        fig.add_hline(y=50, line_dash="dash", line_color="green", opacity=0.7, row=2, col=1)
        
        # Cost per Conversion Chart (inverted - lower is better)
        cpc_colors = ['#27ae60' if x <= 50 else '#f39c12' if x <= 100 else '#e74c3c' for x in kpi_data['Cost_per_Conversion']]
        fig.add_trace(go.Bar(
            x=kpi_data.index,
            y=kpi_data['Cost_per_Conversion'],
            name='Cost per Conversion ($)',
            marker=dict(
                color=cpc_colors,
                opacity=0.8,
                line=dict(color='black', width=1)
            ),
            hovertemplate='<b>%{x}</b><br>Cost per Conversion: $%{y:.2f}<extra></extra>',
            showlegend=False
        ), row=2, col=2)
        
        # Add cost per conversion threshold lines
        fig.add_hline(y=50, line_dash="dash", line_color="green", opacity=0.7, row=2, col=2)
        fig.add_hline(y=100, line_dash="dash", line_color="orange", opacity=0.7, row=2, col=2)
        
        fig.update_layout(
            title={
                'text': '📈 Key Performance Indicators Comparison',
                'x': 0.5,
                'xanchor': 'center',
                'font': dict(size=18, color='black'),
                'pad': {'t': 20, 'b': 20}
            },
            template='plotly_white',
            height=700,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,  # Position below the plot area
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            ),
            font=dict(size=10),
            margin=dict(l=50, r=50, t=80, b=120)  # Increased bottom margin
        )
        
        # Update y-axes labels
        fig.update_yaxes(title_text="CTR (%)", row=1, col=1)
        fig.update_yaxes(title_text="Conversion Rate (%)", row=1, col=2)
        fig.update_yaxes(title_text="ROI (%)", row=2, col=1)
        fig.update_yaxes(title_text="Cost per Conversion ($)", row=2, col=2)
        
        # Update x-axes labels with better formatting
        fig.update_xaxes(title_text="Campaign", tickangle=45, tickfont=dict(size=9), row=1, col=1)
        fig.update_xaxes(title_text="Campaign", tickangle=45, tickfont=dict(size=9), row=1, col=2)
        fig.update_xaxes(title_text="Campaign", tickangle=45, tickfont=dict(size=9), row=2, col=1)
        fig.update_xaxes(title_text="Campaign", tickangle=45, tickfont=dict(size=9), row=2, col=2)
        
        return fig
    
    def generate_roi_analysis_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Generate enhanced ROI analysis chart with better insights
        
        Args:
            df: DataFrame with marketing data
        
        Returns:
            Plotly figure object
        """
        # Create ROI categories with better labels
        df_roi = df.copy()
        df_roi['ROI_Category'] = pd.cut(
            df_roi['ROI'],
            bins=[-float('inf'), -10, 0, 10, 50, float('inf')],
            labels=['🔴 Poor (<-10%)', '🟡 Negative (-10% to 0%)', '🟠 Break-even (0% to 10%)', 
                   '🟢 Good (10% to 50%)', '💚 Excellent (>50%)']
        )
        
        # Create bubble chart with enhanced features
        fig = go.Figure()
        
        # Add bubbles for each campaign
        for category in df_roi['ROI_Category'].unique():
            category_data = df_roi[df_roi['ROI_Category'] == category]
            
            fig.add_trace(go.Scatter(
                x=category_data['Budget'],
                y=category_data['Revenue'],
                mode='markers',
                name=category,
                marker=dict(
                    size=category_data['Conversions'] * 2,  # Size based on conversions
                    sizemode='diameter',
                    sizeref=2.*max(df_roi['Conversions'])/(40**2),
                    color=category_data['ROI'],
                    colorscale='RdYlGn',  # Red to Green color scale
                    showscale=True,
                    colorbar=dict(title="ROI (%)"),
                    line=dict(color='black', width=1),
                    opacity=0.8
                ),
                text=category_data.index,
                hovertemplate='<b>%{text}</b><br>' +
                             'Budget: $%{x:,.2f}<br>' +
                             'Revenue: $%{y:,.2f}<br>' +
                             'Conversions: %{marker.size:.0f}<br>' +
                             'ROI: %{marker.color:.2f}%<extra></extra>'
            ))
        
        # Add break-even line (where Revenue = Budget)
        max_budget = df_roi['Budget'].max()
        fig.add_trace(go.Scatter(
            x=[0, max_budget],
            y=[0, max_budget],
            mode='lines',
            name='Break-even Line',
            line=dict(color='red', width=2, dash='dash'),
            hovertemplate='Break-even Point<extra></extra>'
        ))
        
        # Add ideal ROI line (50% ROI)
        fig.add_trace(go.Scatter(
            x=[0, max_budget],
            y=[0, max_budget * 1.5],
            mode='lines',
            name='50% ROI Target',
            line=dict(color='green', width=2, dash='dot'),
            hovertemplate='50% ROI Target<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': '🎯 ROI Analysis: Budget vs Revenue Performance',
                'x': 0.5,
                'xanchor': 'center',
                'font': dict(size=18, color='black'),
                'pad': {'t': 20, 'b': 20}
            },
            xaxis_title='💰 Budget ($)',
            yaxis_title='💵 Revenue ($)',
            template='plotly_white',
            height=650,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,  # Position below the plot area
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            ),
            font=dict(size=10),
            margin=dict(l=60, r=60, t=80, b=120)  # Increased bottom margin
        )
        
        # Format axes to show currency
        fig.update_xaxes(tickprefix='$', tickformat=',.0f')
        fig.update_yaxes(tickprefix='$', tickformat=',.0f')
        
        return fig
    
    def generate_efficiency_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """
        Generate campaign efficiency heatmap for quick performance assessment
        
        Args:
            df: DataFrame with marketing data
        
        Returns:
            Plotly figure object
        """
        # Create efficiency scores
        df_efficiency = df.copy()
        
        # Normalize metrics to 0-100 scale for heatmap
        df_efficiency['ROI_Score'] = np.clip((df_efficiency['ROI'] + 100) / 2, 0, 100)  # Convert ROI to 0-100
        df_efficiency['CTR_Score'] = np.clip(df_efficiency['CTR'] * 10, 0, 100)  # CTR to 0-100
        df_efficiency['Conv_Score'] = np.clip(df_efficiency['Conversion_Rate'] * 10, 0, 100)  # Conv rate to 0-100
        df_efficiency['CPC_Score'] = np.clip(100 - (df_efficiency['Cost_per_Conversion'] / 2), 0, 100)  # Invert CPC (lower is better)
        
        # Create heatmap data
        metrics = ['ROI_Score', 'CTR_Score', 'Conv_Score', 'CPC_Score']
        metric_labels = ['ROI Performance', 'CTR Performance', 'Conversion Performance', 'Cost Efficiency']
        
        heatmap_data = []
        for metric in metrics:
            heatmap_data.append(df_efficiency[metric].values)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=df_efficiency.index,
            y=metric_labels,
            colorscale='RdYlGn',  # Red to Green
            zmid=50,  # Middle point
            hoverongaps=False,
            hovertemplate='<b>%{x}</b><br>%{y}: %{z:.1f}<extra></extra>',
            colorbar=dict(title="Performance Score")
        ))
        
        fig.update_layout(
            title={
                'text': '🔥 Campaign Efficiency Heatmap',
                'x': 0.5,
                'xanchor': 'center',
                'font': dict(size=18, color='black'),
                'pad': {'t': 20, 'b': 20}
            },
            xaxis_title='Campaign',
            yaxis_title='Performance Metrics',
            template='plotly_white',
            height=450,
            font=dict(size=10),
            margin=dict(l=80, r=80, t=80, b=100)
        )
        
        # Rotate x-axis labels for better readability
        fig.update_xaxes(tickangle=45, tickfont=dict(size=9))
        
        return fig
    
    def identify_best_performers(self, df: pd.DataFrame) -> Dict:
        """
        Identify best and worst performing campaigns
        
        Args:
            df: DataFrame with marketing KPIs
        
        Returns:
            Dictionary with performance rankings
        """
        rankings = {}
        
        # Best ROI
        best_roi_idx = df['ROI'].idxmax()
        worst_roi_idx = df['ROI'].idxmin()
        
        rankings['best_roi'] = {
            'campaign': best_roi_idx,
            'value': df.loc[best_roi_idx, 'ROI'],
            'revenue': df.loc[best_roi_idx, 'Revenue'],
            'budget': df.loc[best_roi_idx, 'Budget']
        }
        
        rankings['worst_roi'] = {
            'campaign': worst_roi_idx,
            'value': df.loc[worst_roi_idx, 'ROI'],
            'revenue': df.loc[worst_roi_idx, 'Revenue'],
            'budget': df.loc[worst_roi_idx, 'Budget']
        }
        
        # Best Conversion Rate
        best_conv_idx = df['Conversion_Rate'].idxmax()
        worst_conv_idx = df['Conversion_Rate'].idxmin()
        
        rankings['best_conversion'] = {
            'campaign': best_conv_idx,
            'value': df.loc[best_conv_idx, 'Conversion_Rate'],
            'conversions': df.loc[best_conv_idx, 'Conversions'],
            'clicks': df.loc[best_conv_idx, 'Clicks']
        }
        
        rankings['worst_conversion'] = {
            'campaign': worst_conv_idx,
            'value': df.loc[worst_conv_idx, 'Conversion_Rate'],
            'conversions': df.loc[worst_conv_idx, 'Conversions'],
            'clicks': df.loc[worst_conv_idx, 'Clicks']
        }
        
        # Most Profitable
        best_profit_idx = df['Profit'].idxmax()
        worst_profit_idx = df['Profit'].idxmin()
        
        rankings['most_profitable'] = {
            'campaign': best_profit_idx,
            'value': df.loc[best_profit_idx, 'Profit'],
            'revenue': df.loc[best_profit_idx, 'Revenue'],
            'budget': df.loc[best_profit_idx, 'Budget']
        }
        
        rankings['least_profitable'] = {
            'campaign': worst_profit_idx,
            'value': df.loc[worst_profit_idx, 'Profit'],
            'revenue': df.loc[worst_profit_idx, 'Revenue'],
            'budget': df.loc[worst_profit_idx, 'Budget']
        }
        
        return rankings
    
    def get_comprehensive_analysis(self, df: pd.DataFrame) -> Dict:
        """
        Perform comprehensive marketing analysis
        
        Args:
            df: DataFrame with raw marketing data
        
        Returns:
            Dictionary with all analysis results
        """
        # Validate data
        is_valid, errors = self.validate_data(df)
        if not is_valid:
            return {'error': errors}
        
        # Calculate KPIs
        df_with_kpis = self.calculate_kpis(df)
        
        # Generate charts
        performance_chart = self.generate_performance_overview_chart(df_with_kpis)
        kpi_comparison_chart = self.generate_kpi_comparison_chart(df_with_kpis)
        roi_chart = self.generate_roi_analysis_chart(df_with_kpis)
        efficiency_heatmap = self.generate_efficiency_heatmap(df_with_kpis)
        
        # Get statistics and rankings
        summary_stats = self.get_summary_statistics(df_with_kpis)
        rankings = self.identify_best_performers(df_with_kpis)
        
        return {
            'data': df_with_kpis,
            'performance_chart': performance_chart,
            'kpi_comparison_chart': kpi_comparison_chart,
            'roi_chart': roi_chart,
            'efficiency_heatmap': efficiency_heatmap,
            'summary_statistics': summary_stats,
            'rankings': rankings,
            'total_metrics': {
                'total_budget': df_with_kpis['Budget'].sum(),
                'total_revenue': df_with_kpis['Revenue'].sum(),
                'total_clicks': df_with_kpis['Clicks'].sum(),
                'total_conversions': df_with_kpis['Conversions'].sum(),
                'overall_roi': ((df_with_kpis['Revenue'].sum() - df_with_kpis['Budget'].sum()) / 
                              df_with_kpis['Budget'].sum()) * 100,
                'overall_conversion_rate': (df_with_kpis['Conversions'].sum() / 
                                      df_with_kpis['Clicks'].sum()) * 100
            }
        }
