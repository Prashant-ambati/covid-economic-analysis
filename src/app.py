import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
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

# Initialize the Dash app with a dark theme
app = dash.Dash(
    __name__,
    title='COVID-19 Economic Impact Dashboard',
    external_stylesheets=[
        dbc.themes.DARKLY,
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
    ]
)

# Custom CSS for premium dark look
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background-color: #121212;
                color: #ffffff;
            }
            .nav-link {
                color: #ffffff !important;
                font-weight: 500;
            }
            .card {
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                transition: transform 0.2s;
                background-color: #1e1e1e;
                border: 1px solid #2d2d2d;
            }
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
            }
            .stat-card {
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                color: white;
                border: 1px solid #3d3d3d;
            }
            .footer {
                background-color: #1a1a1a;
                color: #ffffff;
                padding: 2rem 0;
                margin-top: 2rem;
                border-top: 1px solid #2d2d2d;
            }
            .navbar {
                background-color: #1a1a1a !important;
                border-bottom: 1px solid #2d2d2d;
            }
            .navbar-brand {
                color: #ffffff !important;
                font-weight: 600;
            }
            .date-picker {
                background-color: #1e1e1e !important;
                color: #ffffff !important;
                border: 1px solid #2d2d2d !important;
            }
            .date-picker .DayPicker-Day {
                color: #ffffff !important;
            }
            .date-picker .DayPicker-Day--selected {
                background-color: #3498db !important;
            }
            .form-check-input:checked {
                background-color: #3498db;
                border-color: #3498db;
            }
            .form-check-label {
                color: #ffffff;
            }
            .lead {
                color: #b0b0b0;
            }
            .display-4 {
                color: #ffffff;
            }
            .card-header {
                background-color: #2d2d2d;
                border-bottom: 1px solid #3d3d3d;
            }
            .card-title {
                color: #ffffff;
            }
            .hr {
                border-color: #2d2d2d;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Initialize database manager
db_manager = DatabaseManager()

# Navigation Bar
navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("COVID-19 Economic Impact Dashboard", className="ms-2"),
        dbc.Nav([
            dbc.NavItem(dbc.NavLink("Overview", href="#overview")),
            dbc.NavItem(dbc.NavLink("Analysis", href="#analysis")),
            dbc.NavItem(dbc.NavLink("Insights", href="#insights")),
            dbc.NavItem(dbc.NavLink("About", href="#about")),
        ], className="ms-auto")
    ]),
    color="dark",
    className="mb-4",
)

# Define the layout
app.layout = html.Div([
    navbar,
    dbc.Container([
        # Header Section
        dbc.Row([
            dbc.Col([
                html.H1('COVID-19 Economic Impact Analysis',
                       className='display-4 mb-4 text-center'),
                html.P('Analyzing the relationship between COVID-19 and economic indicators worldwide',
                      className='lead text-center mb-5')
            ])
        ]),
        
        # Quick Stats Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Cases", className="card-title"),
                        html.H2(id="total-cases", className="mb-0"),
                        html.P("Global Cases", className="text-muted mb-0")
                    ])
                ], className="stat-card mb-4")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("GDP Impact", className="card-title"),
                        html.H2(id="gdp-impact", className="mb-0"),
                        html.P("Average Growth", className="text-muted mb-0")
                    ])
                ], className="stat-card mb-4")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Unemployment", className="card-title"),
                        html.H2(id="unemployment-stat", className="mb-0"),
                        html.P("Global Rate", className="text-muted mb-0")
                    ])
                ], className="stat-card mb-4")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Inflation Rate", className="card-title"),
                        html.H2(id="inflation-stat", className="mb-0"),
                        html.P("Average Rate", className="text-muted mb-0")
                    ])
                ], className="stat-card mb-4")
            ], width=3),
        ]),
        
        # Filters Section
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H5("Date Range", className="text-white"),
                        dcc.DatePickerRange(
                            id='date-range',
                            start_date=datetime.now() - timedelta(days=365),
                            end_date=datetime.now(),
                            className='mb-3 date-picker'
                        )
                    ], width=6),
                    dbc.Col([
                        html.H5("Metrics", className="text-white"),
                        dbc.Checklist(
                            id='metrics-selector',
                            options=[
                                {'label': 'Cases', 'value': 'cases'},
                                {'label': 'Deaths', 'value': 'deaths'},
                                {'label': 'GDP', 'value': 'gdp'},
                                {'label': 'Unemployment', 'value': 'unemployment'}
                            ],
                            value=['cases', 'gdp'],
                            inline=True
                        )
                    ], width=6)
                ])
            ])
        ], className="mb-4"),
        
        # Main Charts Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H3("COVID-19 Timeline", className="mb-0 text-white")),
                    dbc.CardBody([
                        dcc.Graph(id='covid-timeline')
                    ])
                ], className="mb-4")
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H3("Economic Indicators", className="mb-0 text-white")),
                    dbc.CardBody([
                        dcc.Graph(id='economic-indicators')
                    ])
                ], className="mb-4")
            ], width=12)
        ]),
        
        # Analysis Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H3("Correlation Analysis", className="mb-0 text-white")),
                    dbc.CardBody([
                        dcc.Graph(id='correlation-heatmap')
                    ])
                ], className="mb-4")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H3("Trend Analysis", className="mb-0 text-white")),
                    dbc.CardBody([
                        dcc.Graph(id='trend-analysis')
                    ])
                ], className="mb-4")
            ], width=6)
        ]),
        
        # Insights Section
        dbc.Card([
            dbc.CardHeader(html.H3("Key Insights", className="mb-0 text-white")),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H5("Economic Impact", className="text-white"),
                        html.P(id="economic-insight", className="lead")
                    ], width=6),
                    dbc.Col([
                        html.H5("Recovery Indicators", className="text-white"),
                        html.P(id="recovery-insight", className="lead")
                    ], width=6)
                ])
            ])
        ], className="mb-4"),
        
        # Footer
        html.Footer([
            html.Hr(className="hr"),
            dbc.Row([
                dbc.Col([
                    html.P("Data Sources:", className="font-weight-bold text-white"),
                    html.Ul([
                        html.Li("WHO COVID-19 Dashboard"),
                        html.Li("World Bank Economic Indicators"),
                        html.Li("IMF Economic Outlook")
                    ], className="text-muted")
                ], width=4),
                dbc.Col([
                    html.P("Last Updated:", className="font-weight-bold text-white"),
                    html.P(id="last-updated", className="text-muted")
                ], width=4),
                dbc.Col([
                    html.P("Disclaimer:", className="font-weight-bold text-white"),
                    html.P("This dashboard is for informational purposes only.", className="text-muted")
                ], width=4)
            ])
        ], className="footer")
    ], fluid=True, className="py-4")
])

@app.callback(
    [Output('covid-timeline', 'figure'),
     Output('economic-indicators', 'figure'),
     Output('correlation-heatmap', 'figure'),
     Output('trend-analysis', 'figure'),
     Output('total-cases', 'children'),
     Output('gdp-impact', 'children'),
     Output('unemployment-stat', 'children'),
     Output('inflation-stat', 'children'),
     Output('economic-insight', 'children'),
     Output('recovery-insight', 'children'),
     Output('last-updated', 'children')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('metrics-selector', 'value')]
)
def update_dashboard(start_date, end_date, selected_metrics):
    try:
        # Get data from database
        covid_data = db_manager.get_covid_data(start_date=start_date, end_date=end_date)
        economic_data = db_manager.get_economic_data(start_date=start_date, end_date=end_date)
        merged_data = db_manager.get_merged_data(start_date=start_date, end_date=end_date)
        
        # COVID-19 Timeline with improved styling
        covid_fig = go.Figure()
        if 'cases' in selected_metrics:
            covid_fig.add_trace(go.Scatter(
                x=covid_data['date'],
                y=covid_data['cases'],
                name='Total Cases',
                line=dict(color='#3498db', width=2),
                fill='tozeroy',
                fillcolor='rgba(52, 152, 219, 0.1)'
            ))
        if 'deaths' in selected_metrics:
            covid_fig.add_trace(go.Scatter(
                x=covid_data['date'],
                y=covid_data['deaths'],
                name='Total Deaths',
                line=dict(color='#e74c3c', width=2),
                fill='tozeroy',
                fillcolor='rgba(231, 76, 60, 0.1)'
            ))
        covid_fig.update_layout(
            title=None,
            xaxis_title='Date',
            yaxis_title='Count',
            hovermode='x unified',
            template='plotly_dark',
            margin=dict(l=40, r=40, t=40, b=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Economic Indicators with improved styling
        economic_fig = go.Figure()
        economic_fig.add_trace(go.Scatter(
            x=economic_data['date'],
            y=economic_data['gdp_growth'],
            name='GDP Growth',
            line=dict(color='#2ecc71', width=2)
        ))
        economic_fig.add_trace(go.Scatter(
            x=economic_data['date'],
            y=economic_data['unemployment_rate'],
            name='Unemployment Rate',
            line=dict(color='#f1c40f', width=2)
        ))
        economic_fig.add_trace(go.Scatter(
            x=economic_data['date'],
            y=economic_data['inflation_rate'],
            name='Inflation Rate',
            line=dict(color='#9b59b6', width=2)
        ))
        economic_fig.update_layout(
            title=None,
            xaxis_title='Date',
            yaxis_title='Value',
            hovermode='x unified',
            template='plotly_dark',
            margin=dict(l=40, r=40, t=40, b=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Correlation Heatmap with improved styling
        correlation_data = merged_data[['cases', 'deaths', 'gdp_growth', 'unemployment_rate', 'inflation_rate']].corr()
        heatmap_fig = px.imshow(
            correlation_data,
            labels=dict(x="Variable", y="Variable", color="Correlation"),
            x=correlation_data.columns,
            y=correlation_data.columns,
            color_continuous_scale='RdBu',
            aspect='auto'
        )
        heatmap_fig.update_layout(
            title=None,
            margin=dict(l=40, r=40, t=40, b=40),
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Trend Analysis
        trend_fig = go.Figure()
        trend_fig.add_trace(go.Scatter(
            x=merged_data['date'],
            y=merged_data['cases'].rolling(window=7).mean(),
            name='7-day Moving Average (Cases)',
            line=dict(color='#3498db', width=2)
        ))
        trend_fig.update_layout(
            title=None,
            xaxis_title='Date',
            yaxis_title='7-day Moving Average',
            template='plotly_dark',
            margin=dict(l=40, r=40, t=40, b=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Calculate stats for cards
        total_cases = f"{int(covid_data['cases'].max()):,}"
        gdp_impact = f"{economic_data['gdp_growth'].mean():.1f}%"
        unemployment = f"{economic_data['unemployment_rate'].mean():.1f}%"
        inflation = f"{economic_data['inflation_rate'].mean():.1f}%"
        
        # Generate insights
        economic_insight = "GDP growth shows significant correlation with COVID-19 cases, indicating direct economic impact."
        recovery_insight = "Economic recovery patterns vary by region, with some showing faster recovery rates."
        
        # Last updated
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return (
            covid_fig, economic_fig, heatmap_fig, trend_fig,
            total_cases, gdp_impact, unemployment, inflation,
            economic_insight, recovery_insight, last_updated
        )
        
    except Exception as e:
        logger.error(f"Error updating dashboard: {str(e)}")
        return [{} for _ in range(11)]  # Return empty figures and stats

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050) 