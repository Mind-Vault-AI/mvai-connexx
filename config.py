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

    # Company Info
    DOMAIN = os.getenv('DOMAIN', 'mindvault-ai.com')
    COMPANY_NAME = 'Mind Vault AI'
    COMPANY_EMAIL = 'info@mindvault-ai.com'
    COMPANY_WEBSITE = 'https://mindvault-ai.com'

    # Features
    ENABLE_AI_ASSISTANT = os.getenv('ENABLE_AI_ASSISTANT', 'true').lower() == 'true'
    ENABLE_DEMO_MODE = os.getenv('ENABLE_DEMO_MODE', 'true').lower() == 'true'
    DEMO_ACCOUNT_EXPIRY_DAYS = int(os.getenv('DEMO_ACCOUNT_EXPIRY_DAYS', 14))

    # Pricing
    DEFAULT_PRICING_TIER = os.getenv('DEFAULT_PRICING_TIER', 'demo')
    ALLOW_TIER_UPGRADE = True
    ALLOW_TIER_DOWNGRADE = True

    # SLA
    TARGET_UPTIME_PCT = float(os.getenv('TARGET_UPTIME_PCT', 99.9))
    TARGET_RESPONSE_TIME_MS = int(os.getenv('TARGET_RESPONSE_TIME_MS', 200))

    # Email (TODO: Configure in production)
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    SMTP_FROM_EMAIL = os.getenv('SMTP_FROM_EMAIL', 'info@mindvault-ai.com')
    SMTP_FROM_NAME = os.getenv('SMTP_FROM_NAME', 'MVAI Connexx')

    # Payments (TODO: Configure)
    PAYMENT_PROVIDER = os.getenv('PAYMENT_PROVIDER', 'stripe')  # stripe, mollie
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
    MOLLIE_API_KEY = os.getenv('MOLLIE_API_KEY', '')

    # Monitoring
    SENTRY_DSN = os.getenv('SENTRY_DSN', '')
    ENABLE_SENTRY = bool(os.getenv('SENTRY_DSN', ''))

    # Legal Pages
    TERMS_OF_SERVICE_URL = '/legal#terms'
    PRIVACY_POLICY_URL = '/legal#privacy'
    DISCLAIMER_URL = '/legal#disclaimer'

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
