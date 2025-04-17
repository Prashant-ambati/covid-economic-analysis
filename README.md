# COVID-19 Economic Impact Analysis Dashboard

This dashboard provides an interactive analysis of COVID-19's impact on economic indicators in the United States. It visualizes the relationship between COVID-19 cases and various economic metrics, offering insights into the pandemic's economic effects.

## Features

- Interactive COVID-19 case analysis with daily trends
- Regional distribution map of COVID-19 cases
- Economic indicators visualization
- Correlation analysis between COVID-19 and economic metrics
- Economic forecast predictions
- Key insights and findings

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd covid_economic_analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the application:
```bash
python src/app.py
```

2. Open your web browser and navigate to:
```
http://localhost:8050
```

## Deployment

This application is configured for deployment on Render. The `Procfile` and `requirements.txt` are already set up for this purpose.

## Data Sources

- COVID-19 data: [Our World in Data](https://ourworldindata.org/coronavirus)
- Economic indicators: [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
