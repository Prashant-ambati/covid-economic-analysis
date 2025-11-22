"""
REST API for COVID-19 Economic Impact Analysis
Provides endpoints for accessing COVID-19 and economic data programmatically
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from database import DatabaseManager
import pandas as pd
import logging
from datetime import datetime, timedelta
from functools import wraps
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize database manager
db_manager = DatabaseManager()

# API Configuration
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"


def handle_errors(f):
    """Decorator to handle errors consistently across endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({
                'error': str(e),
                'status': 'error'
            }), 500
    return decorated_function


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        'name': 'COVID-19 Economic Impact API',
        'version': API_VERSION,
        'status': 'active',
        'endpoints': {
            'health': f'{API_PREFIX}/health',
            'covid_data': f'{API_PREFIX}/covid',
            'economic_data': f'{API_PREFIX}/economic',
            'merged_data': f'{API_PREFIX}/merged',
            'statistics': f'{API_PREFIX}/statistics',
            'correlations': f'{API_PREFIX}/correlations'
        },
        'documentation': 'https://github.com/yourusername/covid_economic_analysis'
    })


@app.route(f'{API_PREFIX}/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected'
    })


@app.route(f'{API_PREFIX}/covid', methods=['GET'])
@handle_errors
def get_covid_data():
    """
    Get COVID-19 data with optional filters
    
    Query Parameters:
        - country: Filter by country name
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
        - limit: Maximum number of records to return
    """
    country = request.args.get('country')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', type=int)
    
    # Fetch data from database
    df = db_manager.get_covid_data(
        country=country,
        start_date=start_date,
        end_date=end_date
    )
    
    # Apply limit if specified
    if limit:
        df = df.head(limit)
    
    # Convert to JSON
    data = df.to_dict(orient='records')
    
    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data
    })


@app.route(f'{API_PREFIX}/economic', methods=['GET'])
@handle_errors
def get_economic_data():
    """
    Get economic data with optional filters
    
    Query Parameters:
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
        - limit: Maximum number of records to return
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', type=int)
    
    # Fetch data from database
    df = db_manager.get_economic_data(
        start_date=start_date,
        end_date=end_date
    )
    
    # Apply limit if specified
    if limit:
        df = df.head(limit)
    
    # Convert to JSON
    data = df.to_dict(orient='records')
    
    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data
    })


@app.route(f'{API_PREFIX}/merged', methods=['GET'])
@handle_errors
def get_merged_data():
    """
    Get merged COVID-19 and economic data
    
    Query Parameters:
        - country: Filter by country name
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
        - limit: Maximum number of records to return
    """
    country = request.args.get('country')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', type=int)
    
    # Fetch data from database
    df = db_manager.get_merged_data(
        country=country,
        start_date=start_date,
        end_date=end_date
    )
    
    # Apply limit if specified
    if limit:
        df = df.head(limit)
    
    # Convert to JSON
    data = df.to_dict(orient='records')
    
    return jsonify({
        'status': 'success',
        'count': len(data),
        'data': data
    })


@app.route(f'{API_PREFIX}/statistics', methods=['GET'])
@handle_errors
def get_statistics():
    """
    Get statistical summary of the data
    
    Query Parameters:
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Fetch data
    covid_df = db_manager.get_covid_data(start_date=start_date, end_date=end_date)
    economic_df = db_manager.get_economic_data(start_date=start_date, end_date=end_date)
    
    # Calculate statistics
    stats = {
        'covid': {
            'total_cases': int(covid_df['cases'].max()) if not covid_df.empty else 0,
            'total_deaths': int(covid_df['deaths'].max()) if not covid_df.empty else 0,
            'avg_new_cases': float(covid_df['new_cases'].mean()) if not covid_df.empty else 0,
            'avg_new_deaths': float(covid_df['new_deaths'].mean()) if not covid_df.empty else 0,
            'case_fatality_rate': float(covid_df['case_fatality_rate'].mean()) if not covid_df.empty else 0
        },
        'economic': {
            'avg_gdp_growth': float(economic_df['gdp_growth'].mean()) if not economic_df.empty else 0,
            'avg_unemployment': float(economic_df['unemployment_rate'].mean()) if not economic_df.empty else 0,
            'avg_inflation': float(economic_df['inflation_rate'].mean()) if not economic_df.empty else 0,
            'gdp_volatility': float(economic_df['gdp_growth'].std()) if not economic_df.empty else 0
        },
        'period': {
            'start_date': start_date or 'N/A',
            'end_date': end_date or 'N/A',
            'data_points': len(covid_df)
        }
    }
    
    return jsonify({
        'status': 'success',
        'statistics': stats
    })


@app.route(f'{API_PREFIX}/correlations', methods=['GET'])
@handle_errors
def get_correlations():
    """
    Get correlation analysis between COVID-19 and economic indicators
    
    Query Parameters:
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Fetch merged data
    df = db_manager.get_merged_data(start_date=start_date, end_date=end_date)
    
    if df.empty:
        return jsonify({
            'status': 'error',
            'message': 'No data available for the specified period'
        }), 404
    
    # Calculate correlations
    correlations = {
        'cases_vs_gdp': float(df['cases'].corr(df['gdp_growth'])),
        'cases_vs_unemployment': float(df['cases'].corr(df['unemployment_rate'])),
        'cases_vs_inflation': float(df['cases'].corr(df['inflation_rate'])),
        'deaths_vs_gdp': float(df['deaths'].corr(df['gdp_growth'])),
        'deaths_vs_unemployment': float(df['deaths'].corr(df['unemployment_rate'])),
        'deaths_vs_inflation': float(df['deaths'].corr(df['inflation_rate']))
    }
    
    return jsonify({
        'status': 'success',
        'correlations': correlations,
        'interpretation': {
            'strong': 'Correlation > 0.7 or < -0.7',
            'moderate': 'Correlation between 0.3-0.7 or -0.3 to -0.7',
            'weak': 'Correlation between -0.3 and 0.3'
        }
    })


@app.route(f'{API_PREFIX}/trends', methods=['GET'])
@handle_errors
def get_trends():
    """
    Get trend analysis for COVID-19 and economic indicators
    
    Query Parameters:
        - window: Rolling window size (default: 7)
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
    """
    window = request.args.get('window', default=7, type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Fetch data
    covid_df = db_manager.get_covid_data(start_date=start_date, end_date=end_date)
    
    if covid_df.empty:
        return jsonify({
            'status': 'error',
            'message': 'No data available for the specified period'
        }), 404
    
    # Calculate trends
    covid_df['date'] = pd.to_datetime(covid_df['date'])
    covid_df = covid_df.sort_values('date')
    
    trends = {
        'cases_trend': covid_df['new_cases'].rolling(window=window).mean().tolist(),
        'deaths_trend': covid_df['new_deaths'].rolling(window=window).mean().tolist(),
        'dates': covid_df['date'].dt.strftime('%Y-%m-%d').tolist(),
        'window_size': window
    }
    
    return jsonify({
        'status': 'success',
        'trends': trends
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
