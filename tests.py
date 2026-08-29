"""Unit tests for Study Time Monitor Agent"""

import pytest
import asyncio
from datetime import datetime
from agent.core import StudyTimeMonitorAgent
from agent.models import User, StudySession, Alert
from agent.analytics import AnalyticsEngine
from config import TestingConfig


class TestStudyTimeMonitorAgent:
    """Test cases for the main agent"""
    
    @pytest.fixture
    def agent(self):
        """Fixture to create agent instance"""
        return StudyTimeMonitorAgent(TestingConfig())
    
    def test_agent_initialization(self, agent):
        """Test agent initialization"""
        assert agent is not None
        assert agent.users == {}
        assert agent.study_sessions == []
        assert agent.alerts == []
    
    @pytest.mark.asyncio
    async def test_monitor_user_study_time(self, agent):
        """Test monitoring user study time"""
        result = await agent.monitor_user_study_time("test_user_123")
        assert result is not None
        assert "user_id" in result
        assert result["user_id"] == "test_user_123"
    
    def test_check_alerts(self, agent):
        """Test alert checking"""
        analysis = {
            "total_study_time": 100,
            "study_streak": 0
        }
        alerts = agent._check_alerts("test_user", analysis)
        assert isinstance(alerts, list)


class TestModels:
    """Test cases for data models"""
    
    def test_user_model(self):
        """Test User model"""
        user = User(
            user_id="user_123",
            name="John Doe",
            email="john@example.com",
            enrolled_platforms=["coursera"]
        )
        assert user.user_id == "user_123"
        assert user.name == "John Doe"
        
        user_dict = user.to_dict()
        assert "created_at" in user_dict
    
    def test_study_session_model(self):
        """Test StudySession model"""
        now = datetime.utcnow()
        session = StudySession(
            session_id="session_123",
            user_id="user_123",
            platform="coursera",
            course_name="Python 101",
            start_time=now,
            end_time=None,
            duration_minutes=60
        )
        assert session.session_id == "session_123"
        assert session.get_duration() == 60
    
    def test_alert_model(self):
        """Test Alert model"""
        alert = Alert(
            user_id="user_123",
            alert_type="LOW_STUDY_TIME",
            message="Study time is low",
            severity="medium"
        )
        assert alert.user_id == "user_123"
        assert alert.alert_type == "LOW_STUDY_TIME"
        assert not alert.resolved
        
        alert_dict = alert.to_dict()
        assert "created_at" in alert_dict


class TestAnalyticsEngine:
    """Test cases for analytics engine"""
    
    @pytest.fixture
    def analytics(self):
        """Fixture to create analytics engine"""
        return AnalyticsEngine()
    
    def test_analytics_initialization(self, analytics):
        """Test analytics engine initialization"""
        assert analytics is not None
    
    def test_analyze_study_patterns(self, analytics):
        """Test study pattern analysis"""
        study_data = {
            "total_study_time": 300,
            "sessions": [],
            "platforms": {}
        }
        analysis = analytics.analyze_study_patterns(study_data)
        assert "total_study_time" in analysis
        assert "avg_daily_study" in analysis
        assert "study_streak" in analysis
    
    def test_calculate_avg_daily_study(self, analytics):
        """Test average daily study calculation"""
        study_data = {
            "sessions": [
                {"duration_minutes": 60},
                {"duration_minutes": 90}
            ],
            "platforms": {}
        }
        avg = analytics._calculate_avg_daily_study(study_data)
        assert isinstance(avg, (int, float))
    
    def test_get_most_active_platform(self, analytics):
        """Test most active platform identification"""
        study_data = {
            "platforms": {
                "coursera": {"total_minutes": 300},
                "udemy": {"total_minutes": 100}
            },
            "sessions": []
        }
        platform = analytics._get_most_active_platform(study_data)
        assert platform in ["coursera", "udemy"]


class TestIntegration:
    """Integration tests"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_monitoring(self):
        """Test end-to-end monitoring workflow"""
        agent = StudyTimeMonitorAgent(TestingConfig())
        
        # Register user
        user = User(
            user_id="test_e2e",
            name="Test User",
            email="test@example.com",
            enrolled_platforms=["coursera"]
        )
        agent.users["test_e2e"] = user
        
        # Monitor user
        result = await agent.monitor_user_study_time("test_e2e")
        assert result["user_id"] == "test_e2e"
        assert "analysis" in result
        assert "alerts" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
