# Quick Start Guide for Study Time Monitor AI Agent

## 🚀 Quick Start (5 minutes)

### Option 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/nt1812/study-time-monitor-agent.git
cd study-time-monitor-agent

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
vim .env

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api
```

### Option 2: Local Development

```bash
# Clone repository
git clone https://github.com/nt1812/study-time-monitor-agent.git
cd study-time-monitor-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
vim .env  # Add your API keys

# Initialize database
python -c "from database import init_db; init_db()"

# Run application
python app.py
```

## 📋 API Quick Reference

### Health Check
```bash
curl http://localhost:5000/health
```

### Register User
```bash
curl -X POST http://localhost:5000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "student_001",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "enrolled_platforms": ["coursera", "udemy"]
  }'
```

### Start Monitoring
```bash
curl -X POST http://localhost:5000/api/v1/monitor/start \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "student_001",
    "interval_seconds": 300
  }'
```

### Get Analysis Report
```bash
curl http://localhost:5000/api/v1/analyze/student_001?period_days=7
```

### Get Alerts
```bash
curl http://localhost:5000/api/v1/alerts/student_001
```

### Dashboard
```bash
curl http://localhost:5000/api/v1/dashboard
```

## 🔧 Configuration

### Essential Environment Variables

```env
# OpenAI API (required for AI insights)
OPENAI_API_KEY=sk-...

# Educational Platform APIs
COURSERA_API_KEY=your_key
UDEMY_API_KEY=your_key
EDXONLINE_API_KEY=your_key

# Database (optional, defaults to SQLite)
DATABASE_URL=postgresql://user:pass@localhost/study_monitor

# Monitoring
STUDY_CHECK_INTERVAL=300  # Check every 5 minutes
ALERT_THRESHOLD_MINUTES=1800  # Alert if < 30 minutes per day
```

## 🧪 Testing

```bash
# Run unit tests
pytest tests.py -v

# Run with coverage
pytest tests.py --cov=agent

# Run specific test
pytest tests.py::TestStudyTimeMonitorAgent::test_agent_initialization -v
```

## 📊 Monitoring Your Instance

### Check Service Health
```bash
# All services
docker-compose ps

# Database connection
docker-compose exec api python -c "from database import get_session; s = get_session(); print('DB OK')"

# API health
curl -s http://localhost:5000/health | jq .
```

### View Logs
```bash
# API logs
docker-compose logs -f api

# Database logs
docker-compose logs -f postgres

# All logs
docker-compose logs -f
```

## 🛑 Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# Stop local server
Ctrl+C
```

## 📱 Next Steps

1. **Register your first user** (see API Quick Reference above)
2. **Configure API keys** for educational platforms
3. **Start monitoring** a user
4. **View reports** and alerts
5. **Customize alerts** based on your needs

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Change port in docker-compose.yml or locally
# Docker: change ports in docker-compose.yml
# Local: modify app.py or use PORT environment variable
```

### Database Connection Error
```bash
# Check database is running
docker-compose ps postgres

# Verify DATABASE_URL in .env
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

### API Key Issues
```bash
# Verify .env file exists
ls -la .env

# Check API keys are set
echo $OPENAI_API_KEY
echo $COURSERA_API_KEY
```

## 📚 Full Documentation

- [README.md](README.md) - Complete documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment guide
- [API Endpoints](README.md#api-documentation) - Full API reference

## 💬 Support

- GitHub Issues: https://github.com/nt1812/study-time-monitor-agent/issues
- Documentation: Check README.md and DEPLOYMENT.md

## 🎉 You're Ready!

Your Study Time Monitor AI Agent is now ready to use. Start by registering a user and monitoring their study time!
