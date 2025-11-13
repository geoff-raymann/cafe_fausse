"""
Configuration management for Café Fausse Backend
Handles environment variables and application settings
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = ENVIRONMENT == 'development'
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'cafe_fausse_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASS = os.getenv('DB_PASS', 'Pass123')
    DB_PORT = os.getenv('DB_PORT', '5432')
    
    # JWT
    JWT_SECRET = os.getenv('JWT_SECRET', 'cafe-fausse-jwt-secret-change-in-production')
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))
    
    # Email
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_ENABLED = EMAIL_ADDRESS and EMAIL_PASSWORD
    
    # Café Information
    CAFE_NAME = os.getenv('CAFE_NAME', 'Café Fausse')
    CAFE_PHONE = os.getenv('CAFE_PHONE', '(202) 555-4567')
    CAFE_ADDRESS = os.getenv('CAFE_ADDRESS', '123 Quantum Street, Digital District')
    CAFE_EMAIL = os.getenv('CAFE_EMAIL', 'info@cafefausse.com')
    
    # Admin
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', EMAIL_ADDRESS)
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'CafeFausse2025!')
    
    # Reservations
    TOTAL_TABLES = int(os.getenv('TOTAL_TABLES', '30'))
    MAX_GUESTS_PER_RESERVATION = int(os.getenv('MAX_GUESTS_PER_RESERVATION', '10'))
    MIN_GUESTS_PER_RESERVATION = int(os.getenv('MIN_GUESTS_PER_RESERVATION', '1'))
    
    # CORS
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    ALLOWED_ORIGINS = [
        FRONTEND_URL,
        'http://localhost:3000',
        'http://localhost:3001',
    ]
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required_for_production = [
            ('JWT_SECRET', cls.JWT_SECRET),
            ('DB_HOST', cls.DB_HOST),
            ('DB_NAME', cls.DB_NAME),
        ]
        
        if cls.ENVIRONMENT == 'production':
            missing = [name for name, value in required_for_production 
                      if not value or value == f'dev-{name.lower()}']
            if missing:
                raise ValueError(f"Missing required production config: {', '.join(missing)}")
        
        return True
    
    @classmethod
    def get_cors_origins(cls):
        """Get list of allowed CORS origins"""
        origins = cls.ALLOWED_ORIGINS.copy()
        
        # Add production URLs if in production
        if cls.ENVIRONMENT == 'production' and cls.FRONTEND_URL:
            if cls.FRONTEND_URL not in origins:
                origins.append(cls.FRONTEND_URL)
        
        return origins


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Override with stricter settings
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '30'))


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
    # Use test database
    DB_NAME = 'cafe_fausse_test_db'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('ENVIRONMENT', 'development')
    return config.get(env, config['default'])
