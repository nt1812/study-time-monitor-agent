"""Flask API server for Study Time Monitor Agent"""

import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from config import config, DevelopmentConfig
from agent.core import StudyTimeMonitorAgent
from agent.models import User

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)

# Initialize the AI Agent
agent = StudyTimeMonitorAgent(app.config)

# Store active monitoring tasks
monitoring_tasks = {}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Study Time Monitor Agent",
        "version": "1.0.0"
    }), 200


@app.route('/api/v1/monitor/start', methods=['POST'])
def start_monitoring():
    """Start monitoring study time for a user
    
    Request body:
    {
        "user_id": "user_123",
        "interval_seconds": 300  # Optional, defaults to config value
    }
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        interval_seconds = data.get('interval_seconds')
        
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        if user_id in monitoring_tasks:
            return jsonify({"error": "Already monitoring this user"}), 409
        
        # Start monitoring task
        loop = asyncio.new_event_loop()
        task = loop.create_task(
            agent.start_monitoring(user_id, interval_seconds)
        )
        monitoring_tasks[user_id] = task
        
        logger.info(f"Started monitoring for user: {user_id}")
        return jsonify({
            "status": "monitoring_started",
            "user_id": user_id,
            "interval_seconds": interval_seconds or agent.config.STUDY_CHECK_INTERVAL
        }), 200
    except Exception as e:
        logger.error(f"Error starting monitoring: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/monitor/stop/<user_id>', methods=['POST'])
def stop_monitoring(user_id):
    """Stop monitoring study time for a user"""
    try:
        if user_id not in monitoring_tasks:
            return jsonify({"error": "No active monitoring for this user"}), 404
        
        task = monitoring_tasks[user_id]
        task.cancel()
        del monitoring_tasks[user_id]
        
        logger.info(f"Stopped monitoring for user: {user_id}")
        return jsonify({
            "status": "monitoring_stopped",
            "user_id": user_id
        }), 200
    except Exception as e:
        logger.error(f"Error stopping monitoring: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/analyze/<user_id>', methods=['GET'])
def analyze_user(user_id):
    """Get current analysis for a user
    
    Query parameters:
    - period_days: Number of days to analyze (default: 7)
    """
    try:
        period_days = request.args.get('period_days', 7, type=int)
        
        # Run async function
        loop = asyncio.new_event_loop()
        report = loop.run_until_complete(
            agent.get_user_report(user_id, period_days)
        )
        
        return jsonify(report), 200
    except Exception as e:
        logger.error(f"Error analyzing user {user_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/monitor/<user_id>', methods=['GET'])
def get_monitoring_status(user_id):
    """Get current monitoring status for a user"""
    try:
        # Run async function
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            agent.monitor_user_study_time(user_id)
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error getting monitoring status: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/alerts/<user_id>', methods=['GET'])
def get_alerts(user_id):
    """Get alerts for a user
    
    Query parameters:
    - resolved: Filter by resolved status (true/false)
    """
    try:
        resolved = request.args.get('resolved', type=lambda x: x.lower() == 'true')
        
        user_alerts = [
            a.to_dict() for a in agent.alerts
            if a.user_id == user_id
        ]
        
        if resolved is not None:
            user_alerts = [
                a for a in user_alerts
                if a['resolved'] == resolved
            ]
        
        return jsonify({
            "user_id": user_id,
            "alerts": user_alerts,
            "total_alerts": len(user_alerts)
        }), 200
    except Exception as e:
        logger.error(f"Error getting alerts: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/alerts/<user_id>/<alert_id>/resolve', methods=['POST'])
def resolve_alert(user_id, alert_id):
    """Mark an alert as resolved"""
    try:
        for alert in agent.alerts:
            if alert.user_id == user_id:
                alert.resolved = True
                return jsonify({
                    "status": "resolved",
                    "alert": alert.to_dict()
                }), 200
        
        return jsonify({"error": "Alert not found"}), 404
    except Exception as e:
        logger.error(f"Error resolving alert: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/users/register', methods=['POST'])
def register_user():
    """Register a new user for monitoring
    
    Request body:
    {
        "user_id": "user_123",
        "name": "John Doe",
        "email": "john@example.com",
        "enrolled_platforms": ["coursera", "udemy"]
    }
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if user_id in agent.users:
            return jsonify({"error": "User already registered"}), 409
        
        user = User(
            user_id=user_id,
            name=data.get('name'),
            email=data.get('email'),
            enrolled_platforms=data.get('enrolled_platforms', [])
        )
        
        agent.users[user_id] = user
        logger.info(f"Registered new user: {user_id}")
        
        return jsonify({
            "status": "registered",
            "user": user.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user information"""
    try:
        if user_id not in agent.users:
            return jsonify({"error": "User not found"}), 404
        
        user = agent.users[user_id]
        return jsonify(user.to_dict()), 200
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard overview"""
    try:
        return jsonify({
            "total_users": len(agent.users),
            "active_monitoring": len(monitoring_tasks),
            "total_alerts": len(agent.alerts),
            "total_sessions": len(agent.study_sessions)
        }), 200
    except Exception as e:
        logger.error(f"Error getting dashboard: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    logger.info("Starting Study Time Monitor Agent API Server")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
