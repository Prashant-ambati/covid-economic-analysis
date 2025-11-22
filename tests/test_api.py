"""
Unit tests for the COVID-19 Economic Impact API
"""

import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_root_endpoint(client):
    """Test the root endpoint returns API information"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'COVID-19 Economic Impact API'
    assert data['version'] == 'v1'
    assert data['status'] == 'active'
    assert 'endpoints' in data


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert data['database'] == 'connected'


def test_covid_data_endpoint(client):
    """Test the COVID-19 data endpoint"""
    response = client.get('/api/v1/covid')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'count' in data
    assert 'data' in data


def test_covid_data_with_filters(client):
    """Test COVID-19 data endpoint with query parameters"""
    response = client.get('/api/v1/covid?limit=10')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['count'] <= 10


def test_economic_data_endpoint(client):
    """Test the economic data endpoint"""
    response = client.get('/api/v1/economic')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'count' in data
    assert 'data' in data


def test_merged_data_endpoint(client):
    """Test the merged data endpoint"""
    response = client.get('/api/v1/merged')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'count' in data
    assert 'data' in data


def test_statistics_endpoint(client):
    """Test the statistics endpoint"""
    response = client.get('/api/v1/statistics')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'statistics' in data
    assert 'covid' in data['statistics']
    assert 'economic' in data['statistics']
    assert 'period' in data['statistics']


def test_correlations_endpoint(client):
    """Test the correlations endpoint"""
    response = client.get('/api/v1/correlations')
    # May return 404 if no data, which is acceptable
    assert response.status_code in [200, 404]
    data = response.get_json()
    assert data['status'] in ['success', 'error']
    
    if response.status_code == 200:
        assert 'correlations' in data
        assert 'interpretation' in data


def test_trends_endpoint(client):
    """Test the trends endpoint"""
    response = client.get('/api/v1/trends')
    # May return 404 if no data, which is acceptable
    assert response.status_code in [200, 404]
    data = response.get_json()
    assert data['status'] in ['success', 'error']
    
    if response.status_code == 200:
        assert 'trends' in data


def test_trends_with_window(client):
    """Test trends endpoint with custom window parameter"""
    response = client.get('/api/v1/trends?window=14')
    assert response.status_code in [200, 404]
    data = response.get_json()
    
    if response.status_code == 200:
        assert data['trends']['window_size'] == 14


def test_invalid_endpoint(client):
    """Test that invalid endpoints return 404"""
    response = client.get('/api/v1/invalid')
    assert response.status_code == 404


def test_cors_headers(client):
    """Test that CORS headers are present"""
    response = client.get('/api/v1/health')
    assert 'Access-Control-Allow-Origin' in response.headers


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
