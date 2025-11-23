#!/usr/bin/env python3
"""
Command-line interface for COVID-19 Economic Impact Analysis
Provides easy access to common tasks and operations
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


def run_dashboard():
    """Start the dashboard application"""
    print("🚀 Starting dashboard...")
    from src.app import app
    app.run_server(debug=True, host='0.0.0.0', port=8050)


def run_api():
    """Start the API server"""
    print("🚀 Starting API server...")
    from src.api import app
    app.run(host='0.0.0.0', port=5000, debug=True)


def run_pipeline():
    """Run the data pipeline"""
    print("🔄 Running data pipeline...")
    from src.main import main
    main()
    print("✅ Pipeline completed!")


def export_data(args):
    """Export data"""
    print(f"📤 Exporting {args.type} data in {args.format} format...")
    from src.export import DataExporter
    
    exporter = DataExporter(output_dir=args.output)
    
    try:
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
        
        print(f"✅ Export successful: {filepath}")
        
    except Exception as e:
        print(f"❌ Export failed: {str(e)}")
        sys.exit(1)


def show_config():
    """Display current configuration"""
    print("📋 Current Configuration\n")
    from src.config import print_config
    print_config()


def show_stats():
    """Show database statistics"""
    print("📊 Database Statistics\n")
    from src.database import DatabaseManager
    
    db = DatabaseManager()
    
    try:
        covid_data = db.get_covid_data()
        economic_data = db.get_economic_data()
        merged_data = db.get_merged_data()
        
        print(f"COVID-19 Records: {len(covid_data):,}")
        print(f"Economic Records: {len(economic_data):,}")
        print(f"Merged Records: {len(merged_data):,}")
        
        if not covid_data.empty:
            print(f"\nCOVID-19 Date Range:")
            print(f"  From: {covid_data['date'].min()}")
            print(f"  To: {covid_data['date'].max()}")
        
        if not economic_data.empty:
            print(f"\nEconomic Date Range:")
            print(f"  From: {economic_data['date'].min()}")
            print(f"  To: {economic_data['date'].max()}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


def run_tests(args):
    """Run tests"""
    import subprocess
    
    print("🧪 Running tests...\n")
    
    cmd = ['pytest', 'tests/', '-v']
    
    if args.coverage:
        cmd.extend(['--cov=src', '--cov-report=html', '--cov-report=term'])
    
    if args.file:
        cmd = ['pytest', args.file, '-v']
    
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


def clear_cache():
    """Clear application cache"""
    print("🗑️  Clearing cache...")
    from src.cache import clear_cache as do_clear
    do_clear()
    print("✅ Cache cleared!")


def setup_project():
    """Initial project setup"""
    print("🔧 Setting up project...\n")
    
    # Create directories
    directories = ['data', 'logs', 'exports', 'cache']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Create .env file if it doesn't exist
    if not Path('.env').exists():
        import shutil
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from .env.example")
    
    # Initialize database
    print("\n📦 Initializing database...")
    from src.database import DatabaseManager
    db = DatabaseManager()
    db.create_tables()
    print("✅ Database initialized!")
    
    print("\n✨ Setup complete! You can now:")
    print("  - Run the dashboard: python cli.py dashboard")
    print("  - Run the API: python cli.py api")
    print("  - Run the pipeline: python cli.py pipeline")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='COVID-19 Economic Impact Analysis CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py setup              # Initial project setup
  python cli.py dashboard          # Start dashboard
  python cli.py api                # Start API server
  python cli.py pipeline           # Run data pipeline
  python cli.py export --type merged --format csv
  python cli.py stats              # Show database statistics
  python cli.py test               # Run all tests
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Setup command
    subparsers.add_parser('setup', help='Initial project setup')
    
    # Dashboard command
    subparsers.add_parser('dashboard', help='Start the dashboard application')
    
    # API command
    subparsers.add_parser('api', help='Start the API server')
    
    # Pipeline command
    subparsers.add_parser('pipeline', help='Run the data pipeline')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export data')
    export_parser.add_argument('--type', choices=['covid', 'economic', 'merged', 'all'],
                               default='merged', help='Data type to export')
    export_parser.add_argument('--format', choices=['json', 'csv', 'excel'],
                               default='csv', help='Export format')
    export_parser.add_argument('--country', help='Filter by country')
    export_parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    export_parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    export_parser.add_argument('--output', default='exports', help='Output directory')
    
    # Config command
    subparsers.add_parser('config', help='Show current configuration')
    
    # Stats command
    subparsers.add_parser('stats', help='Show database statistics')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run tests')
    test_parser.add_argument('--coverage', action='store_true', help='Run with coverage')
    test_parser.add_argument('--file', help='Run specific test file')
    
    # Cache command
    subparsers.add_parser('clear-cache', help='Clear application cache')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    try:
        if args.command == 'setup':
            setup_project()
        elif args.command == 'dashboard':
            run_dashboard()
        elif args.command == 'api':
            run_api()
        elif args.command == 'pipeline':
            run_pipeline()
        elif args.command == 'export':
            export_data(args)
        elif args.command == 'config':
            show_config()
        elif args.command == 'stats':
            show_stats()
        elif args.command == 'test':
            run_tests(args)
        elif args.command == 'clear-cache':
            clear_cache()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
