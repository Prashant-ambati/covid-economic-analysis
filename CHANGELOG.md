# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-22

### Added
- **RESTful API** for programmatic access to COVID-19 and economic data
  - `/api/v1/health` - Health check endpoint
  - `/api/v1/covid` - COVID-19 data with filtering options
  - `/api/v1/economic` - Economic indicators data
  - `/api/v1/merged` - Combined COVID-19 and economic data
  - `/api/v1/statistics` - Statistical summary endpoint
  - `/api/v1/correlations` - Correlation analysis endpoint
  - `/api/v1/trends` - Trend analysis with rolling averages
- Comprehensive API documentation in `API_DOCUMENTATION.md`
- API unit tests in `tests/test_api.py`
- Example usage script in `examples/api_usage_example.py`
- Flask and Flask-CORS dependencies
- CORS support for cross-origin requests
- Error handling decorator for consistent error responses
- Query parameter support for filtering data by date range, country, and limit

### Changed
- Updated `README.md` with API information and usage examples
- Enhanced project features list to include API capabilities

### Technical Details
- API built with Flask 3.0.0
- Supports JSON response format
- Implements RESTful design principles
- Includes comprehensive error handling
- CORS enabled for frontend integration

## [1.0.0] - 2025-04-17

### Added
- Initial release
- COVID-19 data ingestion and processing
- Economic indicators analysis
- Interactive Dash dashboard
- SQLite database for data storage
- Data visualization with Plotly
- Correlation analysis between COVID-19 and economic indicators
- Statistical analysis tools
- Automated data pipeline
