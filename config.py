import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///study_monitor.db')
    MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/study_monitor')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # AI/LLM Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    AGENT_MODEL = os.getenv('AGENT_MODEL', 'gpt-4')
    AGENT_TEMPERATURE = float(os.getenv('AGENT_TEMPERATURE', 0.7))
    
    # Monitoring Configuration
    STUDY_CHECK_INTERVAL = int(os.getenv('STUDY_CHECK_INTERVAL', 300))  # 5 minutes
    ALERT_THRESHOLD_MINUTES = int(os.getenv('ALERT_THRESHOLD_MINUTES', 1800))  # 30 minutes
    
    # External Platform APIs
    COURSERA_API_KEY = os.getenv('COURSERA_API_KEY')
    UDEMY_API_KEY = os.getenv('UDEMY_API_KEY')
    EDXONLINE_API_KEY = os.getenv('EDXONLINE_API_KEY')
    
    # Logging
    LOG_LEVEL = os.getenv('AGENT_LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'sqlite:///test.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
