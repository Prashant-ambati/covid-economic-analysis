import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataVisualizer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_covid_timeline(self, df, country=None):
        """
        Create an interactive timeline of COVID-19 cases and deaths
        
        Args:
            df (pd.DataFrame): COVID-19 data
            country (str, optional): Specific country to visualize
            
        Returns:
            plotly.graph_objects.Figure: Interactive plot
        """
        try:
            self.logger.info("Creating COVID-19 timeline visualization")
            
            if country:
                df = df[df['country'] == country]
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Add cases trace
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['cases_7day_avg'],
                    name="7-day Average Cases",
                    line=dict(color='blue')
                ),
                secondary_y=False
            )
            
            # Add deaths trace
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['deaths_7day_avg'],
                    name="7-day Average Deaths",
                    line=dict(color='red')
                ),
                secondary_y=True
            )
            
            # Update layout
            fig.update_layout(
                title=f"COVID-19 Timeline{' - ' + country if country else ''}",
                xaxis_title="Date",
                yaxis_title="Cases",
                yaxis2_title="Deaths",
                hovermode="x unified"
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating COVID-19 timeline: {str(e)}")
            raise

    def create_economic_indicators(self, df):
        """
        Create an interactive plot of economic indicators
        
        Args:
            df (pd.DataFrame): Economic data
            
        Returns:
            plotly.graph_objects.Figure: Interactive plot
        """
        try:
            self.logger.info("Creating economic indicators visualization")
            
            fig = make_subplots(rows=3, cols=1, subplot_titles=("GDP Growth", "Unemployment Rate", "Inflation Rate"))
            
            # Add GDP growth trace
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['gdp_growth'],
                    name="GDP Growth",
                    line=dict(color='green')
                ),
                row=1, col=1
            )
            
            # Add unemployment rate trace
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['unemployment_rate'],
                    name="Unemployment Rate",
                    line=dict(color='orange')
                ),
                row=2, col=1
            )
            
            # Add inflation rate trace
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['inflation_rate'],
                    name="Inflation Rate",
                    line=dict(color='purple')
                ),
                row=3, col=1
            )
            
            # Update layout
            fig.update_layout(
                title="Economic Indicators Over Time",
                height=900,
                showlegend=False,
                hovermode="x unified"
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating economic indicators visualization: {str(e)}")
            raise

    def create_correlation_heatmap(self, df):
        """
        Create a correlation heatmap between COVID-19 and economic indicators
        
        Args:
            df (pd.DataFrame): Merged data
            
        Returns:
            plotly.graph_objects.Figure: Interactive heatmap
        """
        try:
            self.logger.info("Creating correlation heatmap")
            
            # Calculate correlations
            corr_matrix = df[[
                'new_cases', 'new_deaths', 'case_fatality_rate',
                'gdp_growth', 'unemployment_rate', 'inflation_rate'
            ]].corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0
            ))
            
            fig.update_layout(
                title="Correlation Heatmap: COVID-19 vs Economic Indicators",
                xaxis_title="Variables",
                yaxis_title="Variables"
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating correlation heatmap: {str(e)}")
            raise

    def create_combined_dashboard(self, covid_df, economic_df, merged_df):
        """
        Create a comprehensive dashboard with multiple visualizations
        
        Args:
            covid_df (pd.DataFrame): COVID-19 data
            economic_df (pd.DataFrame): Economic data
            merged_df (pd.DataFrame): Merged data
            
        Returns:
            plotly.graph_objects.Figure: Interactive dashboard
        """
        try:
            self.logger.info("Creating combined dashboard")
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    "COVID-19 Timeline",
                    "Economic Indicators",
                    "Correlation Heatmap",
                    "Case Fatality Rate vs GDP Growth"
                )
            )
            
            # Add COVID-19 timeline
            covid_timeline = self.create_covid_timeline(covid_df)
            for trace in covid_timeline.data:
                fig.add_trace(trace, row=1, col=1)
            
            # Add economic indicators
            economic_plot = self.create_economic_indicators(economic_df)
            for trace in economic_plot.data:
                fig.add_trace(trace, row=1, col=2)
            
            # Add correlation heatmap
            heatmap = self.create_correlation_heatmap(merged_df)
            fig.add_trace(heatmap.data[0], row=2, col=1)
            
            # Add scatter plot
            fig.add_trace(
                go.Scatter(
                    x=merged_df['gdp_growth'],
                    y=merged_df['case_fatality_rate'],
                    mode='markers',
                    name='Case Fatality Rate vs GDP Growth'
                ),
                row=2, col=2
            )
            
            # Update layout
            fig.update_layout(
                title="COVID-19 and Economic Indicators Dashboard",
                height=1000,
                showlegend=True,
                hovermode="closest"
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating combined dashboard: {str(e)}")
            raise 