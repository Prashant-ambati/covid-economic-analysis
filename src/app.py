import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from database import DatabaseManager
import logging
import dash_bootstrap_components as dbc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the Dash app with dark theme
app = dash.Dash(
    __name__,
    title='COVID-19 Economic Analysis',
    external_stylesheets=[dbc.themes.DARKLY]
)

# Initialize database manager
db_manager = DatabaseManager()

# Define the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('COVID-19 and Economic Indicators Analysis',
                   className='text-center my-4',
                   style={'color': '#fff'})
        ])
    ]),
    
    # Date Range Selector
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Select Date Range', className='text-center mb-3'),
                    dcc.DatePickerRange(
                        id='date-range',
                        start_date=pd.to_datetime('2020-01-01'),
                        end_date=pd.to_datetime('2023-12-31'),
                        className='w-100'
                    )
                ])
            ], className='mb-4')
        ])
    ]),
    
    # COVID-19 Timeline
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('COVID-19 Timeline', className='text-center mb-3'),
                    dcc.Graph(id='covid-timeline')
                ])
            ], className='mb-4')
        ])
    ]),
    
    # Economic Indicators
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('Economic Indicators', className='text-center mb-3'),
                    dcc.Graph(id='economic-indicators')
                ])
            ], className='mb-4')
        ])
    ]),
    
    # Correlation Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2('Correlation Analysis', className='text-center mb-3'),
                    dcc.Graph(id='correlation-heatmap')
                ])
            ], className='mb-4')
        ])
    ])
], fluid=True, className='py-4')

@app.callback(
    [Output('covid-timeline', 'figure'),
     Output('economic-indicators', 'figure'),
     Output('correlation-heatmap', 'figure')],
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
            line=dict(color='#3498db')
        ))
        covid_fig.add_trace(go.Scatter(
            x=covid_data['date'],
            y=covid_data['deaths'],
            name='Total Deaths',
            line=dict(color='#e74c3c')
        ))
        covid_fig.update_layout(
            title='COVID-19 Cases and Deaths Over Time',
            xaxis_title='Date',
            yaxis_title='Count',
            hovermode='x unified',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Economic Indicators
        economic_fig = go.Figure()
        economic_fig.add_trace(go.Scatter(
            x=economic_data['date'],
            y=economic_data['gdp_growth'],
            name='GDP Growth',
            line=dict(color='#2ecc71')
        ))
        economic_fig.add_trace(go.Scatter(
            x=economic_data['date'],
            y=economic_data['unemployment_rate'],
            name='Unemployment Rate',
            line=dict(color='#f1c40f')
        ))
        economic_fig.add_trace(go.Scatter(
            x=economic_data['date'],
            y=economic_data['inflation_rate'],
            name='Inflation Rate',
            line=dict(color='#9b59b6')
        ))
        economic_fig.update_layout(
            title='Economic Indicators Over Time',
            xaxis_title='Date',
            yaxis_title='Value',
            hovermode='x unified',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
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
        heatmap_fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return covid_fig, economic_fig, heatmap_fig
        
    except Exception as e:
        logger.error(f"Error updating graphs: {str(e)}")
        return {}, {}, {}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050) 