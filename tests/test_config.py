"""
Tests voor config.py - Configuratie module
"""
import os
import pytest
from unittest.mock import patch

import config


class TestConfig:
    """Test de basis Config class"""

    def test_default_secret_key_exists(self):
        assert config.Config.DEFAULT_SECRET_KEY == 'dev-secret-key-change-in-production'

    def test_default_database_path(self):
        assert config.Config.DATABASE_PATH is not None
        assert 'mvai_connexx.db' in config.Config.DATABASE_PATH

    def test_default_session_lifetime(self):
        assert config.Config.SESSION_LIFETIME_HOURS == 24

    def test_default_payment_provider(self):
        assert config.Config.PAYMENT_PROVIDER in ['gumroad', 'stripe', 'mollie']

    def test_default_openai_settings(self):
        assert config.Config.OPENAI_MODEL == 'gpt-4-turbo'
        assert config.Config.OPENAI_MAX_TOKENS == 1000
        assert 0 <= config.Config.OPENAI_TEMPERATURE <= 2.0

    def test_company_info(self):
        assert config.Config.COMPANY_NAME == 'Mind Vault AI'
        assert 'mindvault-ai.com' in config.Config.COMPANY_EMAIL

    def test_sla_targets(self):
        assert config.Config.TARGET_UPTIME_PCT == 99.9
        assert config.Config.TARGET_RESPONSE_TIME_MS == 200

    def test_valid_deployment_modes(self):
        assert config.Config.DEPLOYMENT_MODE in ['cloud', 'on-premise', 'hybrid']

    def test_rate_limiting_defaults(self):
        assert '200 per day' in config.Config.RATELIMIT_DEFAULT


class TestDevelopmentConfig:
    """Test development configuratie"""

    def test_debug_enabled(self):
        assert config.DevelopmentConfig.DEBUG is True

    def test_ip_whitelist_disabled(self):
        assert config.DevelopmentConfig.ENABLE_IP_WHITELIST is False

    def test_rate_limiting_disabled(self):
        assert config.DevelopmentConfig.RATELIMIT_ENABLED is False


class TestProductionConfig:
    """Test production configuratie"""

    def test_debug_disabled(self):
        assert config.ProductionConfig.DEBUG is False

    def test_ip_whitelist_enabled(self):
        assert config.ProductionConfig.ENABLE_IP_WHITELIST is True

    def test_threat_detection_enabled(self):
        assert config.ProductionConfig.ENABLE_THREAT_DETECTION is True

    def test_rate_limiting_enabled(self):
        assert config.ProductionConfig.RATELIMIT_ENABLED is True


class TestHybridConfig:
    """Test hybrid configuratie"""

    def test_private_network_mode(self):
        assert config.HybridConfig.PRIVATE_NETWORK_MODE == 'hybrid'

    def test_vpn_required(self):
        assert config.HybridConfig.VPN_REQUIRED is True


class TestGetConfig:
    """Test config selector"""

    @patch.dict(os.environ, {'FLASK_ENV': 'development'})
    def test_get_development_config(self):
        cfg = config.get_config()
        assert cfg == config.DevelopmentConfig

    @patch.dict(os.environ, {'FLASK_ENV': 'production'})
    def test_get_production_config(self):
        cfg = config.get_config()
        assert cfg == config.ProductionConfig

    @patch.dict(os.environ, {'FLASK_ENV': 'hybrid'})
    def test_get_hybrid_config(self):
        cfg = config.get_config()
        assert cfg == config.HybridConfig

    @patch.dict(os.environ, {'FLASK_ENV': 'unknown'})
    def test_fallback_to_development(self):
        cfg = config.get_config()
        assert cfg == config.DevelopmentConfig


class TestConfigValidator:
    """Test ConfigValidator"""

    def test_development_validation_always_passes(self):
        result = config.ConfigValidator.validate_config(
            config.DevelopmentConfig, environment='development'
        )
        assert result is True

    def test_valid_payment_providers(self):
        assert 'gumroad' in config.ConfigValidator.VALID_PAYMENT_PROVIDERS
        assert 'stripe' in config.ConfigValidator.VALID_PAYMENT_PROVIDERS
        assert 'mollie' in config.ConfigValidator.VALID_PAYMENT_PROVIDERS
        assert 'bitcoin' not in config.ConfigValidator.VALID_PAYMENT_PROVIDERS

    @patch.dict(os.environ, {'SECRET_KEY': 'dev-secret-key-change-in-production'})
    def test_production_requires_non_default_secret_key(self):
        """Production moet een niet-default SECRET_KEY hebben"""
        # Reload config to pick up the default key
        class FakeConfig:
            DEFAULT_SECRET_KEY = 'dev-secret-key-change-in-production'
            SECRET_KEY = 'dev-secret-key-change-in-production'
            PAYMENT_PROVIDER = 'gumroad'
            DOMAIN = 'test.com'
            COMPANY_EMAIL = 'test@test.com'
        with pytest.raises(ValueError, match="PRODUCTION CONFIGURATION ERROR"):
            config.ConfigValidator.validate_config(FakeConfig, environment='production')

    def test_required_production_vars_defined(self):
        assert 'SECRET_KEY' in config.ConfigValidator.REQUIRED_FOR_PRODUCTION
        assert 'DOMAIN' in config.ConfigValidator.REQUIRED_FOR_PRODUCTION
