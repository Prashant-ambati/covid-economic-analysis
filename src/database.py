import sqlite3
import pandas as pd
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_name="covid_economic.db"):
        self.db_name = db_name
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', db_name)
        self.conn = None
        self.cursor = None
        self.logger = logging.getLogger(__name__)

    def connect(self):
        """Establish connection to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Error connecting to database: {str(e)}")
            raise

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed")

    def create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            self.connect()
            
            # Create COVID-19 data table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS covid_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    country TEXT,
                    cases INTEGER,
                    deaths INTEGER,
                    recovered INTEGER,
                    new_cases INTEGER,
                    new_deaths INTEGER,
                    cases_7day_avg REAL,
                    deaths_7day_avg REAL,
                    case_fatality_rate REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create economic data table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS economic_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    gdp_growth REAL,
                    unemployment_rate REAL,
                    inflation_rate REAL,
                    gdp_growth_change REAL,
                    unemployment_change REAL,
                    inflation_change REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create merged data table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS merged_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    country TEXT,
                    cases INTEGER,
                    deaths INTEGER,
                    new_cases INTEGER,
                    new_deaths INTEGER,
                    cases_7day_avg REAL,
                    deaths_7day_avg REAL,
                    case_fatality_rate REAL,
                    gdp_growth REAL,
                    unemployment_rate REAL,
                    inflation_rate REAL,
                    gdp_growth_change REAL,
                    unemployment_change REAL,
                    inflation_change REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            self.logger.info("Database tables created successfully")
            
        except sqlite3.Error as e:
            self.logger.error(f"Error creating tables: {str(e)}")
            raise
        finally:
            self.disconnect()

    def insert_covid_data(self, df):
        """Insert COVID-19 data into database"""
        try:
            self.connect()
            df.to_sql('covid_data', self.conn, if_exists='append', index=False)
            self.logger.info(f"Inserted {len(df)} rows into covid_data table")
        except Exception as e:
            self.logger.error(f"Error inserting COVID-19 data: {str(e)}")
            raise
        finally:
            self.disconnect()

    def insert_economic_data(self, df):
        """Insert economic data into database"""
        try:
            self.connect()
            df.to_sql('economic_data', self.conn, if_exists='append', index=False)
            self.logger.info(f"Inserted {len(df)} rows into economic_data table")
        except Exception as e:
            self.logger.error(f"Error inserting economic data: {str(e)}")
            raise
        finally:
            self.disconnect()

    def insert_merged_data(self, df):
        """Insert merged data into database"""
        try:
            self.connect()
            df.to_sql('merged_data', self.conn, if_exists='append', index=False)
            self.logger.info(f"Inserted {len(df)} rows into merged_data table")
        except Exception as e:
            self.logger.error(f"Error inserting merged data: {str(e)}")
            raise
        finally:
            self.disconnect()

    def get_covid_data(self, country=None, start_date=None, end_date=None):
        """Retrieve COVID-19 data from database"""
        try:
            self.connect()
            query = "SELECT * FROM covid_data"
            params = []
            
            if country or start_date or end_date:
                query += " WHERE"
                conditions = []
                
                if country:
                    conditions.append(" country = ?")
                    params.append(country)
                
                if start_date:
                    conditions.append(" date >= ?")
                    params.append(start_date)
                
                if end_date:
                    conditions.append(" date <= ?")
                    params.append(end_date)
                
                query += " AND".join(conditions)
            
            df = pd.read_sql_query(query, self.conn, params=params)
            self.logger.info(f"Retrieved {len(df)} rows from covid_data table")
            return df
            
        except Exception as e:
            self.logger.error(f"Error retrieving COVID-19 data: {str(e)}")
            raise
        finally:
            self.disconnect()

    def get_economic_data(self, start_date=None, end_date=None):
        """Retrieve economic data from database"""
        try:
            self.connect()
            query = "SELECT * FROM economic_data"
            params = []
            
            if start_date or end_date:
                query += " WHERE"
                conditions = []
                
                if start_date:
                    conditions.append(" date >= ?")
                    params.append(start_date)
                
                if end_date:
                    conditions.append(" date <= ?")
                    params.append(end_date)
                
                query += " AND".join(conditions)
            
            df = pd.read_sql_query(query, self.conn, params=params)
            self.logger.info(f"Retrieved {len(df)} rows from economic_data table")
            return df
            
        except Exception as e:
            self.logger.error(f"Error retrieving economic data: {str(e)}")
            raise
        finally:
            self.disconnect()

    def get_merged_data(self, country=None, start_date=None, end_date=None):
        """Retrieve merged data from database"""
        try:
            self.connect()
            query = "SELECT * FROM merged_data"
            params = []
            
            if country or start_date or end_date:
                query += " WHERE"
                conditions = []
                
                if country:
                    conditions.append(" country = ?")
                    params.append(country)
                
                if start_date:
                    conditions.append(" date >= ?")
                    params.append(start_date)
                
                if end_date:
                    conditions.append(" date <= ?")
                    params.append(end_date)
                
                query += " AND".join(conditions)
            
            df = pd.read_sql_query(query, self.conn, params=params)
            self.logger.info(f"Retrieved {len(df)} rows from merged_data table")
            return df
            
        except Exception as e:
            self.logger.error(f"Error retrieving merged data: {str(e)}")
            raise
        finally:
            self.disconnect() 