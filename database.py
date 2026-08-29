"""Database models using SQLAlchemy"""

from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DevelopmentConfig

Base = declarative_base()


class UserModel(Base):
    """User database model"""
    __tablename__ = 'users'
    
    user_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    enrolled_platforms = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class StudySessionModel(Base):
    """Study session database model"""
    __tablename__ = 'study_sessions'
    
    session_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    course_name = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration_minutes = Column(Integer, default=0)
    content_type = Column(String, default='video')
    progress_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class AlertModel(Base):
    """Alert database model"""
    __tablename__ = 'alerts'
    
    alert_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    alert_type = Column(String, nullable=False)
    message = Column(String)
    severity = Column(String, default='medium')
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime)


class AnalyticsModel(Base):
    """Analytics data database model"""
    __tablename__ = 'analytics'
    
    analytics_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    period_days = Column(Integer)
    total_study_time = Column(Integer)
    avg_daily_study = Column(Float)
    study_streak = Column(Integer)
    most_active_platform = Column(String)
    peak_hours = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


# Database initialization
engine = create_engine(DevelopmentConfig.DATABASE_URL)
Session = sessionmaker(bind=engine)


def init_db():
    """Initialize the database"""
    Base.metadata.create_all(engine)


def get_session():
    """Get a database session"""
    return Session()
