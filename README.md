# COVID-19 and Economic Indicators Analysis

A data engineering and analytics project that demonstrates the correlation between COVID-19 cases and key economic indicators.

## Project Overview

This project implements a complete data pipeline that:
1. Fetches COVID-19 case data from a public API
2. Retrieves economic indicators (GDP, unemployment rates, etc.)
3. Processes and transforms the data
4. Stores it in a SQLite database
5. Creates interactive visualizations
6. Performs statistical analysis

## Features

- **Data Pipeline**: Automated ETL process with error handling and logging
- **Data Processing**: Data cleaning, transformation, and aggregation
- **Database**: SQLite implementation with proper schema design
- **Visualization**: Interactive dashboards using Plotly
- **Analysis**: Statistical correlation analysis between COVID-19 and economic indicators
- **Testing**: Unit tests for data processing functions
- **Documentation**: Comprehensive documentation and code comments

## Technical Stack

- Python 3.8+
- Pandas for data manipulation
- SQLite for data storage
- Plotly for visualization
- Requests for API calls
- Pytest for testing
- Logging for pipeline monitoring

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the data pipeline:
   ```bash
   python src/main.py
   ```
2. View the visualizations:
   ```bash
   python src/visualization.py
   ```

## Project Structure

```
covid_economic_analysis/
├── src/                    # Source code
│   ├── data_ingestion.py   # API data fetching
│   ├── data_processing.py  # Data transformation
│   ├── database.py         # Database operations
│   ├── visualization.py    # Data visualization
│   └── main.py            # Pipeline orchestration
├── tests/                  # Unit tests
├── data/                   # Data storage
├── docs/                   # Documentation
└── requirements.txt        # Project dependencies
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License.
