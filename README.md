# Study Time Monitor AI Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

An intelligent AI Agent for monitoring and analyzing study time across multiple educational platforms. This system uses machine learning and LLMs to provide personalized insights and recommendations to optimize student learning effectiveness.

## Features

✨ **Multi-Platform Integration**
- Support for Coursera, Udemy, and edX
- Unified study time tracking across platforms
- Real-time data synchronization

🤖 **AI-Powered Analysis**
- OpenAI GPT-4 integration for intelligent insights
- Study pattern analysis and predictions
- Personalized learning recommendations

📊 **Comprehensive Analytics**
- Study session tracking
- Peak hours identification
- Study streak monitoring
- Effectiveness scoring

🔔 **Smart Alerts**
- Low study time warnings
- Inconsistent pattern detection
- Customizable alert thresholds
- Multi-channel notifications (Email, Slack)

📈 **Reporting & Dashboards**
- Weekly/monthly study reports
- Visual analytics
- Progress tracking
- Comparative analysis

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Redis (optional, for caching)
- PostgreSQL (optional, for production)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/nt1812/study-time-monitor-agent.git
cd study-time-monitor-agent
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. **Initialize database**
```bash
python -c "from database import init_db; init_db()"
```

6. **Run the application**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Configuration

Create a `.env` file based on `.env.example`:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key
COURSERA_API_KEY=your_coursera_key
UDEMY_API_KEY=your_udemy_key
EDXONLINE_API_KEY=your_edx_key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/study_monitor

# Agent Configuration
AGENT_MODEL=gpt-4
AGENT_TEMPERATURE=0.7
STUDY_CHECK_INTERVAL=300
ALERT_THRESHOLD_MINUTES=1800
```

## API Documentation

### Health Check
```http
GET /health
```

### User Management

**Register User**
```http
POST /api/v1/users/register
Content-Type: application/json

{
  "user_id": "user_123",
  "name": "John Doe",
  "email": "john@example.com",
  "enrolled_platforms": ["coursera", "udemy"]
}
```

**Get User Info**
```http
GET /api/v1/users/{user_id}
```

### Monitoring

**Start Monitoring**
```http
POST /api/v1/monitor/start
Content-Type: application/json

{
  "user_id": "user_123",
  "interval_seconds": 300
}
```

**Get Current Status**
```http
GET /api/v1/monitor/{user_id}
```

**Stop Monitoring**
```http
POST /api/v1/monitor/stop/{user_id}
```

### Analysis & Reports

**Get Analysis Report**
```http
GET /api/v1/analyze/{user_id}?period_days=7
```

### Alerts

**Get User Alerts**
```http
GET /api/v1/alerts/{user_id}?resolved=false
```

**Resolve Alert**
```http
POST /api/v1/alerts/{user_id}/{alert_id}/resolve
```

### Dashboard

**Get Dashboard Overview**
```http
GET /api/v1/dashboard
```

## Usage Examples

### Python Integration

```python
from agent.core import StudyTimeMonitorAgent
import asyncio

# Initialize agent
agent = StudyTimeMonitorAgent()

# Monitor a user
async def monitor():
    result = await agent.monitor_user_study_time("user_123")
    print(result)

asyncio.run(monitor())
```

### cURL Examples

```bash
# Register a user
curl -X POST http://localhost:5000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123", "name": "John", "email": "john@example.com", "enrolled_platforms": ["coursera"]}'

# Start monitoring
curl -X POST http://localhost:5000/api/v1/monitor/start \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123", "interval_seconds": 300}'

# Get analysis
curl http://localhost:5000/api/v1/analyze/user_123?period_days=7
```

## Project Structure

```
study-time-monitor-agent/
├── agent/
│   ├── __init__.py
│   ├── core.py                 # Main agent logic
│   ├── models.py               # Data models
│   ├── platform_integrations.py # Platform APIs
│   └── analytics.py            # Analytics engine
├── app.py                      # Flask API server
├── config.py                   # Configuration
├── database.py                 # Database models
├── logger.py                   # Logging setup
├── utils.py                    # Utility functions
├── requirements.txt            # Dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## Architecture

### Agent Components

1. **Core Agent** (`agent/core.py`)
   - Main orchestration logic
   - User monitoring and analysis
   - Insight generation using LLMs
   - Alert management

2. **Platform Integration** (`agent/platform_integrations.py`)
   - APIs for educational platforms
   - Concurrent data fetching
   - Data normalization

3. **Analytics Engine** (`agent/analytics.py`)
   - Study pattern analysis
   - Peak hour identification
   - Study streak calculation
   - Effectiveness scoring

4. **API Server** (`app.py`)
   - REST API endpoints
   - Request handling
   - Response formatting

## Key Features Explained

### Study Time Monitoring
The agent continuously monitors study sessions across multiple platforms and aggregates data for comprehensive analysis.

### Pattern Analysis
Using analytics, the system identifies:
- Peak study hours
- Consistency patterns
- Platform preferences
- Content type engagement

### AI Insights
OpenAI GPT-4 generates personalized recommendations based on:
- Historical study patterns
- Current performance metrics
- Best practice recommendations
- Goal alignment

### Alert System
Automated alerts notify users of:
- Low study time
- No activity detected
- Inconsistent patterns
- Goal misalignment

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the development team.

## Roadmap

- [ ] Mobile app support
- [ ] Advanced ML model integration
- [ ] Video content analysis
- [ ] Peer comparison analytics
- [ ] Integration with more platforms (LinkedIn Learning, Pluralsight)
- [ ] Gamification features
- [ ] Voice/chatbot interface

## Acknowledgments

- OpenAI for GPT-4 API
- Educational platform providers (Coursera, Udemy, edX)
- Python community for excellent libraries
