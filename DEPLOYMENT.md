# Deployment Guide

Complete guide for deploying the COVID-19 Economic Impact Analysis application.

## Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Environment Variables](#environment-variables)
- [Production Checklist](#production-checklist)

## Local Development

### Prerequisites

- Python 3.11+
- pip
- Virtual environment (recommended)

### Setup

```bash
# Clone repository
git clone https://github.com/Prashant-ambati/covid-economic-analysis.git
cd covid-economic-analysis

# Setup project
python cli.py setup

# Or manual setup:
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### Running Services

```bash
# Using CLI tool
python cli.py dashboard  # Dashboard on port 8050
python cli.py api        # API on port 5000
python cli.py pipeline   # Run data pipeline

# Or directly
python src/app.py        # Dashboard
python src/api.py        # API
python src/main.py       # Pipeline
```

## Docker Deployment

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

### Quick Start

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Services

```bash
# Build image
docker build -t covid-analysis .

# Run dashboard only
docker run -p 8050:8050 -v $(pwd)/data:/app/data covid-analysis python src/app.py

# Run API only
docker run -p 5000:5000 -v $(pwd)/data:/app/data covid-analysis python src/api.py
```

### Docker Commands

```bash
# View running containers
docker-compose ps

# Restart services
docker-compose restart

# View logs for specific service
docker-compose logs -f api

# Execute command in container
docker-compose exec api python cli.py stats

# Rebuild after code changes
docker-compose up -d --build
```

## Cloud Deployment

### Heroku

1. **Install Heroku CLI**
```bash
brew install heroku/brew/heroku  # macOS
# or download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login and Create App**
```bash
heroku login
heroku create covid-economic-analysis
```

3. **Configure Environment**
```bash
heroku config:set API_DEBUG=False
heroku config:set LOG_LEVEL=INFO
heroku config:set CACHE_ENABLED=True
```

4. **Deploy**
```bash
git push heroku master
```

5. **Scale Services**
```bash
heroku ps:scale web=1
```

### Render

1. **Create render.yaml** (already included)

2. **Connect Repository**
   - Go to https://render.com
   - Connect your GitHub repository
   - Render will auto-detect render.yaml

3. **Configure Environment Variables**
   - Set in Render dashboard
   - Use .env.example as reference

4. **Deploy**
   - Automatic on git push
   - Manual trigger in dashboard

### AWS (EC2)

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.medium or larger
   - Open ports: 22, 80, 443, 8050, 5000

2. **Connect and Setup**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Clone repository
git clone https://github.com/Prashant-ambati/covid-economic-analysis.git
cd covid-economic-analysis

# Setup
python3.11 cli.py setup
```

3. **Install and Configure Nginx**
```bash
sudo apt install nginx -y

# Create nginx config
sudo nano /etc/nginx/sites-available/covid-analysis
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/covid-analysis /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

4. **Setup Systemd Services**

Dashboard service:
```bash
sudo nano /etc/systemd/system/covid-dashboard.service
```

```ini
[Unit]
Description=COVID-19 Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/covid-economic-analysis
Environment="PATH=/home/ubuntu/covid-economic-analysis/venv/bin"
ExecStart=/home/ubuntu/covid-economic-analysis/venv/bin/python src/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

API service:
```bash
sudo nano /etc/systemd/system/covid-api.service
```

```ini
[Unit]
Description=COVID-19 API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/covid-economic-analysis
Environment="PATH=/home/ubuntu/covid-economic-analysis/venv/bin"
ExecStart=/home/ubuntu/covid-economic-analysis/venv/bin/python src/api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start services
sudo systemctl enable covid-dashboard covid-api
sudo systemctl start covid-dashboard covid-api
sudo systemctl status covid-dashboard covid-api
```

### DigitalOcean

Similar to AWS EC2 setup. Use their App Platform for easier deployment:

1. Connect GitHub repository
2. Configure build and run commands
3. Set environment variables
4. Deploy

## Environment Variables

### Required

```bash
# Database
DB_NAME=covid_economic.db

# API
API_HOST=0.0.0.0
API_PORT=5000

# Dashboard
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=8050
```

### Optional

```bash
# Logging
LOG_LEVEL=INFO

# Cache
CACHE_ENABLED=True
CACHE_TTL=300

# Features
FEATURE_CACHING=True
FEATURE_EXPORT=True
```

### Production Settings

```bash
API_DEBUG=False
DASHBOARD_DEBUG=False
LOG_LEVEL=WARNING
CACHE_ENABLED=True
RATE_LIMIT_ENABLED=True
```

## Production Checklist

### Security

- [ ] Set `DEBUG=False` in production
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Enable rate limiting
- [ ] Set up API authentication (if needed)
- [ ] Regular security updates

### Performance

- [ ] Enable caching
- [ ] Configure database connection pooling
- [ ] Set up CDN for static assets
- [ ] Optimize database queries
- [ ] Monitor memory usage
- [ ] Set up load balancing (if needed)

### Monitoring

- [ ] Set up application logging
- [ ] Configure error tracking (Sentry)
- [ ] Monitor uptime
- [ ] Track API usage
- [ ] Set up alerts
- [ ] Database backups

### Maintenance

- [ ] Automated backups
- [ ] Update schedule
- [ ] Rollback plan
- [ ] Documentation
- [ ] Health checks
- [ ] Monitoring dashboard

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8050
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Database Locked

```bash
# Check for other processes
ps aux | grep python

# Remove lock file
rm data/covid_economic.db-journal
```

### Docker Issues

```bash
# Clean up
docker-compose down -v
docker system prune -a

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Memory Issues

```bash
# Check memory usage
free -h

# Increase swap (Linux)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Scaling

### Horizontal Scaling

Use load balancer with multiple instances:

```yaml
# docker-compose.yml
services:
  api:
    deploy:
      replicas: 3
```

### Vertical Scaling

Increase resources:
- More CPU cores
- More RAM
- Faster storage

### Database Scaling

Migrate from SQLite to PostgreSQL:

```python
# Update database.py
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/dbname')
```

## Backup and Recovery

### Automated Backups

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backups/backup_$DATE.tar.gz data/ logs/
find backups/ -mtime +7 -delete
EOF

chmod +x backup.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

### Recovery

```bash
# Restore from backup
tar -xzf backups/backup_YYYYMMDD_HHMMSS.tar.gz
```

## Support

For deployment issues:
- Check logs: `docker-compose logs` or `tail -f logs/app.log`
- Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Open GitHub issue
- Check documentation

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)
- [AWS EC2 Guide](https://docs.aws.amazon.com/ec2/)
- [Nginx Documentation](https://nginx.org/en/docs/)
