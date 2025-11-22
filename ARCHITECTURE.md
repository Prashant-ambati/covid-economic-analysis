# Project Architecture

## Overview

The COVID-19 Economic Impact Analysis project consists of three main components:
1. **Data Pipeline** - Ingestion, processing, and storage
2. **Dashboard** - Interactive web visualization
3. **REST API** - Programmatic data access (NEW)

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Sources                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ COVID-19 API │  │ Economic API │  │  CSV Files   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Ingestion Layer                       │
│                  (data_ingestion.py)                         │
│  • Fetch COVID-19 data                                       │
│  • Fetch economic indicators                                 │
│  • Handle API requests                                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Data Processing Layer                       │
│                 (data_processing.py)                         │
│  • Clean and validate data                                   │
│  • Calculate metrics (7-day avg, CFR, etc.)                  │
│  • Merge datasets                                            │
│  • Correlation analysis                                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer                            │
│                    (database.py)                             │
│  • SQLite database                                           │
│  • Tables: covid_data, economic_data, merged_data           │
│  • CRUD operations                                           │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│    Dashboard Layer       │  │      API Layer (NEW)     │
│       (app.py)           │  │       (api.py)           │
│                          │  │                          │
│  • Dash web app          │  │  • Flask REST API        │
│  • Interactive charts    │  │  • 8 endpoints           │
│  • Real-time updates     │  │  • JSON responses        │
│  • Dark theme UI         │  │  • CORS enabled          │
│  • Port: 8050            │  │  • Port: 5000            │
└──────────────────────────┘  └──────────────────────────┘
                │                       │
                ▼                       ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│    Web Browser           │  │  API Clients             │
│  • Interactive UI        │  │  • Python scripts        │
│  • Visualizations        │  │  • JavaScript apps       │
│  • Filters & controls    │  │  • Mobile apps           │
└──────────────────────────┘  └──────────────────────────┘
```

## Component Details

### 1. Data Pipeline

**Files:**
- `src/data_ingestion.py` - Fetches data from external sources
- `src/data_processing.py` - Cleans and processes data
- `src/database.py` - Manages database operations
- `src/main.py` - Orchestrates the pipeline

**Flow:**
```
Fetch → Clean → Process → Store → Analyze
```

### 2. Dashboard (Existing)

**File:** `src/app.py`

**Features:**
- Interactive Plotly charts
- Real-time data filtering
- Dark theme UI
- Responsive design
- Multiple visualization types

**Tech Stack:**
- Dash
- Plotly
- Dash Bootstrap Components

### 3. REST API (NEW)

**File:** `src/api.py`

**Endpoints:**
```
GET  /                      → API info
GET  /api/v1/health         → Health check
GET  /api/v1/covid          → COVID-19 data
GET  /api/v1/economic       → Economic data
GET  /api/v1/merged         → Combined data
GET  /api/v1/statistics     → Statistics
GET  /api/v1/correlations   → Correlations
GET  /api/v1/trends         → Trend analysis
```

**Tech Stack:**
- Flask
- Flask-CORS
- SQLite

## Data Flow

### Pipeline Execution
```
1. main.py starts
2. DataIngestion fetches raw data
3. DataProcessor cleans data
4. DatabaseManager stores data
5. DataVisualizer creates charts
```

### Dashboard Request
```
1. User opens browser → localhost:8050
2. Dash app loads
3. User selects filters
4. Callback triggered
5. Database queried
6. Charts updated
7. Response rendered
```

### API Request
```
1. Client sends HTTP request → localhost:5000/api/v1/covid
2. Flask routes request
3. Query parameters parsed
4. Database queried
5. Data formatted as JSON
6. Response sent to client
```

## Database Schema

### covid_data
```sql
CREATE TABLE covid_data (
    id INTEGER PRIMARY KEY,
    date DATE,
    country TEXT,
    cases INTEGER,
    deaths INTEGER,
    recovered INTEGER,
    new_cases INTEGER,
    new_deaths INTEGER,
    cases_7day_avg REAL,
    deaths_7day_avg REAL,
    case_fatality_rate REAL,
    created_at TIMESTAMP
)
```

### economic_data
```sql
CREATE TABLE economic_data (
    id INTEGER PRIMARY KEY,
    date DATE,
    gdp_growth REAL,
    unemployment_rate REAL,
    inflation_rate REAL,
    gdp_growth_change REAL,
    unemployment_change REAL,
    inflation_change REAL,
    created_at TIMESTAMP
)
```

### merged_data
```sql
CREATE TABLE merged_data (
    id INTEGER PRIMARY KEY,
    date DATE,
    country TEXT,
    cases INTEGER,
    deaths INTEGER,
    new_cases INTEGER,
    new_deaths INTEGER,
    cases_7day_avg REAL,
    deaths_7day_avg REAL,
    case_fatality_rate REAL,
    gdp_growth REAL,
    unemployment_rate REAL,
    inflation_rate REAL,
    gdp_growth_change REAL,
    unemployment_change REAL,
    inflation_change REAL,
    created_at TIMESTAMP
)
```

## API Architecture

### Request Flow
```
Client Request
    ↓
Flask Router
    ↓
Error Handler Decorator
    ↓
Endpoint Function
    ↓
Database Manager
    ↓
SQLite Database
    ↓
Data Processing
    ↓
JSON Response
    ↓
Client
```

### Error Handling
```python
@handle_errors
def endpoint():
    try:
        # Process request
        return success_response
    except Exception as e:
        # Logged and handled
        return error_response
```

## Testing Architecture

### Test Structure
```
tests/
├── test_api.py              # API endpoint tests
└── test_data_processing.py  # Data processing tests
```

### CI/CD Pipeline
```
GitHub Push/PR
    ↓
GitHub Actions Triggered
    ↓
Setup Python Environment
    ↓
Install Dependencies
    ↓
Run Tests
    ↓
Test API Startup
    ↓
Report Results
```

## Deployment Options

### Local Development
```bash
# Dashboard
python src/app.py → localhost:8050

# API
python src/api.py → localhost:5000
```

### Production (Heroku/Render)
```bash
# Using Procfile
web: gunicorn src.app:server
api: gunicorn src.api:app
```

### Docker (Future)
```dockerfile
FROM python:3.11
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8050 5000
CMD ["python", "src/app.py"]
```

## Security Considerations

### Current
- CORS enabled for cross-origin requests
- Input validation on query parameters
- Error messages don't expose sensitive info
- SQLite for local development

### Future Enhancements
- API authentication (JWT)
- Rate limiting
- API keys
- HTTPS enforcement
- Input sanitization
- SQL injection prevention (parameterized queries)

## Performance Considerations

### Current
- SQLite for fast local queries
- Efficient pandas operations
- Minimal data processing in endpoints

### Future Optimizations
- Redis caching
- Database indexing
- Query optimization
- Connection pooling
- Async operations
- CDN for static assets

## Scalability

### Current Limitations
- SQLite (single file database)
- Synchronous operations
- No caching layer

### Scaling Path
1. **Database:** SQLite → PostgreSQL
2. **Caching:** Add Redis
3. **API:** Add load balancer
4. **Processing:** Add Celery for async tasks
5. **Storage:** Move to cloud storage (S3)
6. **Deployment:** Containerize with Docker/Kubernetes

## Monitoring & Logging

### Current
- Python logging module
- Console output
- Log files

### Future
- Application monitoring (New Relic, DataDog)
- Error tracking (Sentry)
- API analytics
- Performance metrics
- User analytics

## Technology Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | Dash, Plotly, Bootstrap |
| API | Flask, Flask-CORS |
| Data Processing | Pandas, NumPy |
| Database | SQLite |
| Testing | Pytest |
| CI/CD | GitHub Actions |
| Deployment | Gunicorn, Heroku/Render |
| Documentation | Markdown |

## Development Workflow

```
1. Feature Branch
   ↓
2. Code Implementation
   ↓
3. Write Tests
   ↓
4. Run Tests Locally
   ↓
5. Update Documentation
   ↓
6. Commit & Push
   ↓
7. CI/CD Tests Run
   ↓
8. Create Pull Request
   ↓
9. Code Review
   ↓
10. Merge to Main
```

## Conclusion

The architecture is designed to be:
- **Modular** - Separate concerns
- **Testable** - Comprehensive tests
- **Scalable** - Clear upgrade path
- **Maintainable** - Clean code structure
- **Documented** - Extensive documentation
- **Extensible** - Easy to add features

This architecture supports both interactive visualization and programmatic access, making it suitable for various use cases and deployment scenarios.
