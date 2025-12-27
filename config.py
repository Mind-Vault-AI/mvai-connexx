"""
MVAI Connexx - Configuration Module
Hybrid deployment configuratie met private network support
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuratie"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SESSION_LIFETIME_HOURS = int(os.getenv('SESSION_LIFETIME_HOURS', 24))

    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'mvai_connexx.db')
    BACKUP_DIR = os.getenv('BACKUP_DIR', 'backups')
    BACKUP_RETENTION_DAYS = int(os.getenv('BACKUP_RETENTION_DAYS', 30))

    # Security
    ENABLE_IP_WHITELIST = os.getenv('ENABLE_IP_WHITELIST', 'false').lower() == 'true'
    ENABLE_THREAT_DETECTION = os.getenv('ENABLE_THREAT_DETECTION', 'true').lower() == 'true'
    ENABLE_HONEYPOT = os.getenv('ENABLE_HONEYPOT', 'true').lower() == 'true'
    AUTO_BLACKLIST_THRESHOLD = int(os.getenv('AUTO_BLACKLIST_THRESHOLD', 5))
    BLACKLIST_DURATION_HOURS = int(os.getenv('BLACKLIST_DURATION_HOURS', 24))

    # Rate Limiting
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'true').lower() == 'true'
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '200 per day;50 per hour')
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')

    # Private Network
    PRIVATE_NETWORK_MODE = os.getenv('PRIVATE_NETWORK_MODE', 'public')  # public, private, hybrid
    ALLOWED_NETWORKS = os.getenv('ALLOWED_NETWORKS', '').split(',') if os.getenv('ALLOWED_NETWORKS') else []
    VPN_REQUIRED = os.getenv('VPN_REQUIRED', 'false').lower() == 'true'

    # Trusted IPs (comma separated)
    TRUSTED_IPS = os.getenv('TRUSTED_IPS', '').split(',') if os.getenv('TRUSTED_IPS') else []

    # Admin IPs (alleen deze IPs kunnen admin panel gebruiken)
    ADMIN_IPS = os.getenv('ADMIN_IPS', '').split(',') if os.getenv('ADMIN_IPS') else []

    # Deployment
    DEPLOYMENT_MODE = os.getenv('DEPLOYMENT_MODE', 'cloud')  # cloud, on-premise, hybrid
    INTERNAL_IP_RANGE = os.getenv('INTERNAL_IP_RANGE', '10.0.0.0/8,172.16.0.0/12,192.168.0.0/16')

class DevelopmentConfig(Config):
    """Development configuratie"""
    DEBUG = True
    ENABLE_IP_WHITELIST = False
    RATELIMIT_ENABLED = False

class ProductionConfig(Config):
    """Production configuratie"""
    DEBUG = False
    ENABLE_IP_WHITELIST = True
    ENABLE_THREAT_DETECTION = True
    RATELIMIT_ENABLED = True

class HybridConfig(Config):
    """Hybrid deployment configuratie"""
    PRIVATE_NETWORK_MODE = 'hybrid'
    VPN_REQUIRED = True
    ENABLE_IP_WHITELIST = True

# Config selector
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'hybrid': HybridConfig
}

def get_config():
    """Haal configuratie op basis van environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, DevelopmentConfig)
