"""
Data export functionality for COVID-19 Economic Impact Analysis
Supports multiple export formats: JSON, CSV, Excel
"""

import pandas as pd
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from database import DatabaseManager

logger = logging.getLogger(__name__)


class DataExporter:
    """Handle data export in various formats"""
    
    def __init__(self, output_dir: str = 'exports'):
        """
        Initialize data exporter
        
        Args:
            output_dir (str): Directory for exported files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.db_manager = DatabaseManager()
        logger.info(f"DataExporter initialized with output_dir: {output_dir}")
    
    def _generate_filename(self, base_name: str, extension: str) -> Path:
        """
        Generate filename with timestamp
        
        Args:
            base_name (str): Base name for the file
            extension (str): File extension
            
        Returns:
            Path: Full file path
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{base_name}_{timestamp}.{extension}"
        return self.output_dir / filename
    
    def export_to_json(
        self,
        data: pd.DataFrame,
        filename: Optional[str] = None,
        orient: str = 'records'
    ) -> str:
        """
        Export data to JSON format
        
        Args:
            data (pd.DataFrame): Data to export
            filename (str, optional): Custom filename
            orient (str): JSON orientation (records, split, index, etc.)
            
        Returns:
            str: Path to exported file
        """
        try:
            if filename is None:
                filepath = self._generate_filename('export', 'json')
            else:
                filepath = self.output_dir / filename
            
            # Convert DataFrame to JSON
            data.to_json(filepath, orient=orient, date_format='iso', indent=2)
            
            logger.info(f"Exported {len(data)} records to JSON: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error exporting to JSON: {str(e)}")
            raise
    
    def export_to_csv(
        self,
        data: pd.DataFrame,
        filename: Optional[str] = None,
        include_index: bool = False
    ) -> str:
        """
        Export data to CSV format
        
        Args:
            data (pd.DataFrame): Data to export
            filename (str, optional): Custom filename
            include_index (bool): Include DataFrame index
            
        Returns:
            str: Path to exported file
        """
        try:
            if filename is None:
                filepath = self._generate_filename('export', 'csv')
            else:
                filepath = self.output_dir / filename
            
            # Convert DataFrame to CSV
            data.to_csv(filepath, index=include_index, encoding='utf-8')
            
            logger.info(f"Exported {len(data)} records to CSV: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            raise
    
    def export_to_excel(
        self,
        data: pd.DataFrame,
        filename: Optional[str] = None,
        sheet_name: str = 'Data',
        include_index: bool = False
    ) -> str:
        """
        Export data to Excel format
        
        Args:
            data (pd.DataFrame): Data to export
            filename (str, optional): Custom filename
            sheet_name (str): Name of the Excel sheet
            include_index (bool): Include DataFrame index
            
        Returns:
            str: Path to exported file
        """
        try:
            if filename is None:
                filepath = self._generate_filename('export', 'xlsx')
            else:
                filepath = self.output_dir / filename
            
            # Convert DataFrame to Excel
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                data.to_excel(writer, sheet_name=sheet_name, index=include_index)
            
            logger.info(f"Exported {len(data)} records to Excel: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error exporting to Excel: {str(e)}")
            raise
    
    def export_covid_data(
        self,
        format: str = 'csv',
        country: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> str:
        """
        Export COVID-19 data
        
        Args:
            format (str): Export format (json, csv, excel)
            country (str, optional): Filter by country
            start_date (str, optional): Start date filter
            end_date (str, optional): End date filter
            
        Returns:
            str: Path to exported file
        """
        logger.info(f"Exporting COVID-19 data in {format} format")
        
        # Fetch data from database
        data = self.db_manager.get_covid_data(
            country=country,
            start_date=start_date,
            end_date=end_date
        )
        
        if data.empty:
            raise ValueError("No data available for export")
        
        # Export based on format
        if format.lower() == 'json':
            return self.export_to_json(data, 'covid_data.json')
        elif format.lower() == 'csv':
            return self.export_to_csv(data, 'covid_data.csv')
        elif format.lower() in ['excel', 'xlsx']:
            return self.export_to_excel(data, 'covid_data.xlsx', sheet_name='COVID-19 Data')
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def export_economic_data(
        self,
        format: str = 'csv',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> str:
        """
        Export economic data
        
        Args:
            format (str): Export format (json, csv, excel)
            start_date (str, optional): Start date filter
            end_date (str, optional): End date filter
            
        Returns:
            str: Path to exported file
        """
        logger.info(f"Exporting economic data in {format} format")
        
        # Fetch data from database
        data = self.db_manager.get_economic_data(
            start_date=start_date,
            end_date=end_date
        )
        
        if data.empty:
            raise ValueError("No data available for export")
        
        # Export based on format
        if format.lower() == 'json':
            return self.export_to_json(data, 'economic_data.json')
        elif format.lower() == 'csv':
            return self.export_to_csv(data, 'economic_data.csv')
        elif format.lower() in ['excel', 'xlsx']:
            return self.export_to_excel(data, 'economic_data.xlsx', sheet_name='Economic Data')
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def export_merged_data(
        self,
        format: str = 'csv',
        country: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> str:
        """
        Export merged COVID-19 and economic data
        
        Args:
            format (str): Export format (json, csv, excel)
            country (str, optional): Filter by country
            start_date (str, optional): Start date filter
            end_date (str, optional): End date filter
            
        Returns:
            str: Path to exported file
        """
        logger.info(f"Exporting merged data in {format} format")
        
        # Fetch data from database
        data = self.db_manager.get_merged_data(
            country=country,
            start_date=start_date,
            end_date=end_date
        )
        
        if data.empty:
            raise ValueError("No data available for export")
        
        # Export based on format
        if format.lower() == 'json':
            return self.export_to_json(data, 'merged_data.json')
        elif format.lower() == 'csv':
            return self.export_to_csv(data, 'merged_data.csv')
        elif format.lower() in ['excel', 'xlsx']:
            return self.export_to_excel(data, 'merged_data.xlsx', sheet_name='Merged Data')
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def export_all(
        self,
        format: str = 'excel',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> str:
        """
        Export all data types to a single file (Excel only)
        
        Args:
            format (str): Export format (only excel supported)
            start_date (str, optional): Start date filter
            end_date (str, optional): End date filter
            
        Returns:
            str: Path to exported file
        """
        if format.lower() not in ['excel', 'xlsx']:
            raise ValueError("export_all only supports Excel format")
        
        logger.info("Exporting all data to Excel")
        
        # Fetch all data
        covid_data = self.db_manager.get_covid_data(
            start_date=start_date,
            end_date=end_date
        )
        economic_data = self.db_manager.get_economic_data(
            start_date=start_date,
            end_date=end_date
        )
        merged_data = self.db_manager.get_merged_data(
            start_date=start_date,
            end_date=end_date
        )
        
        # Create Excel file with multiple sheets
        filepath = self._generate_filename('all_data', 'xlsx')
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            if not covid_data.empty:
                covid_data.to_excel(writer, sheet_name='COVID-19', index=False)
            if not economic_data.empty:
                economic_data.to_excel(writer, sheet_name='Economic', index=False)
            if not merged_data.empty:
                merged_data.to_excel(writer, sheet_name='Merged', index=False)
        
        logger.info(f"Exported all data to Excel: {filepath}")
        return str(filepath)
    
    def get_export_summary(self) -> Dict[str, Any]:
        """
        Get summary of available exports
        
        Returns:
            dict: Export summary information
        """
        exports = list(self.output_dir.glob('*'))
        
        return {
            'output_directory': str(self.output_dir),
            'total_exports': len(exports),
            'exports': [
                {
                    'filename': f.name,
                    'size_bytes': f.stat().st_size,
                    'created': datetime.fromtimestamp(f.stat().st_ctime).isoformat()
                }
                for f in exports
            ]
        }


# CLI interface
if __name__ == '__main__':
    import argparse
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='Export COVID-19 and economic data')
    parser.add_argument('--type', choices=['covid', 'economic', 'merged', 'all'],
                       default='merged', help='Data type to export')
    parser.add_argument('--format', choices=['json', 'csv', 'excel'],
                       default='csv', help='Export format')
    parser.add_argument('--country', help='Filter by country')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--output-dir', default='exports', help='Output directory')
    
    args = parser.parse_args()
    
    # Create exporter
    exporter = DataExporter(output_dir=args.output_dir)
    
    try:
        # Export based on type
        if args.type == 'covid':
            filepath = exporter.export_covid_data(
                format=args.format,
                country=args.country,
                start_date=args.start_date,
                end_date=args.end_date
            )
        elif args.type == 'economic':
            filepath = exporter.export_economic_data(
                format=args.format,
                start_date=args.start_date,
                end_date=args.end_date
            )
        elif args.type == 'merged':
            filepath = exporter.export_merged_data(
                format=args.format,
                country=args.country,
                start_date=args.start_date,
                end_date=args.end_date
            )
        elif args.type == 'all':
            filepath = exporter.export_all(
                format='excel',
                start_date=args.start_date,
                end_date=args.end_date
            )
        
        print(f"\n✅ Export successful!")
        print(f"📁 File: {filepath}")
        
    except Exception as e:
        print(f"\n❌ Export failed: {str(e)}")
        exit(1)
