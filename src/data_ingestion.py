import requests
import pandas as pd
import logging
from datetime import datetime, timedelta
import os
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataIngestion:
    def __init__(self):
        self.base_url = "https://disease.sh/v3/covid-19"
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.data_dir, exist_ok=True)

    def fetch_covid_data(self, country="all"):
        """
        Fetch COVID-19 data from the disease.sh API
        
        Args:
            country (str): Country code or 'all' for global data
            
        Returns:
            pd.DataFrame: DataFrame containing COVID-19 data
        """
        try:
            url = f"{self.base_url}/historical/{country}"
            logger.info(f"Fetching COVID-19 data from {url}")
            
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # Process the data
            if country == "all":
                processed_data = self._process_global_data(data)
            else:
                processed_data = self._process_country_data(data)
            
            # Save to CSV
            filename = f"covid_data_{country}_{datetime.now().strftime('%Y%m%d')}.csv"
            filepath = os.path.join(self.data_dir, filename)
            processed_data.to_csv(filepath, index=False)
            logger.info(f"Data saved to {filepath}")
            
            return processed_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching COVID-19 data: {str(e)}")
            raise

    def _process_global_data(self, data):
        """Process global COVID-19 data"""
        processed_data = []
        
        # The API now returns a dictionary with 'cases', 'deaths', 'recovered' as keys
        for date, cases in data['cases'].items():
            processed_data.append({
                'date': date,
                'country': 'Global',
                'cases': cases,
                'deaths': data['deaths'].get(date, 0),
                'recovered': data['recovered'].get(date, 0)
            })
        
        return pd.DataFrame(processed_data)

    def _process_country_data(self, data):
        """Process country-specific COVID-19 data"""
        processed_data = []
        timeline = data['timeline']
        
        for date, cases in timeline['cases'].items():
            processed_data.append({
                'date': date,
                'country': data['country'],
                'cases': cases,
                'deaths': timeline['deaths'].get(date, 0),
                'recovered': timeline['recovered'].get(date, 0)
            })
        
        return pd.DataFrame(processed_data)

    def fetch_economic_data(self):
        """
        Fetch economic indicators data from World Bank API
        
        Returns:
            pd.DataFrame: DataFrame containing economic indicators
        """
        try:
            # This is a placeholder for World Bank API integration
            # In a real implementation, you would fetch actual economic data
            logger.info("Fetching economic indicators data")
            
            # For demonstration, we'll create sample economic data
            dates = pd.date_range(start='2020-01-01', end=datetime.now(), freq='M')
            economic_data = pd.DataFrame({
                'date': dates,
                'gdp_growth': np.random.uniform(-5, 5, len(dates)),
                'unemployment_rate': np.random.uniform(3, 15, len(dates)),
                'inflation_rate': np.random.uniform(1, 8, len(dates))
            })
            
            # Save to CSV
            filename = f"economic_data_{datetime.now().strftime('%Y%m%d')}.csv"
            filepath = os.path.join(self.data_dir, filename)
            economic_data.to_csv(filepath, index=False)
            logger.info(f"Economic data saved to {filepath}")
            
            return economic_data
            
        except Exception as e:
            logger.error(f"Error fetching economic data: {str(e)}")
            raise 