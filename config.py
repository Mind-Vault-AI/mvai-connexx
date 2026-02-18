"""
MVAI Connexx - Configuration Module
Hybrid deployment configuratie met private network support
"""
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Initialize logger at module level
logger = logging.getLogger(__name__)

class Config:
    """Base configuratie"""

    # Flask
    DEFAULT_SECRET_KEY = 'dev-secret-key-change-in-production'
    SECRET_KEY = os.getenv('SECRET_KEY', DEFAULT_SECRET_KEY)
    SESSION_LIFETIME_HOURS = int(os.getenv('SESSION_LIFETIME_HOURS', 24))

    # Database
    # Fly.io uses /app/data volume, local uses current directory
    _default_db_path = '/app/data/mvai_connexx.db' if os.path.exists('/app/data') else 'mvai_connexx.db'
    DATABASE_PATH = os.getenv('DATABASE_PATH', _default_db_path)

    _default_backup_dir = '/app/data/backups' if os.path.exists('/app/data') else 'backups'
    BACKUP_DIR = os.getenv('BACKUP_DIR', _default_backup_dir)
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

    # AI / OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo')
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', 1000))
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', 0.7))

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

    # Payments - ACTIEF: Gumroad (PayPal backend)
    PAYMENT_PROVIDER = os.getenv('PAYMENT_PROVIDER', 'gumroad')  # gumroad, stripe, mollie

    # Gumroad (ACTIEF - eerst $100, dan PayPal)
    GUMROAD_USERNAME = os.getenv('GUMROAD_USERNAME', 'mindvault-ai')
    GUMROAD_PARTICULIER_URL = os.getenv('GUMROAD_PARTICULIER_URL', 'https://mindvault-ai.gumroad.com/l/mvai-particulier')
    GUMROAD_MKB_URL = os.getenv('GUMROAD_MKB_URL', 'https://mindvault-ai.gumroad.com/l/mvai-mkb')
    GUMROAD_STARTER_URL = os.getenv('GUMROAD_STARTER_URL', 'https://mindvault-ai.gumroad.com/l/mvai-starter')
    GUMROAD_PROFESSIONAL_URL = os.getenv('GUMROAD_PROFESSIONAL_URL', 'https://mindvault-ai.gumroad.com/l/mvai-professional')
    GUMROAD_ENTERPRISE_URL = os.getenv('GUMROAD_ENTERPRISE_URL', 'https://mindvault-ai.gumroad.com/l/mvai-enterprise')

    # Stripe (DISABLED - wacht op KVK)
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')

    # Mollie (alternatief)
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

class ConfigValidator:
    """Valideer dat alle verplichte environment variables zijn ingesteld"""
    
    REQUIRED_FOR_PRODUCTION = [
        'SECRET_KEY',
        'DOMAIN',
        'COMPANY_EMAIL',
    ]
    
    REQUIRED_FOR_PAYMENTS = [
        'PAYMENT_PROVIDER',  # moet 'gumroad', 'stripe', of 'mollie' zijn
    ]
    
    OPTIONAL_BUT_RECOMMENDED = [
        'OPENAI_API_KEY',  # Voor AI Assistant
        'SMTP_USERNAME',    # Voor email notificaties
        'SMTP_PASSWORD',
    ]
    
    VALID_PAYMENT_PROVIDERS = ['gumroad', 'stripe', 'mollie']
    
    @classmethod
    def validate_config(cls, config_obj, environment='production'):
        """
        Valideer configuratie
        
        Args:
            config_obj: Config class instance
            environment: 'development', 'production', of 'hybrid'
        
        Raises:
            ValueError: Als verplichte config ontbreekt in productie
        """
        missing_required = []
        missing_optional = []
        
        # Production-specific validation
        if environment == 'production':
            # Check required variables
            for var in cls.REQUIRED_FOR_PRODUCTION:
                value = getattr(config_obj, var, None)
                # Special handling for SECRET_KEY to check for default value
                if var == 'SECRET_KEY':
                    if not value or value == config_obj.DEFAULT_SECRET_KEY:
                        missing_required.append('SECRET_KEY (must be set to a unique value!)')
                elif not value:
                    missing_required.append(var)
            
            # Check payment provider is set and valid
            payment_provider = getattr(config_obj, 'PAYMENT_PROVIDER', '')
            if not payment_provider:
                missing_required.append('PAYMENT_PROVIDER (not set)')
            elif payment_provider not in cls.VALID_PAYMENT_PROVIDERS:
                missing_required.append(f'PAYMENT_PROVIDER (invalid: {payment_provider})')
        
        # Check optional but recommended variables
        for var in cls.OPTIONAL_BUT_RECOMMENDED:
            value = getattr(config_obj, var, None)
            if not value:
                missing_optional.append(var)
        
        # Report missing variables
        if environment == 'production' and missing_required:
            missing_list = '\n'.join(f'  - {var}' for var in missing_required)
            error_msg = f"""
╔═══════════════════════════════════════════════════════╗
║  ⚠️  PRODUCTION CONFIGURATION ERROR                   ║
╚═══════════════════════════════════════════════════════╝

MISSING REQUIRED ENVIRONMENT VARIABLES:
{missing_list}

Add these to your .env file or set as environment variables!

Example .env:
SECRET_KEY=generate_with_python_secrets
DOMAIN=yourdomain.com
COMPANY_EMAIL=info@yourdomain.com
PAYMENT_PROVIDER=gumroad
"""
            raise ValueError(error_msg)
        
        if missing_optional and environment == 'production':
            optional_list = '\n'.join(f'  - {var}' for var in missing_optional)
            warning_msg = f"""
⚠️  OPTIONAL CONFIGURATION MISSING (recommended for full functionality):
{optional_list}
"""
            logger.warning(warning_msg)
        
        return True
