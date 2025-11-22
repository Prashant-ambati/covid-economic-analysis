"""
Example script demonstrating how to use the COVID-19 Economic Impact API
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:5000/api/v1"


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def example_health_check():
    """Example: Check API health"""
    print_section("Health Check")
    
    response = requests.get(f"{BASE_URL}/health")
    data = response.json()
    
    print(f"Status: {data['status']}")
    print(f"Timestamp: {data['timestamp']}")
    print(f"Database: {data['database']}")


def example_get_statistics():
    """Example: Get statistical summary"""
    print_section("Statistics Summary")
    
    response = requests.get(f"{BASE_URL}/statistics")
    data = response.json()
    
    if data['status'] == 'success':
        stats = data['statistics']
        
        print("COVID-19 Statistics:")
        print(f"  Total Cases: {stats['covid']['total_cases']:,}")
        print(f"  Total Deaths: {stats['covid']['total_deaths']:,}")
        print(f"  Avg New Cases: {stats['covid']['avg_new_cases']:.2f}")
        print(f"  Case Fatality Rate: {stats['covid']['case_fatality_rate']:.2f}%")
        
        print("\nEconomic Statistics:")
        print(f"  Avg GDP Growth: {stats['economic']['avg_gdp_growth']:.2f}%")
        print(f"  Avg Unemployment: {stats['economic']['avg_unemployment']:.2f}%")
        print(f"  Avg Inflation: {stats['economic']['avg_inflation']:.2f}%")
        print(f"  GDP Volatility: {stats['economic']['gdp_volatility']:.2f}")


def example_get_correlations():
    """Example: Get correlation analysis"""
    print_section("Correlation Analysis")
    
    response = requests.get(f"{BASE_URL}/correlations")
    data = response.json()
    
    if data['status'] == 'success':
        corr = data['correlations']
        
        print("COVID-19 Cases vs Economic Indicators:")
        print(f"  Cases vs GDP Growth: {corr['cases_vs_gdp']:.3f}")
        print(f"  Cases vs Unemployment: {corr['cases_vs_unemployment']:.3f}")
        print(f"  Cases vs Inflation: {corr['cases_vs_inflation']:.3f}")
        
        print("\nCOVID-19 Deaths vs Economic Indicators:")
        print(f"  Deaths vs GDP Growth: {corr['deaths_vs_gdp']:.3f}")
        print(f"  Deaths vs Unemployment: {corr['deaths_vs_unemployment']:.3f}")
        print(f"  Deaths vs Inflation: {corr['deaths_vs_inflation']:.3f}")
        
        print("\nInterpretation Guide:")
        for key, value in data['interpretation'].items():
            print(f"  {key.capitalize()}: {value}")


def example_get_covid_data():
    """Example: Get COVID-19 data with filters"""
    print_section("COVID-19 Data (Last 10 Records)")
    
    params = {
        'limit': 10
    }
    
    response = requests.get(f"{BASE_URL}/covid", params=params)
    data = response.json()
    
    if data['status'] == 'success':
        print(f"Total records returned: {data['count']}\n")
        
        for record in data['data'][:3]:  # Show first 3 records
            print(f"Date: {record['date']}")
            print(f"  Country: {record.get('country', 'N/A')}")
            print(f"  Cases: {record['cases']:,}")
            print(f"  Deaths: {record['deaths']:,}")
            print(f"  New Cases: {record['new_cases']:,}")
            print(f"  7-day Avg: {record['cases_7day_avg']:.2f}")
            print()


def example_get_trends():
    """Example: Get trend analysis"""
    print_section("Trend Analysis (7-day Moving Average)")
    
    params = {
        'window': 7
    }
    
    response = requests.get(f"{BASE_URL}/trends", params=params)
    data = response.json()
    
    if data['status'] == 'success':
        trends = data['trends']
        print(f"Window Size: {trends['window_size']} days")
        print(f"Total Data Points: {len(trends['dates'])}")
        
        # Show last 5 trend values
        print("\nLast 5 Days:")
        for i in range(-5, 0):
            print(f"  {trends['dates'][i]}: {trends['cases_trend'][i]:.2f} cases")


def example_get_economic_data():
    """Example: Get economic data"""
    print_section("Economic Data (Last 5 Records)")
    
    params = {
        'limit': 5
    }
    
    response = requests.get(f"{BASE_URL}/economic", params=params)
    data = response.json()
    
    if data['status'] == 'success':
        print(f"Total records returned: {data['count']}\n")
        
        for record in data['data']:
            print(f"Date: {record['date']}")
            print(f"  GDP Growth: {record['gdp_growth']:.2f}%")
            print(f"  Unemployment: {record['unemployment_rate']:.2f}%")
            print(f"  Inflation: {record['inflation_rate']:.2f}%")
            print()


def example_date_range_query():
    """Example: Query data with date range"""
    print_section("Date Range Query")
    
    # Query last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    params = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'limit': 5
    }
    
    print(f"Querying data from {params['start_date']} to {params['end_date']}\n")
    
    response = requests.get(f"{BASE_URL}/merged", params=params)
    data = response.json()
    
    if data['status'] == 'success':
        print(f"Records found: {data['count']}")
        
        if data['count'] > 0:
            print("\nSample Record:")
            record = data['data'][0]
            print(f"  Date: {record['date']}")
            print(f"  Cases: {record['cases']:,}")
            print(f"  GDP Growth: {record['gdp_growth']:.2f}%")
            print(f"  Unemployment: {record['unemployment_rate']:.2f}%")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("  COVID-19 Economic Impact API - Usage Examples")
    print("=" * 60)
    print("\nMake sure the API server is running on http://localhost:5000")
    print("Start it with: python src/api.py")
    
    try:
        # Run examples
        example_health_check()
        example_get_statistics()
        example_get_correlations()
        example_get_covid_data()
        example_get_economic_data()
        example_get_trends()
        example_date_range_query()
        
        print("\n" + "=" * 60)
        print("  All examples completed successfully!")
        print("=" * 60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server")
        print("Please make sure the API is running on http://localhost:5000")
        print("Start it with: python src/api.py\n")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")


if __name__ == "__main__":
    main()
