# Deployment Guide

## Prerequisites

- Docker (optional, for containerization)
- Python 3.8+
- PostgreSQL 12+ (for production)
- Redis (optional, for caching)

## Development Deployment

### Local Setup

```bash
# Clone repository
git clone https://github.com/nt1812/study-time-monitor-agent.git
cd study-time-monitor-agent

# Setup virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
python -c "from database import init_db; init_db()"

# Run application
python app.py
```

## Production Deployment

### Using Docker

**Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

**Build and Run**
```bash
docker build -t study-monitor:latest .
docker run -p 5000:5000 --env-file .env study-monitor:latest
```

### Using Gunicorn (Recommended)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### Using Nginx Reverse Proxy

**nginx.conf**
```nginx
upstream study_monitor {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://study_monitor;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Environment Variables (Production)

```env
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://user:password@host:5432/study_monitor
OPENAI_API_KEY=your_api_key
COURSERA_API_KEY=your_api_key
UDEMY_API_KEY=your_api_key
EDXONLINE_API_KEY=your_api_key
REDIS_URL=redis://localhost:6379/0
AGENT_LOG_LEVEL=INFO
```

## Database Setup (PostgreSQL)

```bash
# Create database
createdb study_monitor

# Create user
psql -c "CREATE USER study_user WITH PASSWORD 'secure_password';"

# Grant privileges
psql -d study_monitor -c "GRANT ALL PRIVILEGES ON DATABASE study_monitor TO study_user;"
```

## Monitoring & Logging

### Application Logs
- Location: `logs/study_monitor.log`
- Format: Rotating file (10MB per file, 10 backups)

### System Monitoring

```bash
# Monitor process
watch -n 1 'ps aux | grep gunicorn'

# Monitor resources
top -p $(pgrep -f gunicorn | tr '\n' ',')
```

## Health Checks

```bash
# Health check endpoint
curl http://localhost:5000/health

# Expected response
{"status": "healthy", "service": "Study Time Monitor Agent", "version": "1.0.0"}
```

## Scaling

### Horizontal Scaling

For multiple instances:

```bash
# Run multiple Gunicorn instances with load balancing
gunicorn --bind 0.0.0.0:5001 app:app &
gunicorn --bind 0.0.0.0:5002 app:app &
gunicorn --bind 0.0.0.0:5003 app:app &
```

### Using Kubernetes (Optional)

**deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: study-monitor
spec:
  replicas: 3
  selector:
    matchLabels:
      app: study-monitor
  template:
    metadata:
      labels:
        app: study-monitor
    spec:
      containers:
      - name: study-monitor
        image: study-monitor:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: study-monitor-secrets
              key: database-url
```

## Backup & Recovery

### Database Backup

```bash
# Backup
pg_dump study_monitor > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
psql study_monitor < backup_20240101_120000.sql
```

## Troubleshooting

### Common Issues

1. **Connection errors**
   - Check database connectivity
   - Verify environment variables
   - Check network firewall rules

2. **API key errors**
   - Verify API keys in .env
   - Check rate limiting on external APIs
   - Verify API access permissions

3. **High memory usage**
   - Adjust Gunicorn workers
   - Check for memory leaks
   - Monitor long-running tasks

### Debug Mode

```bash
FLASK_ENV=development FLASK_DEBUG=1 python app.py
```

## Support

For deployment issues, please refer to the main README.md or open an issue on GitHub.
