# COVID-19 Economic Impact Analysis

[![API Tests](https://github.com/yourusername/covid_economic_analysis/workflows/API%20Tests/badge.svg)](https://github.com/yourusername/covid_economic_analysis/actions)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project analyzes the economic impact of COVID-19 using data visualization and statistical analysis.

## Project Structure

```
covid_economic_analysis/
├── app.py              # Main Dash application
├── data/               # Data directory
├── requirements.txt    # Python dependencies
├── runtime.txt        # Python version specification
└── README.md          # Project documentation
```

## Quick Start

### Option 1: Using CLI Tool (Recommended)

```bash
# Clone and setup
git clone https://github.com/Prashant-ambati/covid-economic-analysis.git
cd covid-economic-analysis
python cli.py setup

# Run services
python cli.py dashboard  # Dashboard on port 8050
python cli.py api        # API on port 5000
python cli.py pipeline   # Run data pipeline
```

### Option 2: Using Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 3: Manual Setup

```bash
# Clone repository
git clone https://github.com/Prashant-ambati/covid-economic-analysis.git
cd covid-economic-analysis

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Run services
python src/app.py  # Dashboard on port 8050
python src/api.py  # API on port 5000
```

## Features

### Core Functionality
- 📊 Interactive data visualization dashboard
- 📈 Economic impact analysis
- 🦠 COVID-19 case tracking
- 📉 Statistical analysis tools
- 🔗 **RESTful API for programmatic data access**
- 🔄 Correlation analysis between COVID-19 and economic indicators
- 📐 Trend analysis with rolling averages

### New Features
- ⚙️ **Configuration Management** - Centralized config with environment variables
- 💾 **Data Export** - Export to JSON, CSV, Excel formats
- 🚀 **Caching System** - In-memory caching for improved performance
- 🐳 **Docker Support** - Easy deployment with Docker and Docker Compose
- 🛠️ **CLI Tool** - Command-line interface for common tasks
- 📦 **Modular Architecture** - Clean, maintainable code structure

## Technologies Used

- Python 3.11
- Dash & Plotly (Interactive Dashboard)
- Flask (REST API)
- Pandas & NumPy (Data Processing)
- SQLite (Database)
- SciPy & Statsmodels (Statistical Analysis)

📐 **[Architecture Overview](ARCHITECTURE.md)** - System design and component details

## API Documentation

The project now includes a RESTful API for programmatic access to COVID-19 and economic data.

📚 **[Quick Start Guide](QUICKSTART_API.md)** - Get started in 5 minutes!

📖 **[Full API Documentation](API_DOCUMENTATION.md)** - Complete endpoint reference

### Quick API Examples

```bash
# Get COVID-19 statistics
curl "http://localhost:5000/api/v1/statistics"

# Get correlation analysis
curl "http://localhost:5000/api/v1/correlations"

# Get COVID-19 data for a specific country
curl "http://localhost:5000/api/v1/covid?country=USA&limit=100"
```

### Run Example Script

```bash
python examples/api_usage_example.py
```

## CLI Commands

The project includes a powerful CLI tool for easy management:

```bash
python cli.py setup              # Initial project setup
python cli.py dashboard          # Start dashboard
python cli.py api                # Start API server
python cli.py pipeline           # Run data pipeline
python cli.py export --type merged --format csv
python cli.py stats              # Show database statistics
python cli.py config             # Show configuration
python cli.py test               # Run tests
python cli.py clear-cache        # Clear cache
```

## Data Export

Export data in multiple formats:

```bash
# Using CLI
python cli.py export --type covid --format csv
python cli.py export --type economic --format excel
python cli.py export --type merged --format json

# Using API
curl "http://localhost:5000/api/v1/export?type=merged&format=csv" -o data.csv

# Using Python
from src.export import DataExporter
exporter = DataExporter()
exporter.export_covid_data(format='excel')
```

## Docker Deployment

```bash
# Build and run
docker-compose up -d

# View services
docker-compose ps

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Project Structure

```
covid-economic-analysis/
├── src/
│   ├── api.py              # REST API
│   ├── app.py              # Dashboard
│   ├── cache.py            # Caching system
│   ├── config.py           # Configuration
│   ├── database.py         # Database operations
│   ├── data_ingestion.py   # Data fetching
│   ├── data_processing.py  # Data processing
│   ├── export.py           # Data export
│   ├── main.py             # Pipeline orchestration
│   └── visualization.py    # Visualizations
├── tests/                  # Test suite
├── examples/               # Usage examples
├── data/                   # Data storage
├── logs/                   # Application logs
├── exports/                # Exported files
├── cli.py                  # CLI tool
├── Dockerfile              # Docker image
├── docker-compose.yml      # Docker services
└── .env.example            # Environment template
```

## Configuration

Copy `.env.example` to `.env` and customize:

```bash
# API Configuration
API_PORT=5000
API_DEBUG=False

# Dashboard Configuration
DASHBOARD_PORT=8050

# Cache Configuration
CACHE_ENABLED=True
CACHE_TTL=300

# Feature Flags
FEATURE_EXPORT=True
FEATURE_CACHING=True
```

## License

MIT License
