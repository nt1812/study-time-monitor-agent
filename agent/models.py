"""Data models for study time monitoring"""

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, asdict


@dataclass
class User:
    """User model for educational platform"""
    user_id: str
    name: str
    email: str
    enrolled_platforms: List[str]
    created_at: datetime = None
    last_active: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.last_active is None:
            self.last_active = datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['last_active'] = self.last_active.isoformat()
        return data


@dataclass
class StudySession:
    """Study session model"""
    session_id: str
    user_id: str
    platform: str
    course_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: int = 0
    content_type: str = "video"  # video, quiz, assignment, reading
    progress_percentage: float = 0.0
    
    def get_duration(self) -> int:
        """Calculate session duration"""
        if self.end_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() / 60)
        return self.duration_minutes
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "platform": self.platform,
            "course_name": self.course_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_minutes": self.get_duration(),
            "content_type": self.content_type,
            "progress_percentage": self.progress_percentage
        }


@dataclass
class Alert:
    """Alert model for study monitoring"""
    user_id: str
    alert_type: str  # LOW_STUDY_TIME, NO_ACTIVITY, INCONSISTENT_PATTERN, etc.
    message: str
    severity: str = "medium"  # low, medium, high, critical
    created_at: datetime = None
    resolved: bool = False
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "user_id": self.user_id,
            "alert_type": self.alert_type,
            "message": self.message,
            "severity": self.severity,
            "created_at": self.created_at.isoformat(),
            "resolved": self.resolved
        }


@dataclass
class StudyAnalytics:
    """Analytics data model"""
    user_id: str
    period_days: int
    total_study_time: int  # in minutes
    avg_daily_study: float
    study_streak: int
    most_active_platform: str
    peak_hours: List[int]
    courses_enrolled: int
    completion_rate: float
    
    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)
