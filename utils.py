"""Utility functions for the application"""

import uuid
from datetime import datetime, timedelta
import json


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID
    
    Args:
        prefix: Optional prefix for the ID
        
    Returns:
        Generated unique ID
    """
    unique_id = str(uuid.uuid4())
    return f"{prefix}_{unique_id}" if prefix else unique_id


def get_time_range(days: int = 7) -> tuple:
    """Get start and end datetime for a period
    
    Args:
        days: Number of days in the period
        
    Returns:
        Tuple of (start_datetime, end_datetime)
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    return start_time, end_time


def format_duration(minutes: int) -> str:
    """Format minutes to human-readable duration
    
    Args:
        minutes: Duration in minutes
        
    Returns:
        Formatted duration string
    """
    if minutes < 60:
        return f"{minutes}m"
    elif minutes < 1440:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins}m"
    else:
        days = minutes // 1440
        remaining_minutes = minutes % 1440
        hours = remaining_minutes // 60
        return f"{days}d {hours}h"


def calculate_study_effectiveness(total_time: int, sessions_count: int) -> float:
    """Calculate study effectiveness score
    
    Args:
        total_time: Total study time in minutes
        sessions_count: Number of study sessions
        
    Returns:
        Effectiveness score (0-100)
    """
    if sessions_count == 0:
        return 0.0
    
    avg_session_time = total_time / sessions_count
    
    # Score based on session duration (longer sessions = better focus)
    if avg_session_time < 15:
        score = 30
    elif avg_session_time < 30:
        score = 60
    elif avg_session_time < 60:
        score = 80
    else:
        score = 100
    
    # Adjust based on total time (minimum 3 hours per week)
    if total_time < 180:
        score *= 0.7
    elif total_time > 420:
        score = min(100, score * 1.1)
    
    return round(score, 2)


def parse_platform_response(response: dict, platform: str) -> dict:
    """Parse platform API response
    
    Args:
        response: API response dictionary
        platform: Platform name
        
    Returns:
        Parsed response data
    """
    parsed = {
        "platform": platform,
        "total_minutes": 0,
        "sessions": []
    }
    
    try:
        if platform == "coursera":
            parsed["total_minutes"] = response.get("totalLearningTime", 0)
            parsed["sessions"] = response.get("learningActivities", [])
        elif platform == "udemy":
            parsed["total_minutes"] = response.get("total_learning_time", 0)
            parsed["sessions"] = response.get("courses", [])
        elif platform == "edx":
            parsed["total_minutes"] = response.get("time_spent_hours", 0) * 60
            parsed["sessions"] = response.get("enrollments", [])
    except (KeyError, TypeError) as e:
        print(f"Error parsing {platform} response: {e}")
    
    return parsed


def send_email_alert(email: str, subject: str, body: str) -> bool:
    """Send email alert to user
    
    Args:
        email: Recipient email
        subject: Email subject
        body: Email body
        
    Returns:
        Success status
    """
    # Implementation would integrate with email service (SendGrid, AWS SES, etc.)
    print(f"Email sent to {email}: {subject}")
    return True


def send_slack_notification(webhook_url: str, message: str) -> bool:
    """Send Slack notification
    
    Args:
        webhook_url: Slack webhook URL
        message: Message to send
        
    Returns:
        Success status
    """
    # Implementation would send to Slack webhook
    print(f"Slack notification sent: {message}")
    return True
