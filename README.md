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

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/covid_economic_analysis.git
cd covid_economic_analysis
```

2. Create and activate a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the dashboard application:
```bash
python src/app.py
```

The dashboard will be available at `http://localhost:8050`

5. (Optional) Run the REST API:
```bash
python src/api.py
```

The API will be available at `http://localhost:5000`

## Features

- Interactive data visualization dashboard
- Economic impact analysis
- COVID-19 case tracking
- Statistical analysis tools
- **RESTful API for programmatic data access**
- Correlation analysis between COVID-19 and economic indicators
- Trend analysis with rolling averages

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

## License

MIT License
