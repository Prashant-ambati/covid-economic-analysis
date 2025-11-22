# COVID-19 Economic Impact API Documentation

## Overview

The COVID-19 Economic Impact API provides programmatic access to COVID-19 case data and economic indicators, allowing developers to integrate this data into their applications.

**Base URL:** `http://localhost:5000/api/v1`

**Version:** 1.0

## Authentication

Currently, the API is open and does not require authentication. Rate limiting may be implemented in future versions.

## Response Format

All responses are returned in JSON format with the following structure:

```json
{
  "status": "success",
  "data": [...],
  "count": 100
}
```

Error responses:

```json
{
  "status": "error",
  "error": "Error message description"
}
```

## Endpoints

### 1. Root Endpoint

**GET** `/`

Returns API information and available endpoints.

**Response:**
```json
{
  "name": "COVID-19 Economic Impact API",
  "version": "v1",
  "status": "active",
  "endpoints": {...}
}
```

---

### 2. Health Check

**GET** `/api/v1/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-22T10:30:00",
  "database": "connected"
}
```

---

### 3. COVID-19 Data

**GET** `/api/v1/covid`

Retrieve COVID-19 case data with optional filters.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| country | string | No | Filter by country name |
| start_date | string | No | Start date (YYYY-MM-DD) |
| end_date | string | No | End date (YYYY-MM-DD) |
| limit | integer | No | Maximum records to return |

**Example Request:**
```bash
curl "http://localhost:5000/api/v1/covid?country=USA&start_date=2020-01-01&limit=100"
```

**Example Response:**
```json
{
  "status": "success",
  "count": 100,
  "data": [
    {
      "id": 1,
      "date": "2020-01-01",
      "country": "USA",
      "cases": 1000,
      "deaths": 50,
      "recovered": 800,
      "new_cases": 100,
      "new_deaths": 5,
      "cases_7day_avg": 95.5,
      "deaths_7day_avg": 4.8,
      "case_fatality_rate": 5.0
    }
  ]
}
```

---

### 4. Economic Data

**GET** `/api/v1/economic`

Retrieve economic indicator data.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start_date | string | No | Start date (YYYY-MM-DD) |
| end_date | string | No | End date (YYYY-MM-DD) |
| limit | integer | No | Maximum records to return |

**Example Request:**
```bash
curl "http://localhost:5000/api/v1/economic?start_date=2020-01-01&end_date=2021-12-31"
```

**Example Response:**
```json
{
  "status": "success",
  "count": 24,
  "data": [
    {
      "id": 1,
      "date": "2020-01-01",
      "gdp_growth": 2.3,
      "unemployment_rate": 3.5,
      "inflation_rate": 1.8,
      "gdp_growth_change": 0.5,
      "unemployment_change": -0.2,
      "inflation_change": 0.1
    }
  ]
}
```

---

### 5. Merged Data

**GET** `/api/v1/merged`

Retrieve merged COVID-19 and economic data.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| country | string | No | Filter by country name |
| start_date | string | No | Start date (YYYY-MM-DD) |
| end_date | string | No | End date (YYYY-MM-DD) |
| limit | integer | No | Maximum records to return |

**Example Request:**
```bash
curl "http://localhost:5000/api/v1/merged?country=USA&start_date=2020-01-01"
```

**Example Response:**
```json
{
  "status": "success",
  "count": 50,
  "data": [
    {
      "date": "2020-01-01",
      "country": "USA",
      "cases": 1000,
      "deaths": 50,
      "new_cases": 100,
      "new_deaths": 5,
      "gdp_growth": 2.3,
      "unemployment_rate": 3.5,
      "inflation_rate": 1.8
    }
  ]
}
```

---

### 6. Statistics

**GET** `/api/v1/statistics`

Get statistical summary of COVID-19 and economic data.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start_date | string | No | Start date (YYYY-MM-DD) |
| end_date | string | No | End date (YYYY-MM-DD) |

**Example Request:**
```bash
curl "http://localhost:5000/api/v1/statistics?start_date=2020-01-01&end_date=2021-12-31"
```

**Example Response:**
```json
{
  "status": "success",
  "statistics": {
    "covid": {
      "total_cases": 50000000,
      "total_deaths": 800000,
      "avg_new_cases": 50000,
      "avg_new_deaths": 800,
      "case_fatality_rate": 1.6
    },
    "economic": {
      "avg_gdp_growth": 2.1,
      "avg_unemployment": 5.5,
      "avg_inflation": 2.3,
      "gdp_volatility": 1.2
    },
    "period": {
      "start_date": "2020-01-01",
      "end_date": "2021-12-31",
      "data_points": 730
    }
  }
}
```

---

### 7. Correlations

**GET** `/api/v1/correlations`

Get correlation analysis between COVID-19 and economic indicators.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start_date | string | No | Start date (YYYY-MM-DD) |
| end_date | string | No | End date (YYYY-MM-DD) |

**Example Request:**
```bash
curl "http://localhost:5000/api/v1/correlations"
```

**Example Response:**
```json
{
  "status": "success",
  "correlations": {
    "cases_vs_gdp": -0.65,
    "cases_vs_unemployment": 0.72,
    "cases_vs_inflation": 0.15,
    "deaths_vs_gdp": -0.58,
    "deaths_vs_unemployment": 0.68,
    "deaths_vs_inflation": 0.12
  },
  "interpretation": {
    "strong": "Correlation > 0.7 or < -0.7",
    "moderate": "Correlation between 0.3-0.7 or -0.3 to -0.7",
    "weak": "Correlation between -0.3 and 0.3"
  }
}
```

---

### 8. Trends

**GET** `/api/v1/trends`

Get trend analysis with rolling averages.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| window | integer | No | Rolling window size (default: 7) |
| start_date | string | No | Start date (YYYY-MM-DD) |
| end_date | string | No | End date (YYYY-MM-DD) |

**Example Request:**
```bash
curl "http://localhost:5000/api/v1/trends?window=14&start_date=2020-01-01"
```

**Example Response:**
```json
{
  "status": "success",
  "trends": {
    "cases_trend": [100, 105, 110, 115, ...],
    "deaths_trend": [5, 5.2, 5.5, 5.8, ...],
    "dates": ["2020-01-01", "2020-01-02", ...],
    "window_size": 14
  }
}
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - No data available |
| 500 | Internal Server Error |

## Rate Limiting

Currently not implemented. Future versions may include rate limiting.

## Usage Examples

### Python

```python
import requests

# Get COVID-19 data
response = requests.get('http://localhost:5000/api/v1/covid', params={
    'country': 'USA',
    'start_date': '2020-01-01',
    'limit': 100
})
data = response.json()
print(data)

# Get statistics
response = requests.get('http://localhost:5000/api/v1/statistics')
stats = response.json()
print(stats['statistics'])
```

### JavaScript

```javascript
// Get COVID-19 data
fetch('http://localhost:5000/api/v1/covid?country=USA&limit=100')
  .then(response => response.json())
  .then(data => console.log(data));

// Get correlations
fetch('http://localhost:5000/api/v1/correlations')
  .then(response => response.json())
  .then(data => console.log(data.correlations));
```

### cURL

```bash
# Get economic data
curl "http://localhost:5000/api/v1/economic?start_date=2020-01-01&end_date=2021-12-31"

# Get merged data
curl "http://localhost:5000/api/v1/merged?country=USA&limit=50"

# Get statistics
curl "http://localhost:5000/api/v1/statistics"
```

## Running the API

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the API server:
```bash
python src/api.py
```

3. The API will be available at `http://localhost:5000`

## Support

For issues or questions, please open an issue on the GitHub repository.
