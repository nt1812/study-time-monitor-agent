"""Analytics engine for studying study patterns"""

import logging
from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """Analyze study patterns and generate insights"""
    
    def __init__(self):
        """Initialize analytics engine"""
        pass
    
    def analyze_study_patterns(self, study_data: Dict) -> Dict:
        """Analyze study data and extract patterns
        
        Args:
            study_data: Study data from platforms
            
        Returns:
            Analysis results with key metrics
        """
        try:
            analysis = {
                "total_study_time": study_data.get("total_study_time", 0),
                "avg_daily_study": self._calculate_avg_daily_study(study_data),
                "study_streak": self._calculate_study_streak(study_data),
                "most_active_platform": self._get_most_active_platform(study_data),
                "peak_hours": self._identify_peak_hours(study_data),
                "platforms_summary": self._summarize_platforms(study_data),
                "sessions_count": len(study_data.get("sessions", []))
            }
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing study patterns: {str(e)}")
            return {}
    
    def _calculate_avg_daily_study(self, study_data: Dict) -> float:
        """Calculate average daily study time"""
        sessions = study_data.get("sessions", [])
        if not sessions:
            return 0.0
        
        # Group sessions by day
        daily_totals = defaultdict(int)
        for session in sessions:
            # Assuming session has a date
            date_key = "today"  # Simplified, would parse actual dates
            daily_totals[date_key] += session.get("duration_minutes", 0)
        
        if not daily_totals:
            return 0.0
        
        return sum(daily_totals.values()) / len(daily_totals)
    
    def _calculate_study_streak(self, study_data: Dict) -> int:
        """Calculate consecutive days of study"""
        sessions = study_data.get("sessions", [])
        if not sessions:
            return 0
        
        # Simplified: count unique days with study activity
        unique_days = set()
        for session in sessions:
            # Parse session date and add to set
            unique_days.add("today")  # Simplified
        
        return len(unique_days)
    
    def _get_most_active_platform(self, study_data: Dict) -> str:
        """Identify the platform with most study time"""
        platforms = study_data.get("platforms", {})
        max_platform = max(
            platforms.items(),
            key=lambda x: x[1].get("total_minutes", 0) if isinstance(x[1], dict) else 0,
            default=("unknown", {})
        )
        return max_platform[0]
    
    def _identify_peak_hours(self, study_data: Dict) -> List[int]:
        """Identify peak study hours"""
        sessions = study_data.get("sessions", [])
        if not sessions:
            return []
        
        hour_counts = defaultdict(int)
        for session in sessions:
            # Extract hour from session start time
            hour = 14  # Simplified
            hour_counts[hour] += 1
        
        # Return top 3 hours
        top_hours = sorted(
            hour_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        return [hour for hour, _ in top_hours]
    
    def _summarize_platforms(self, study_data: Dict) -> Dict:
        """Summarize activity across platforms"""
        platforms = study_data.get("platforms", {})
        summary = {}
        
        for platform, data in platforms.items():
            if isinstance(data, dict) and "error" not in data:
                summary[platform] = {
                    "total_minutes": data.get("total_minutes", 0),
                    "sessions": len(data.get("sessions", []))
                }
        
        return summary
