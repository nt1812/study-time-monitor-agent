"""Core AI Agent for monitoring study time on educational platforms"""

import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
import openai
from config import Config
from agent.models import StudySession, Alert, User
from agent.platform_integrations import PlatformIntegration
from agent.analytics import AnalyticsEngine

logger = logging.getLogger(__name__)


class StudyTimeMonitorAgent:
    """AI Agent for monitoring and analyzing study time on educational platforms"""

    def __init__(self, config: Config = None):
        """Initialize the Study Time Monitor Agent
        
        Args:
            config: Configuration object for the agent
        """
        self.config = config or Config()
        self.platform_integration = PlatformIntegration()
        self.analytics_engine = AnalyticsEngine()
        self.users: Dict[str, User] = {}
        self.study_sessions: List[StudySession] = []
        self.alerts: List[Alert] = []
        
        openai.api_key = self.config.OPENAI_API_KEY
        logger.info("Study Time Monitor Agent initialized")

    async def monitor_user_study_time(self, user_id: str) -> Dict:
        """Monitor study time for a specific user
        
        Args:
            user_id: ID of the user to monitor
            
        Returns:
            Dictionary with monitoring results
        """
        try:
            # Fetch user data from educational platforms
            user_data = await self.platform_integration.fetch_user_study_data(user_id)
            
            # Analyze study patterns
            analysis = self.analytics_engine.analyze_study_patterns(user_data)
            
            # Generate insights using LLM
            insights = await self._generate_insights(user_id, analysis)
            
            # Check for alerts
            alerts = self._check_alerts(user_id, analysis)
            
            return {
                "user_id": user_id,
                "study_data": user_data,
                "analysis": analysis,
                "insights": insights,
                "alerts": alerts,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error monitoring user {user_id}: {str(e)}")
            raise

    async def _generate_insights(self, user_id: str, analysis: Dict) -> str:
        """Generate AI insights about study patterns
        
        Args:
            user_id: ID of the user
            analysis: Analysis results
            
        Returns:
            AI-generated insights
        """
        try:
            prompt = f"""
            Based on the following study time analysis for user {user_id}:
            
            Total Study Time: {analysis.get('total_study_time', 0)} minutes
            Average Daily Study: {analysis.get('avg_daily_study', 0)} minutes
            Study Streak: {analysis.get('study_streak', 0)} days
            Most Active Platform: {analysis.get('most_active_platform', 'N/A')}
            Peak Study Hours: {analysis.get('peak_hours', [])}
            
            Provide personalized recommendations to improve study effectiveness.
            """
            
            response = await asyncio.to_thread(
                openai.ChatCompletion.create,
                model=self.config.AGENT_MODEL,
                messages=[
                    {"role": "system", "content": "You are an educational AI assistant helping students optimize their study time."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.AGENT_TEMPERATURE,
                max_tokens=500
            )
            
            return response['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return "Unable to generate insights at this time."

    def _check_alerts(self, user_id: str, analysis: Dict) -> List[Alert]:
        """Check for alerts based on study patterns
        
        Args:
            user_id: ID of the user
            analysis: Analysis results
            
        Returns:
            List of alerts
        """
        alerts = []
        
        # Alert if study time is below threshold
        total_study = analysis.get('total_study_time', 0)
        if total_study < self.config.ALERT_THRESHOLD_MINUTES:
            alerts.append(Alert(
                user_id=user_id,
                alert_type="LOW_STUDY_TIME",
                message=f"Study time is below recommended threshold: {total_study} minutes",
                severity="medium"
            ))
        
        # Alert if no study activity
        if total_study == 0:
            alerts.append(Alert(
                user_id=user_id,
                alert_type="NO_ACTIVITY",
                message="No study activity detected in the monitoring period",
                severity="high"
            ))
        
        # Alert if inconsistent study patterns
        if analysis.get('study_streak', 0) == 0 and analysis.get('total_study_time', 0) > 0:
            alerts.append(Alert(
                user_id=user_id,
                alert_type="INCONSISTENT_PATTERN",
                message="Study activity is inconsistent. Try to maintain a regular schedule.",
                severity="low"
            ))
        
        self.alerts.extend(alerts)
        return alerts

    async def get_user_report(self, user_id: str, period_days: int = 7) -> Dict:
        """Generate a comprehensive study report for a user
        
        Args:
            user_id: ID of the user
            period_days: Number of days to include in the report
            
        Returns:
            Comprehensive study report
        """
        try:
            report_data = await self.platform_integration.fetch_user_study_data(
                user_id, 
                days=period_days
            )
            analysis = self.analytics_engine.analyze_study_patterns(report_data)
            
            return {
                "user_id": user_id,
                "period_days": period_days,
                "report_date": datetime.utcnow().isoformat(),
                "summary": analysis,
                "alerts": [a.to_dict() for a in self.alerts if a.user_id == user_id]
            }
        except Exception as e:
            logger.error(f"Error generating report for user {user_id}: {str(e)}")
            raise

    async def start_monitoring(self, user_id: str, interval_seconds: int = None):
        """Start continuous monitoring for a user
        
        Args:
            user_id: ID of the user to monitor
            interval_seconds: Interval between checks (uses config default if None)
        """
        interval = interval_seconds or self.config.STUDY_CHECK_INTERVAL
        logger.info(f"Starting continuous monitoring for user {user_id} with interval {interval}s")
        
        while True:
            try:
                result = await self.monitor_user_study_time(user_id)
                logger.info(f"Monitoring result for {user_id}: {result}")
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
            
            await asyncio.sleep(interval)
