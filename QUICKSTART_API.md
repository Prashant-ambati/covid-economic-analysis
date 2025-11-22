# API Quick Start Guide

Get started with the COVID-19 Economic Impact API in 5 minutes!

## Prerequisites

- Python 3.11+
- pip package manager
- Virtual environment (recommended)

## Installation

1. **Clone the repository** (if you haven't already):
```bash
git clone https://github.com/yourusername/covid_economic_analysis.git
cd covid_economic_analysis
```

2. **Create and activate virtual environment**:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Starting the API

Run the API server:
```bash
python src/api.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

The API is now running! 🚀

## Your First API Call

Open a new terminal and try:

```bash
curl http://localhost:5000/api/v1/health
```

You should get:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-22T10:30:00",
  "database": "connected"
}
```

## Quick Examples

### 1. Get Statistics
```bash
curl http://localhost:5000/api/v1/statistics
```

### 2. Get COVID-19 Data (Last 10 Records)
```bash
curl "http://localhost:5000/api/v1/covid?limit=10"
```

### 3. Get Correlation Analysis
```bash
curl http://localhost:5000/api/v1/correlations
```

### 4. Get Economic Data for Date Range
```bash
curl "http://localhost:5000/api/v1/economic?start_date=2020-01-01&end_date=2021-12-31"
```

## Using Python

```python
import requests

# Get statistics
response = requests.get('http://localhost:5000/api/v1/statistics')
data = response.json()
print(data['statistics'])

# Get COVID-19 data
response = requests.get('http://localhost:5000/api/v1/covid', params={'limit': 10})
covid_data = response.json()
print(f"Found {covid_data['count']} records")
```

## Using JavaScript

```javascript
// Fetch statistics
fetch('http://localhost:5000/api/v1/statistics')
  .then(response => response.json())
  .then(data => console.log(data.statistics));

// Fetch COVID-19 data
fetch('http://localhost:5000/api/v1/covid?limit=10')
  .then(response => response.json())
  .then(data => console.log(`Found ${data.count} records`));
```

## Run Example Script

We've included a comprehensive example script:

```bash
python examples/api_usage_example.py
```

This will demonstrate all API endpoints with formatted output.

## Run Tests

Verify everything works:

```bash
pytest tests/test_api.py -v
```

## Available Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API information |
| `GET /api/v1/health` | Health check |
| `GET /api/v1/covid` | COVID-19 data |
| `GET /api/v1/economic` | Economic data |
| `GET /api/v1/merged` | Combined data |
| `GET /api/v1/statistics` | Statistical summary |
| `GET /api/v1/correlations` | Correlation analysis |
| `GET /api/v1/trends` | Trend analysis |

## Query Parameters

Most endpoints support these parameters:

- `start_date` - Filter by start date (YYYY-MM-DD)
- `end_date` - Filter by end date (YYYY-MM-DD)
- `country` - Filter by country name
- `limit` - Limit number of results

Example:
```bash
curl "http://localhost:5000/api/v1/covid?country=USA&start_date=2020-01-01&limit=100"
```

## Next Steps

- Read the full [API Documentation](API_DOCUMENTATION.md)
- Explore the [example script](examples/api_usage_example.py)
- Check out the [dashboard](src/app.py) for visualization

## Troubleshooting

**Connection refused?**
- Make sure the API is running: `python src/api.py`
- Check the port is not in use: `lsof -i :5000`

**No data returned?**
- Ensure the database exists: `ls data/covid_economic.db`
- Run the data pipeline: `python src/main.py`

**Import errors?**
- Verify all dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.11+)

## Support

For issues or questions:
- Check the [API Documentation](API_DOCUMENTATION.md)
- Open an issue on GitHub
- Review the example code in `examples/`

Happy coding! 🎉
