"""
Tests voor logging_config.py - Logging module
"""
import pytest

from logging_config import LogEvents, get_logger, configure_structured_logging


class TestLogEvents:
    """Test LogEvents constanten"""

    def test_security_events_defined(self):
        assert LogEvents.LOGIN_SUCCESS == "login_success"
        assert LogEvents.LOGIN_FAILED == "login_failed"
        assert LogEvents.UNAUTHORIZED_ACCESS == "unauthorized_access"

    def test_app_lifecycle_events_defined(self):
        assert LogEvents.APP_STARTUP == "application_startup"
        assert LogEvents.APP_SHUTDOWN == "application_shutdown"

    def test_payment_events_defined(self):
        assert LogEvents.PAYMENT_INITIATED == "payment_initiated"
        assert LogEvents.PAYMENT_SUCCESS == "payment_success"
        assert LogEvents.PAYMENT_FAILED == "payment_failed"

    def test_api_events_defined(self):
        assert LogEvents.API_REQUEST == "api_request"
        assert LogEvents.API_ERROR == "api_error"

    def test_database_events_defined(self):
        assert LogEvents.DB_QUERY == "database_query"
        assert LogEvents.DB_ERROR == "database_error"


class TestGetLogger:
    """Test logger factory"""

    def test_returns_logger(self):
        logger = get_logger('test')
        assert logger is not None

    def test_default_name(self):
        logger = get_logger()
        assert logger is not None


class TestConfigureLogging:
    """Test logging configuratie"""

    def test_development_config(self):
        logger = configure_structured_logging(
            app_name='test-app',
            environment='development'
        )
        assert logger is not None

    def test_production_config(self):
        logger = configure_structured_logging(
            app_name='test-app',
            environment='production'
        )
        assert logger is not None
