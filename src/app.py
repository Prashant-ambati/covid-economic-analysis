import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from database import DatabaseManager
import logging
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, 
                title='COVID-19 Economic Analysis',
                external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initialize database manager
db_manager = DatabaseManager()

# Define the layout with Bootstrap components
app.layout = dbc.Container([
    # Header with copyright
    dbc.Row([
        dbc.Col([
            html.H1('COVID-19 and Economic Indicators Analysis', 
                   className='text-center my-4'),
            html.P('© 2024 Prashant Ambati', 
                  className='text-center text-muted')
        ])
    ]),
    
    # Date Range Selector
    dbc.Row([
        dbc.Col([
            html.H3('Select Date Range', className='text-center'),
            dcc.DatePickerRange(
                id='date-range',
                start_date=pd.to_datetime('2020-01-01'),
                end_date=pd.to_datetime('2023-12-31'),
                className='d-flex justify-content-center'
            )
        ], className='mb-4')
    ]),
    
    # Main content in tabs
    dbc.Tabs([
        # COVID-19 Analysis Tab
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='covid-timeline')
                ], className='mb-4'),
                dbc.Col([
                    dcc.Graph(id='covid-daily')
                ], className='mb-4')
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='covid-regional')
                ], className='mb-4')
            ])
        ], label='COVID-19 Analysis'),
        
        # Economic Indicators Tab
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='economic-indicators')
                ], className='mb-4'),
                dbc.Col([
                    dcc.Graph(id='economic-forecast')
                ], className='mb-4')
            ])
        ], label='Economic Indicators'),
        
        # Correlation Analysis Tab
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='correlation-heatmap')
                ], className='mb-4'),
                dbc.Col([
                    dcc.Graph(id='scatter-matrix')
                ], className='mb-4')
            ])
        ], label='Correlation Analysis'),
        
        # Insights Tab
        dbc.Tab([
            dbc.Row([
                dbc.Col([
                    html.Div(id='key-insights')
                ], className='mb-4')
            ])
        ], label='Key Insights')
    ])
], fluid=True)

# Callbacks for all graphs
@app.callback(
    [Output('covid-timeline', 'figure'),
     Output('covid-daily', 'figure'),
     Output('covid-regional', 'figure'),
     Output('economic-indicators', 'figure'),
     Output('economic-forecast', 'figure'),
     Output('correlation-heatmap', 'figure'),
     Output('scatter-matrix', 'figure'),
     Output('key-insights', 'children')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_graphs(start_date, end_date):
    try:
        # Get data from database
        covid_data = db_manager.get_covid_data(start_date=start_date, end_date=end_date)
        economic_data = db_manager.get_economic_data(start_date=start_date, end_date=end_date)
        merged_data = db_manager.get_merged_data(start_date=start_date, end_date=end_date)
        
        # COVID-19 Timeline
        covid_fig = go.Figure()
        covid_fig.add_trace(go.Scatter(
            x=covid_data['date'],
            y=covid_data['cases'],
            name='Total Cases',
            line=dict(color='blue')
        ))
        covid_fig.add_trace(go.Scatter(
            x=covid_data['date'],
            y=covid_data['deaths'],
            name='Total Deaths',
            line=dict(color='red')
        ))
        covid_fig.update_layout(
            title='COVID-19 Cases and Deaths Over Time',
            xaxis_title='Date',
            yaxis_title='Count',
            hovermode='x unified',
            template='plotly_white'
        )
        
        # Daily Cases
        daily_fig = go.Figure()
        daily_fig.add_trace(go.Bar(
            x=covid_data['date'],
            y=covid_data['daily_cases'],
            name='Daily Cases',
            marker_color='blue'
        ))
        daily_fig.update_layout(
            title='Daily COVID-19 Cases',
            xaxis_title='Date',
            yaxis_title='Cases',
            template='plotly_white'
        )
        
        # Regional Analysis
        regional_fig = px.choropleth(
            covid_data,
            locations='country',
            locationmode='country names',
            color='cases',
            hover_name='country',
            animation_frame='date',
            title='Regional COVID-19 Cases Distribution'
        )
        
        # Economic Indicators
        economic_fig = go.Figure()
        economic_fig.add_trace(go.Scatter(
            x=economic_data['date'],
            y=economic_data['gdp_growth'],
            name='GDP Growth',
            line=dict(color='green')
        ))
        economic_fig.add_trace(go.Scatter(
            x=economic_data['date'],
            y=economic_data['unemployment_rate'],
            name='Unemployment Rate',
            line=dict(color='orange')
        ))
        economic_fig.add_trace(go.Scatter(
            x=economic_data['date'],
            y=economic_data['inflation_rate'],
            name='Inflation Rate',
            line=dict(color='purple')
        ))
        economic_fig.update_layout(
            title='Economic Indicators Over Time',
            xaxis_title='Date',
            yaxis_title='Value',
            hovermode='x unified',
            template='plotly_white'
        )
        
        # Economic Forecast
        forecast_fig = go.Figure()
        # Add forecast visualization here
        forecast_fig.update_layout(
            title='Economic Indicators Forecast',
            template='plotly_white'
        )
        
        # Correlation Heatmap
        correlation_data = merged_data[['cases', 'deaths', 'gdp_growth', 'unemployment_rate', 'inflation_rate']].corr()
        heatmap_fig = px.imshow(
            correlation_data,
            labels=dict(x="Variable", y="Variable", color="Correlation"),
            x=correlation_data.columns,
            y=correlation_data.columns,
            color_continuous_scale='RdBu',
            title='Correlation Heatmap'
        )
        
        # Scatter Matrix
        scatter_fig = px.scatter_matrix(
            merged_data,
            dimensions=['cases', 'deaths', 'gdp_growth', 'unemployment_rate', 'inflation_rate'],
            title='Scatter Matrix of Variables'
        )
        
        # Key Insights
        insights = dbc.Card([
            dbc.CardHeader("Key Insights"),
            dbc.CardBody([
                html.H5("COVID-19 Impact Analysis"),
                html.P("The data shows a strong correlation between COVID-19 cases and economic indicators."),
                html.H5("Economic Recovery"),
                html.P("Economic indicators show signs of recovery post-pandemic."),
                html.H5("Regional Variations"),
                html.P("Different regions show varying patterns in COVID-19 impact and economic recovery.")
            ])
        ])
        
        return covid_fig, daily_fig, regional_fig, economic_fig, forecast_fig, heatmap_fig, scatter_fig, insights
        
    except Exception as e:
        logger.error(f"Error updating graphs: {str(e)}")
        return {}, {}, {}, {}, {}, {}, {}, html.Div("Error loading data")

# Make the app compatible with Render
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050) 