import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.data_processing import DataProcessor

@pytest.fixture
def sample_covid_data():
    """Create sample COVID-19 data for testing"""
    dates = pd.date_range(start='2020-01-01', end='2020-01-10', freq='D')
    return pd.DataFrame({
        'date': dates,
        'country': ['US'] * len(dates),
        'cases': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
        'deaths': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'recovered': [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    })

@pytest.fixture
def sample_economic_data():
    """Create sample economic data for testing"""
    dates = pd.date_range(start='2020-01-01', end='2020-01-10', freq='D')
    return pd.DataFrame({
        'date': dates,
        'gdp_growth': [2.5, 2.4, 2.3, 2.2, 2.1, 2.0, 1.9, 1.8, 1.7, 1.6],
        'unemployment_rate': [3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4],
        'inflation_rate': [2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9]
    })

def test_clean_covid_data(sample_covid_data):
    """Test cleaning and processing of COVID-19 data"""
    processor = DataProcessor()
    processed_data = processor.clean_covid_data(sample_covid_data)
    
    # Check if new columns are created
    assert 'new_cases' in processed_data.columns
    assert 'new_deaths' in processed_data.columns
    assert 'cases_7day_avg' in processed_data.columns
    assert 'deaths_7day_avg' in processed_data.columns
    assert 'case_fatality_rate' in processed_data.columns
    
    # Check if date column is datetime
    assert pd.api.types.is_datetime64_any_dtype(processed_data['date'])
    
    # Check if data is sorted by date
    assert processed_data['date'].is_monotonic_increasing
    
    # Check if new_cases calculation is correct
    assert processed_data['new_cases'].iloc[1] == 100  # 200 - 100 = 100

def test_clean_economic_data(sample_economic_data):
    """Test cleaning and processing of economic data"""
    processor = DataProcessor()
    processed_data = processor.clean_economic_data(sample_economic_data)
    
    # Check if new columns are created
    assert 'gdp_growth_change' in processed_data.columns
    assert 'unemployment_change' in processed_data.columns
    assert 'inflation_change' in processed_data.columns
    
    # Check if date column is datetime
    assert pd.api.types.is_datetime64_any_dtype(processed_data['date'])
    
    # Check if data is sorted by date
    assert processed_data['date'].is_monotonic_increasing
    
    # Check if percentage changes are calculated correctly
    assert abs(processed_data['gdp_growth_change'].iloc[1] - (-4.0)) < 0.01  # (2.4-2.5)/2.5 * 100

def test_merge_datasets(sample_covid_data, sample_economic_data):
    """Test merging of COVID-19 and economic data"""
    processor = DataProcessor()
    
    # Process both datasets
    processed_covid = processor.clean_covid_data(sample_covid_data)
    processed_economic = processor.clean_economic_data(sample_economic_data)
    
    # Merge datasets
    merged_data = processor.merge_datasets(processed_covid, processed_economic)
    
    # Check if merged data contains all necessary columns
    required_columns = [
        'date', 'country', 'cases', 'deaths', 'new_cases', 'new_deaths',
        'cases_7day_avg', 'deaths_7day_avg', 'case_fatality_rate',
        'gdp_growth', 'unemployment_rate', 'inflation_rate'
    ]
    assert all(col in merged_data.columns for col in required_columns)
    
    # Check if data is properly merged
    assert len(merged_data) > 0
    assert not merged_data.isnull().values.any()

def test_calculate_correlations(sample_covid_data, sample_economic_data):
    """Test calculation of correlations"""
    processor = DataProcessor()
    
    # Process and merge datasets
    processed_covid = processor.clean_covid_data(sample_covid_data)
    processed_economic = processor.clean_economic_data(sample_economic_data)
    merged_data = processor.merge_datasets(processed_covid, processed_economic)
    
    # Calculate correlations
    correlations = processor._calculate_correlations(merged_data)
    
    # Check if correlations are calculated
    assert 'cases_gdp' in correlations
    assert 'cases_unemployment' in correlations
    assert 'cases_inflation' in correlations
    assert 'deaths_gdp' in correlations
    assert 'deaths_unemployment' in correlations
    assert 'deaths_inflation' in correlations
    
    # Check if correlation values are between -1 and 1
    for value in correlations.values():
        assert -1 <= value <= 1 