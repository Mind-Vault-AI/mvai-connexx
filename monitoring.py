"""
MVAI Connexx - ICT Monitoring & Error Reporting Module
Enterprise-grade monitoring voor error tracking, alerting en exit strategies
"""
import traceback
import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional
import database as db
from collections import defaultdict

# ═══════════════════════════════════════════════════════
# ERROR SEVERITY LEVELS
# ═══════════════════════════════════════════════════════

class ErrorSeverity(Enum):
    """Error severity classificatie"""
    CRITICAL = "critical"  # System down, data loss, security breach
    HIGH = "high"          # Major functionality broken, maar system draait
    MEDIUM = "medium"      # Degraded performance, workarounds beschikbaar
    LOW = "low"            # Minor issues, geen impact op core functionaliteit
    INFO = "info"          # Informational, geen actie vereist

class IncidentStatus(Enum):
    """Incident status tracking"""
    OPEN = "open"
    INVESTIGATING = "investigating"
    MITIGATING = "mitigating"
    RESOLVED = "resolved"
    CLOSED = "closed"

# ═══════════════════════════════════════════════════════
# ERROR LOGGER
# ═══════════════════════════════════════════════════════

class ErrorLogger:
    """Centralized error logging met categorization en alerting"""

    def __init__(self):
        self.error_counts = defaultdict(int)
        self.alert_thresholds = {
            ErrorSeverity.CRITICAL: 1,   # Alert immediate
            ErrorSeverity.HIGH: 3,       # Alert after 3 occurrences
            ErrorSeverity.MEDIUM: 10,    # Alert after 10 occurrences
            ErrorSeverity.LOW: 50        # Alert after 50 occurrences
        }

    def log_error(self,
                  error_type: str,
                  message: str,
                  severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                  component: str = "unknown",
                  stack_trace: Optional[str] = None,
                  customer_id: Optional[int] = None,
                  metadata: Optional[Dict] = None) -> int:
        """
        Log een error met volledige context

        Returns:
            error_id: ID van gelogde error
        """
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO system_errors (
                    error_type, message, severity, component,
                    stack_trace, customer_id, metadata, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                error_type,
                message,
                severity.value,
                component,
                stack_trace,
                customer_id,
                json.dumps(metadata) if metadata else None
            ))
            error_id = cursor.lastrowid

        # Track error count
        self.error_counts[error_type] += 1

        # Check if alert needed
        if self._should_alert(severity):
            self._create_alert(error_id, error_type, message, severity)

        return error_id

    def _should_alert(self, severity: ErrorSeverity) -> bool:
        """Bepaal of error een alert moet triggeren"""
        # Critical errors = immediate alert
        if severity == ErrorSeverity.CRITICAL:
            return True

        # Andere severities: check threshold
        threshold = self.alert_thresholds.get(severity, 999)
        count = sum(1 for s in self.error_counts.values() if s >= threshold)

        return count > 0

    def _create_alert(self, error_id: int, error_type: str, message: str, severity: ErrorSeverity):
        """Creëer een alert voor ICT team"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ict_alerts (
                    error_id, alert_type, message, severity,
                    status, created_at, expires_at
                ) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, datetime('now', '+24 hours'))
            ''', (error_id, error_type, message, severity.value, 'open'))

    def log_exception(self,
                     exception: Exception,
                     severity: ErrorSeverity = ErrorSeverity.HIGH,
                     component: str = "unknown",
                     customer_id: Optional[int] = None) -> int:
        """
        Log een Python exception met stack trace
        """
        error_type = type(exception).__name__
        message = str(exception)
        stack_trace = ''.join(traceback.format_exception(
            type(exception), exception, exception.__traceback__
        ))

        return self.log_error(
            error_type=error_type,
            message=message,
            severity=severity,
            component=component,
            stack_trace=stack_trace,
            customer_id=customer_id
        )

# Global error logger instance
error_logger = ErrorLogger()

# ═══════════════════════════════════════════════════════
# SYSTEM HEALTH MONITOR
# ═══════════════════════════════════════════════════════

class SystemHealthMonitor:
    """Monitor systeem health metrics"""

    def __init__(self):
        self.health_checks = []

    def check_database_health(self) -> Dict:
        """Check database connectivity en performance"""
        try:
            start = datetime.now()
            with db.get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM customers')
                count = cursor.fetchone()[0]

            response_time = (datetime.now() - start).total_seconds()

            return {
                'status': 'healthy',
                'response_time_ms': response_time * 1000,
                'customer_count': count,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            error_logger.log_exception(e, ErrorSeverity.CRITICAL, 'database')
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def check_disk_space(self) -> Dict:
        """Check beschikbare disk space"""
        try:
            import shutil
            disk_path = os.environ.get('MVAI_MONITOR_DISK_PATH', '/home/user/mvai-connexx')
            stats = shutil.disk_usage(disk_path)

            total_gb = stats.total / (1024**3)
            used_gb = stats.used / (1024**3)
            free_gb = stats.free / (1024**3)
            percent_used = (stats.used / stats.total) * 100

            status = 'healthy'
            if percent_used > 90:
                status = 'critical'
                error_logger.log_error(
                    'disk_space_critical',
                    f'Disk usage at {percent_used:.1f}%',
                    ErrorSeverity.CRITICAL,
                    'system'
                )
            elif percent_used > 75:
                status = 'warning'

            return {
                'status': status,
                'total_gb': round(total_gb, 2),
                'used_gb': round(used_gb, 2),
                'free_gb': round(free_gb, 2),
                'percent_used': round(percent_used, 1)
            }
        except Exception as e:
            error_logger.log_exception(e, ErrorSeverity.HIGH, 'system')
            return {
                'status': 'unknown',
                'error': str(e)
            }

    def check_error_rates(self) -> Dict:
        """Check error rates over laatste uur"""
        try:
            with db.get_db() as conn:
                cursor = conn.cursor()

                # Errors per severity
                cursor.execute('''
                    SELECT severity, COUNT(*) as count
                    FROM system_errors
                    WHERE timestamp >= datetime('now', '-1 hour')
                    GROUP BY severity
                ''')
                errors_by_severity = {row['severity']: row['count'] for row in cursor.fetchall()}

                total_errors = sum(errors_by_severity.values())

                # Determine health status
                critical_count = errors_by_severity.get('critical', 0)
                high_count = errors_by_severity.get('high', 0)

                if critical_count > 0:
                    status = 'critical'
                elif high_count > 5:
                    status = 'degraded'
                elif total_errors > 20:
                    status = 'warning'
                else:
                    status = 'healthy'

                return {
                    'status': status,
                    'total_errors_1h': total_errors,
                    'by_severity': errors_by_severity,
                    'critical_errors': critical_count,
                    'high_errors': high_count
                }
        except Exception as e:
            error_logger.log_exception(e, ErrorSeverity.HIGH, 'monitoring')
            return {
                'status': 'unknown',
                'error': str(e)
            }

    def get_overall_health(self) -> Dict:
        """Krijg overall systeem health status"""
        db_health = self.check_database_health()
        disk_health = self.check_disk_space()
        error_health = self.check_error_rates()

        # Determine overall status
        statuses = [db_health['status'], disk_health['status'], error_health['status']]

        if 'critical' in statuses or 'unhealthy' in statuses:
            overall_status = 'critical'
        elif 'degraded' in statuses or 'warning' in statuses:
            overall_status = 'degraded'
        else:
            overall_status = 'healthy'

        # Get active alerts
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) as count, severity
                FROM ict_alerts
                WHERE status IN ('open', 'investigating')
                GROUP BY severity
            ''')
            active_alerts = {row['severity']: row['count'] for row in cursor.fetchall()}

        return {
            'overall_status': overall_status,
            'timestamp': datetime.now().isoformat(),
            'components': {
                'database': db_health,
                'disk': disk_health,
                'errors': error_health
            },
            'active_alerts': active_alerts,
            'uptime_percentage': self._calculate_uptime()
        }

    def _calculate_uptime(self) -> float:
        """Bereken uptime percentage (laatste 24 uur)"""
        try:
            with db.get_db() as conn:
                cursor = conn.cursor()

                # Count critical errors in last 24h
                cursor.execute('''
                    SELECT COUNT(*) as count
                    FROM system_errors
                    WHERE severity = 'critical'
                    AND timestamp >= datetime('now', '-24 hours')
                ''')
                critical_errors = cursor.fetchone()['count']

                # Assume each critical error = 5 min downtime
                downtime_minutes = critical_errors * 5
                total_minutes = 24 * 60
                uptime_minutes = total_minutes - downtime_minutes

                uptime_percentage = (uptime_minutes / total_minutes) * 100

                return max(0, min(100, round(uptime_percentage, 2)))
        except Exception:
            return 99.9  # Default

# Global health monitor
health_monitor = SystemHealthMonitor()

# ═══════════════════════════════════════════════════════
# ALERT MANAGEMENT
# ═══════════════════════════════════════════════════════

def get_active_alerts() -> List[Dict]:
    """Haal alle actieve alerts op"""
    with db.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, e.component, e.stack_trace
            FROM ict_alerts a
            LEFT JOIN system_errors e ON a.error_id = e.id
            WHERE a.status IN ('open', 'investigating', 'mitigating')
            AND a.expires_at > datetime('now')
            ORDER BY
                CASE a.severity
                    WHEN 'critical' THEN 1
                    WHEN 'high' THEN 2
                    WHEN 'medium' THEN 3
                    ELSE 4
                END,
                a.created_at DESC
        ''')
        return [dict(row) for row in cursor.fetchall()]

def acknowledge_alert(alert_id: int, admin_username: str) -> bool:
    """Acknowledge een alert"""
    try:
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE ict_alerts
                SET status = 'investigating',
                    acknowledged_by = ?,
                    acknowledged_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (admin_username, alert_id))
        return True
    except Exception as e:
        error_logger.log_exception(e, ErrorSeverity.MEDIUM, 'monitoring')
        return False

def resolve_alert(alert_id: int, admin_username: str, resolution_notes: str) -> bool:
    """Resolve een alert"""
    try:
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE ict_alerts
                SET status = 'resolved',
                    resolved_by = ?,
                    resolved_at = CURRENT_TIMESTAMP,
                    resolution_notes = ?
                WHERE id = ?
            ''', (admin_username, resolution_notes, alert_id))
        return True
    except Exception as e:
        error_logger.log_exception(e, ErrorSeverity.MEDIUM, 'monitoring')
        return False

# ═══════════════════════════════════════════════════════
# ERROR ANALYTICS
# ═══════════════════════════════════════════════════════

def get_error_analytics(days: int = 7) -> Dict:
    """Krijg error analytics over periode"""
    with db.get_db() as conn:
        cursor = conn.cursor()

        # Errors per dag
        cursor.execute('''
            SELECT
                DATE(timestamp) as date,
                severity,
                COUNT(*) as count
            FROM system_errors
            WHERE timestamp >= datetime('now', ?)
            GROUP BY DATE(timestamp), severity
            ORDER BY date DESC
        ''', (f'-{days} days',))

        daily_errors = defaultdict(lambda: defaultdict(int))
        for row in cursor.fetchall():
            daily_errors[row['date']][row['severity']] = row['count']

        # Top error types
        cursor.execute('''
            SELECT error_type, COUNT(*) as count, severity
            FROM system_errors
            WHERE timestamp >= datetime('now', ?)
            GROUP BY error_type, severity
            ORDER BY count DESC
            LIMIT 10
        ''', (f'-{days} days',))
        top_errors = [dict(row) for row in cursor.fetchall()]

        # Errors per component
        cursor.execute('''
            SELECT component, COUNT(*) as count, severity
            FROM system_errors
            WHERE timestamp >= datetime('now', ?)
            GROUP BY component, severity
            ORDER BY count DESC
        ''', (f'-{days} days',))
        component_errors = [dict(row) for row in cursor.fetchall()]

        # Mean Time To Resolve (MTTR)
        cursor.execute('''
            SELECT
                AVG(
                    CAST((julianday(resolved_at) - julianday(created_at)) * 24 * 60 AS INTEGER)
                ) as mttr_minutes
            FROM ict_alerts
            WHERE resolved_at IS NOT NULL
            AND created_at >= datetime('now', ?)
        ''', (f'-{days} days',))
        mttr_row = cursor.fetchone()
        mttr_minutes = mttr_row['mttr_minutes'] if mttr_row and mttr_row['mttr_minutes'] else 0

        return {
            'daily_errors': dict(daily_errors),
            'top_errors': top_errors,
            'component_errors': component_errors,
            'mttr_minutes': round(mttr_minutes, 1),
            'period_days': days
        }

# ═══════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════

def get_recent_errors(limit: int = 50, severity: Optional[str] = None) -> List[Dict]:
    """Haal recente errors op"""
    with db.get_db() as conn:
        cursor = conn.cursor()

        query = '''
            SELECT * FROM system_errors
            WHERE 1=1
        '''
        params = []

        if severity:
            query += ' AND severity = ?'
            params.append(severity)

        query += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def cleanup_old_errors(days: int = 90):
    """Cleanup oude errors (retention policy)"""
    with db.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM system_errors
            WHERE timestamp < datetime('now', ?)
            AND severity NOT IN ('critical', 'high')
        ''', (f'-{days} days',))
        deleted = cursor.rowcount

    return deleted

if __name__ == '__main__':
    print("✓ ICT Monitoring Module loaded")
    print(f"✓ Health Status: {health_monitor.get_overall_health()['overall_status']}")
