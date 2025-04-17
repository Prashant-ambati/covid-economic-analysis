import logging
import os
from datetime import datetime, timedelta
from data_ingestion import DataIngestion
from data_processing import DataProcessor
from database import DatabaseManager
from visualization import DataVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('covid_economic_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting COVID-19 and Economic Indicators Analysis Pipeline")
        
        # Initialize components
        data_ingestion = DataIngestion()
        data_processor = DataProcessor()
        db_manager = DatabaseManager()
        visualizer = DataVisualizer()
        
        # Create database tables
        logger.info("Creating database tables")
        db_manager.create_tables()
        
        # Fetch and process COVID-19 data
        logger.info("Fetching COVID-19 data")
        covid_data = data_ingestion.fetch_covid_data()
        processed_covid_data = data_processor.clean_covid_data(covid_data)
        db_manager.insert_covid_data(processed_covid_data)
        
        # Fetch and process economic data
        logger.info("Fetching economic data")
        economic_data = data_ingestion.fetch_economic_data()
        processed_economic_data = data_processor.clean_economic_data(economic_data)
        db_manager.insert_economic_data(processed_economic_data)
        
        # Merge and analyze datasets
        logger.info("Merging and analyzing datasets")
        merged_data = data_processor.merge_datasets(processed_covid_data, processed_economic_data)
        db_manager.insert_merged_data(merged_data)
        
        # Create visualizations
        logger.info("Creating visualizations")
        
        # COVID-19 timeline
        covid_timeline = visualizer.create_covid_timeline(processed_covid_data)
        covid_timeline.write_html("covid_timeline.html")
        
        # Economic indicators
        economic_plot = visualizer.create_economic_indicators(processed_economic_data)
        economic_plot.write_html("economic_indicators.html")
        
        # Correlation analysis
        correlation_heatmap = visualizer.create_correlation_heatmap(merged_data)
        correlation_heatmap.write_html("correlation_heatmap.html")
        
        # Combined dashboard
        dashboard = visualizer.create_combined_dashboard(
            processed_covid_data,
            processed_economic_data,
            merged_data
        )
        dashboard.write_html("dashboard.html")
        
        logger.info("Pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main() 