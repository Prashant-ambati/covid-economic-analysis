"""
Configuration management for COVID-19 Economic Impact Analysis
Centralizes all configuration settings for the application
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DATABASE_CONFIG = {
    'name': os.getenv('DB_NAME', 'covid_economic.db'),
    'path': BASE_DIR / 'data' / os.getenv('DB_NAME', 'covid_economic.db'),
    'timeout': int(os.getenv('DB_TIMEOUT', 30)),
    'check_same_thread': False
}

# API configuration
API_CONFIG = {
    'host': os.getenv('API_HOST', '0.0.0.0'),
    'port': int(os.getenv('API_PORT', 5000)),
    'debug': os.getenv('API_DEBUG', 'False').lower() == 'true',
    'version': 'v1',
    'title': 'COVID-19 Economic Impact API',
    'description': 'RESTful API for COVID-19 and economic data analysis'
}

# Dashboard configuration
DASHBOARD_CONFIG = {
    'host': os.getenv('DASHBOARD_HOST', '0.0.0.0'),
    'port': int(os.getenv('DASHBOARD_PORT', 8050)),
    'debug': os.getenv('DASHBOARD_DEBUG', 'True').lower() == 'true',
    'title': 'COVID-19 Economic Impact Dashboard'
}

# Data sources configuration
DATA_SOURCES = {
    'covid_api': os.getenv('COVID_API_URL', 'https://disease.sh/v3/covid-19'),
    'economic_api': os.getenv('ECONOMIC_API_URL', ''),
    'update_interval': int(os.getenv('DATA_UPDATE_INTERVAL', 3600))  # seconds
}

# Logging configuration
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': BASE_DIR / 'logs' / 'app.log',
    'max_bytes': int(os.getenv('LOG_MAX_BYTES', 10485760)),  # 10MB
    'backup_count': int(os.getenv('LOG_BACKUP_COUNT', 5))
}

# Cache configuration
CACHE_CONFIG = {
    'enabled': os.getenv('CACHE_ENABLED', 'True').lower() == 'true',
    'ttl': int(os.getenv('CACHE_TTL', 300)),  # seconds
    'max_size': int(os.getenv('CACHE_MAX_SIZE', 100))
}

# Rate limiting configuration
RATE_LIMIT_CONFIG = {
    'enabled': os.getenv('RATE_LIMIT_ENABLED', 'False').lower() == 'true',
    'requests_per_minute': int(os.getenv('RATE_LIMIT_RPM', 60)),
    'requests_per_hour': int(os.getenv('RATE_LIMIT_RPH', 1000))
}

# CORS configuration
CORS_CONFIG = {
    'origins': os.getenv('CORS_ORIGINS', '*').split(','),
    'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    'allow_headers': ['Content-Type', 'Authorization']
}

# Data processing configuration
PROCESSING_CONFIG = {
    'rolling_window': int(os.getenv('ROLLING_WINDOW', 7)),
    'min_data_points': int(os.getenv('MIN_DATA_POINTS', 10)),
    'outlier_threshold': float(os.getenv('OUTLIER_THRESHOLD', 3.0))
}

# Export configuration
EXPORT_CONFIG = {
    'formats': ['json', 'csv', 'excel'],
    'max_records': int(os.getenv('EXPORT_MAX_RECORDS', 10000)),
    'output_dir': BASE_DIR / 'exports'
}

# Visualization configuration
VIZ_CONFIG = {
    'theme': os.getenv('VIZ_THEME', 'plotly_dark'),
    'color_scheme': {
        'primary': '#3498db',
        'secondary': '#2ecc71',
        'danger': '#e74c3c',
        'warning': '#f1c40f',
        'info': '#9b59b6'
    },
    'chart_height': int(os.getenv('CHART_HEIGHT', 400)),
    'chart_width': int(os.getenv('CHART_WIDTH', 800))
}

# Security configuration
SECURITY_CONFIG = {
    'api_key_required': os.getenv('API_KEY_REQUIRED', 'False').lower() == 'true',
    'api_key_header': os.getenv('API_KEY_HEADER', 'X-API-Key'),
    'allowed_ips': os.getenv('ALLOWED_IPS', '').split(',') if os.getenv('ALLOWED_IPS') else []
}

# Feature flags
FEATURE_FLAGS = {
    'enable_caching': os.getenv('FEATURE_CACHING', 'True').lower() == 'true',
    'enable_rate_limiting': os.getenv('FEATURE_RATE_LIMIT', 'False').lower() == 'true',
    'enable_analytics': os.getenv('FEATURE_ANALYTICS', 'False').lower() == 'true',
    'enable_export': os.getenv('FEATURE_EXPORT', 'True').lower() == 'true',
    'enable_notifications': os.getenv('FEATURE_NOTIFICATIONS', 'False').lower() == 'true'
}

# Create necessary directories
def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        BASE_DIR / 'data',
        BASE_DIR / 'logs',
        BASE_DIR / 'exports',
        BASE_DIR / 'cache'
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Initialize directories on import
create_directories()


def get_config(section=None):
    """
    Get configuration for a specific section or all configurations
    
    Args:
        section (str, optional): Configuration section name
        
    Returns:
        dict: Configuration dictionary
    """
    configs = {
        'database': DATABASE_CONFIG,
        'api': API_CONFIG,
        'dashboard': DASHBOARD_CONFIG,
        'data_sources': DATA_SOURCES,
        'logging': LOGGING_CONFIG,
        'cache': CACHE_CONFIG,
        'rate_limit': RATE_LIMIT_CONFIG,
        'cors': CORS_CONFIG,
        'processing': PROCESSING_CONFIG,
        'export': EXPORT_CONFIG,
        'visualization': VIZ_CONFIG,
        'security': SECURITY_CONFIG,
        'features': FEATURE_FLAGS
    }
    
    if section:
        return configs.get(section, {})
    return configs


def print_config():
    """Print current configuration (for debugging)"""
    print("=" * 60)
    print("Current Configuration")
    print("=" * 60)
    
    configs = get_config()
    for section, config in configs.items():
        print(f"\n{section.upper()}:")
        for key, value in config.items():
            # Hide sensitive values
            if 'key' in key.lower() or 'secret' in key.lower():
                value = '***HIDDEN***'
            print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    print_config()
