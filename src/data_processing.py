import pandas as pd
import numpy as np
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def clean_covid_data(self, df):
        """
        Clean and preprocess COVID-19 data
        
        Args:
            df (pd.DataFrame): Raw COVID-19 data
            
        Returns:
            pd.DataFrame: Cleaned and processed COVID-19 data
        """
        try:
            self.logger.info("Cleaning COVID-19 data")
            
            # Convert date column to datetime
            df['date'] = pd.to_datetime(df['date'])
            
            # Sort by date
            df = df.sort_values('date')
            
            # Handle missing values
            df = df.fillna(0)
            
            # Calculate daily new cases
            df['new_cases'] = df.groupby('country')['cases'].diff().fillna(0)
            df['new_deaths'] = df.groupby('country')['deaths'].diff().fillna(0)
            
            # Calculate 7-day moving averages
            df['cases_7day_avg'] = df.groupby('country')['new_cases'].transform(
                lambda x: x.rolling(window=7, min_periods=1).mean()
            )
            df['deaths_7day_avg'] = df.groupby('country')['new_deaths'].transform(
                lambda x: x.rolling(window=7, min_periods=1).mean()
            )
            
            # Calculate case fatality rate
            df['case_fatality_rate'] = (df['deaths'] / df['cases'] * 100).fillna(0)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error cleaning COVID-19 data: {str(e)}")
            raise

    def clean_economic_data(self, df):
        """
        Clean and preprocess economic data
        
        Args:
            df (pd.DataFrame): Raw economic data
            
        Returns:
            pd.DataFrame: Cleaned and processed economic data
        """
        try:
            self.logger.info("Cleaning economic data")
            
            # Convert date column to datetime
            df['date'] = pd.to_datetime(df['date'])
            
            # Sort by date
            df = df.sort_values('date')
            
            # Handle missing values using forward fill
            df = df.fillna(method='ffill')
            
            # Calculate percentage changes
            df['gdp_growth_change'] = df['gdp_growth'].pct_change() * 100
            df['unemployment_change'] = df['unemployment_rate'].pct_change() * 100
            df['inflation_change'] = df['inflation_rate'].pct_change() * 100
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error cleaning economic data: {str(e)}")
            raise

    def merge_datasets(self, covid_df, economic_df):
        """
        Merge COVID-19 and economic data
        
        Args:
            covid_df (pd.DataFrame): Processed COVID-19 data
            economic_df (pd.DataFrame): Processed economic data
            
        Returns:
            pd.DataFrame: Merged dataset
        """
        try:
            self.logger.info("Merging COVID-19 and economic data")
            
            # Convert dates to monthly frequency for economic data
            economic_df['month'] = economic_df['date'].dt.to_period('M')
            covid_df['month'] = covid_df['date'].dt.to_period('M')
            
            # Aggregate COVID data by month
            monthly_covid = covid_df.groupby(['country', 'month']).agg({
                'cases': 'max',
                'deaths': 'max',
                'new_cases': 'sum',
                'new_deaths': 'sum',
                'cases_7day_avg': 'mean',
                'deaths_7day_avg': 'mean',
                'case_fatality_rate': 'mean'
            }).reset_index()
            
            # Merge datasets
            merged_df = pd.merge(
                monthly_covid,
                economic_df,
                on='month',
                how='inner'
            )
            
            # Drop the month column as it's not needed in the final output
            merged_df = merged_df.drop('month', axis=1)
            
            # Calculate correlations
            correlations = self._calculate_correlations(merged_df)
            self.logger.info(f"Calculated correlations: {correlations}")
            
            return merged_df
            
        except Exception as e:
            self.logger.error(f"Error merging datasets: {str(e)}")
            raise

    def _calculate_correlations(self, df):
        """
        Calculate correlations between COVID-19 and economic indicators
        
        Args:
            df (pd.DataFrame): Merged dataset
            
        Returns:
            dict: Dictionary of correlation coefficients
        """
        correlations = {
            'cases_gdp': df['new_cases'].corr(df['gdp_growth']),
            'cases_unemployment': df['new_cases'].corr(df['unemployment_rate']),
            'cases_inflation': df['new_cases'].corr(df['inflation_rate']),
            'deaths_gdp': df['new_deaths'].corr(df['gdp_growth']),
            'deaths_unemployment': df['new_deaths'].corr(df['unemployment_rate']),
            'deaths_inflation': df['new_deaths'].corr(df['inflation_rate'])
        }
        
        return correlations 