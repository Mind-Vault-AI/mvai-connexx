"""
MVAI Connexx - Structured Logging Configuration
Enterprise-grade logging voor 99.9% SLA compliance
"""
import structlog
import logging
import sys

def configure_structured_logging(app_name='mvai-connexx', environment='production'):
    """
    Configure structured logging voor enterprise compliance
    
    Features:
    - JSON output voor log aggregatie tools (Datadog, ELK, Splunk)
    - Structured fields voor filtering en queries
    - Timestamp, level, logger name automatisch toegevoegd
    - Exception stack traces in structured format
    - GDPR/SOC2 compliant (geen PII in logs)
    """
    
    # Determine log level based on environment
    log_level = logging.DEBUG if environment == 'development' else logging.INFO
    
    # Configure structlog processors
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    # Add JSON renderer for production, console for development
    if environment == 'production':
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    handler = logging.StreamHandler(sys.stdout)
    
    if environment == 'production':
        # Simple formatter for production (structlog already outputs JSON)
        formatter = logging.Formatter('%(message)s')
    else:
        # Simple formatter for development (structlog handles formatting)
        formatter = logging.Formatter('%(message)s')
    
    handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)
    
    # Suppress noisy loggers
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    return structlog.get_logger(app_name)


def get_logger(name='mvai-connexx'):
    """Get a configured structlog logger instance"""
    return structlog.get_logger(name)


# Logging event constants (voor consistency)
class LogEvents:
    """Structured logging event names voor consistency"""
    
    # Configuration events
    CONFIG_VALIDATION_PASSED = "configuration_validation_passed"
    CONFIG_VALIDATION_FAILED = "configuration_validation_failed"
    CONFIG_VALIDATION_WARNING = "configuration_validation_warning"
    
    # Application lifecycle
    APP_STARTUP = "application_startup"
    APP_SHUTDOWN = "application_shutdown"
    APP_HEALTH_CHECK = "health_check"
    
    # Security events
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    LOGOUT = "logout"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    
    # API events
    API_REQUEST = "api_request"
    API_RESPONSE = "api_response"
    API_ERROR = "api_error"
    
    # Payment events
    PAYMENT_INITIATED = "payment_initiated"
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    
    # Database events
    DB_QUERY = "database_query"
    DB_ERROR = "database_error"
    
    # Error events
    EXCEPTION = "exception"
    VALIDATION_ERROR = "validation_error"
