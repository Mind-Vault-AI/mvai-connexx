"""
MVAI Connexx - Incident Response & Exit Strategy Module
Emergency response procedures voor security breaches en system failures
"""
import os
import json
import shutil
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
import database as db
from monitoring import error_logger, ErrorSeverity

# ═══════════════════════════════════════════════════════
# INCIDENT TYPES & PLAYBOOKS
# ═══════════════════════════════════════════════════════

class IncidentType(Enum):
    """Incident categorieën"""
    SECURITY_BREACH = "security_breach"        # Hacker attack, data breach
    DDOS_ATTACK = "ddos_attack"                # DDoS / flooding attack
    DATA_CORRUPTION = "data_corruption"        # Database corruption
    SYSTEM_DOWN = "system_down"                # Complete system failure
    PERFORMANCE_DEGRADATION = "perf_degradation"  # Extreme slowdown
    UNAUTHORIZED_ACCESS = "unauthorized_access"    # Suspicious access patterns
    DATA_LEAK = "data_leak"                    # Data exfiltration detected

class IncidentSeverity(Enum):
    """Incident severity levels"""
    P0 = "p0"  # Critical - System down, active attack
    P1 = "p1"  # High - Major functionality broken
    P2 = "p2"  # Medium - Degraded service
    P3 = "p3"  # Low - Minor issue

class ResponseAction(Enum):
    """Automated response actions"""
    BLOCK_IP = "block_ip"
    ENABLE_MAINTENANCE_MODE = "maintenance_mode"
    BACKUP_DATABASE = "backup_database"
    SHUTDOWN_SYSTEM = "shutdown_system"
    ISOLATE_CUSTOMER = "isolate_customer"
    RATE_LIMIT_STRICT = "rate_limit_strict"
    ALERT_ADMIN = "alert_admin"
    SNAPSHOT_STATE = "snapshot_state"

# ═══════════════════════════════════════════════════════
# INCIDENT RESPONSE MANAGER
# ═══════════════════════════════════════════════════════

class IncidentResponseManager:
    """Centralized incident response orchestration"""

    def __init__(self):
        self.active_incidents = {}
        self.playbooks = self._load_playbooks()
        self.maintenance_mode = False

    def _load_playbooks(self) -> Dict:
        """Load incident response playbooks"""
        return {
            IncidentType.SECURITY_BREACH: {
                'severity': IncidentSeverity.P0,
                'actions': [
                    ResponseAction.SNAPSHOT_STATE,
                    ResponseAction.BLOCK_IP,
                    ResponseAction.BACKUP_DATABASE,
                    ResponseAction.ALERT_ADMIN,
                    ResponseAction.ENABLE_MAINTENANCE_MODE
                ],
                'escalation_time_minutes': 5,
                'description': 'Security breach detected - immediate lockdown'
            },
            IncidentType.DDOS_ATTACK: {
                'severity': IncidentSeverity.P0,
                'actions': [
                    ResponseAction.RATE_LIMIT_STRICT,
                    ResponseAction.BLOCK_IP,
                    ResponseAction.ALERT_ADMIN
                ],
                'escalation_time_minutes': 10,
                'description': 'DDoS attack - enable aggressive rate limiting'
            },
            IncidentType.DATA_CORRUPTION: {
                'severity': IncidentSeverity.P0,
                'actions': [
                    ResponseAction.SHUTDOWN_SYSTEM,
                    ResponseAction.BACKUP_DATABASE,
                    ResponseAction.ALERT_ADMIN
                ],
                'escalation_time_minutes': 0,  # Immediate escalation
                'description': 'Data corruption detected - emergency shutdown'
            },
            IncidentType.SYSTEM_DOWN: {
                'severity': IncidentSeverity.P0,
                'actions': [
                    ResponseAction.ALERT_ADMIN,
                    ResponseAction.SNAPSHOT_STATE
                ],
                'escalation_time_minutes': 2,
                'description': 'System down - immediate attention required'
            },
            IncidentType.UNAUTHORIZED_ACCESS: {
                'severity': IncidentSeverity.P1,
                'actions': [
                    ResponseAction.BLOCK_IP,
                    ResponseAction.ISOLATE_CUSTOMER,
                    ResponseAction.ALERT_ADMIN
                ],
                'escalation_time_minutes': 15,
                'description': 'Unauthorized access attempt detected'
            },
            IncidentType.DATA_LEAK: {
                'severity': IncidentSeverity.P0,
                'actions': [
                    ResponseAction.BLOCK_IP,
                    ResponseAction.ENABLE_MAINTENANCE_MODE,
                    ResponseAction.SNAPSHOT_STATE,
                    ResponseAction.ALERT_ADMIN
                ],
                'escalation_time_minutes': 5,
                'description': 'Data exfiltration detected - emergency lockdown'
            }
        }

    def create_incident(self,
                       incident_type: IncidentType,
                       description: str,
                       metadata: Optional[Dict] = None,
                       auto_respond: bool = True) -> int:
        """
        Creëer een incident en trigger automated response

        Args:
            incident_type: Type van incident
            description: Beschrijving van wat er gebeurd is
            metadata: Extra context (IP addresses, customer_id, etc.)
            auto_respond: Trigger automatische response acties

        Returns:
            incident_id: ID van gecreëerde incident
        """
        playbook = self.playbooks.get(incident_type)

        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO incidents (
                    incident_type, severity, description, metadata,
                    status, created_at
                ) VALUES (?, ?, ?, ?, 'open', CURRENT_TIMESTAMP)
            ''', (
                incident_type.value,
                playbook['severity'].value if playbook else 'p2',
                description,
                json.dumps(metadata) if metadata else None
            ))
            incident_id = cursor.lastrowid

        # Log in error system
        error_logger.log_error(
            error_type=f'INCIDENT_{incident_type.value.upper()}',
            message=description,
            severity=ErrorSeverity.CRITICAL,
            component='incident_response',
            metadata=metadata
        )

        # Store in active incidents
        self.active_incidents[incident_id] = {
            'type': incident_type,
            'created': datetime.now(),
            'playbook': playbook
        }

        # Execute automated response
        if auto_respond and playbook:
            self._execute_playbook(incident_id, playbook, metadata)

        return incident_id

    def _execute_playbook(self, incident_id: int, playbook: Dict, metadata: Optional[Dict]):
        """Execute incident response playbook"""
        actions_taken = []

        for action in playbook['actions']:
            success = self._execute_action(action, metadata)
            actions_taken.append({
                'action': action.value,
                'success': success,
                'timestamp': datetime.now().isoformat()
            })

        # Save actions to database
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE incidents
                SET response_actions = ?
                WHERE id = ?
            ''', (json.dumps(actions_taken), incident_id))

    def _execute_action(self, action: ResponseAction, metadata: Optional[Dict]) -> bool:
        """Execute single response action"""
        try:
            if action == ResponseAction.BLOCK_IP:
                return self._block_ip(metadata.get('ip_address') if metadata else None)

            elif action == ResponseAction.ENABLE_MAINTENANCE_MODE:
                return self._enable_maintenance_mode()

            elif action == ResponseAction.BACKUP_DATABASE:
                return self._emergency_backup()

            elif action == ResponseAction.SHUTDOWN_SYSTEM:
                return self._shutdown_system()

            elif action == ResponseAction.ISOLATE_CUSTOMER:
                return self._isolate_customer(metadata.get('customer_id') if metadata else None)

            elif action == ResponseAction.RATE_LIMIT_STRICT:
                return self._enable_strict_rate_limiting()

            elif action == ResponseAction.ALERT_ADMIN:
                return self._send_admin_alert(metadata)

            elif action == ResponseAction.SNAPSHOT_STATE:
                return self._snapshot_system_state()

            return False

        except Exception as e:
            error_logger.log_exception(e, ErrorSeverity.HIGH, 'incident_response')
            return False

    def _block_ip(self, ip_address: Optional[str]) -> bool:
        """Block IP address"""
        if not ip_address:
            return False

        try:
            from security import security_manager
            security_manager.add_to_blacklist(
                ip_address,
                'Incident response - automatic block',
                duration_hours=168  # 7 days
            )
            return True
        except:
            return False

    def _enable_maintenance_mode(self) -> bool:
        """Enable maintenance mode"""
        self.maintenance_mode = True

        # Create maintenance flag file
        try:
            with open('/tmp/mvai_maintenance_mode', 'w') as f:
                f.write(json.dumps({
                    'enabled': True,
                    'enabled_at': datetime.now().isoformat(),
                    'reason': 'Incident response - security measure'
                }))
            return True
        except:
            return False

    def _emergency_backup(self) -> bool:
        """Create emergency database backup"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # Determine database path from environment or fall back to default
            db_path = os.getenv('DATABASE_PATH', '/home/user/mvai-connexx/mvai_connexx.db')
            db_dir = os.path.dirname(db_path) or '.'

            # Backups directory relative to database location
            backups_dir = os.path.join(db_dir, 'backups')
            backup_path = os.path.join(backups_dir, f'emergency_backup_{timestamp}.db')

            # Ensure backups directory exists
            os.makedirs(backups_dir, exist_ok=True)

            # Copy database file
            shutil.copy2(
                db_path,
                backup_path
            )
            return True
        except Exception as e:
            error_logger.log_exception(e, ErrorSeverity.CRITICAL, 'backup')
            return False

    def _shutdown_system(self) -> bool:
        """Graceful system shutdown (creates shutdown flag)"""
        try:
            with open('/tmp/mvai_shutdown_requested', 'w') as f:
                f.write(json.dumps({
                    'shutdown': True,
                    'requested_at': datetime.now().isoformat(),
                    'reason': 'Incident response - data protection'
                }))
            return True
        except:
            return False

    def _isolate_customer(self, customer_id: Optional[int]) -> bool:
        """Isolate customer account (disable access)"""
        if not customer_id:
            return False

        try:
            with db.get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE customers
                    SET status = 'suspended',
                        suspended_reason = 'Incident response - security measure'
                    WHERE id = ?
                ''', (customer_id,))
            return True
        except:
            return False

    def _enable_strict_rate_limiting(self) -> bool:
        """Enable strict rate limiting"""
        try:
            with open('/tmp/mvai_strict_rate_limit', 'w') as f:
                f.write(json.dumps({
                    'enabled': True,
                    'limits': {
                        'requests_per_minute': 10,
                        'requests_per_hour': 100
                    },
                    'enabled_at': datetime.now().isoformat()
                }))
            return True
        except:
            return False

    def _send_admin_alert(self, metadata: Optional[Dict]) -> bool:
        """Send alert to admin (log in database)"""
        try:
            from monitoring import error_logger, ErrorSeverity
            error_logger.log_error(
                error_type='ADMIN_ALERT',
                message='Incident response - immediate attention required',
                severity=ErrorSeverity.CRITICAL,
                component='incident_response',
                metadata=metadata
            )
            return True
        except:
            return False

    def _snapshot_system_state(self) -> bool:
        """Create snapshot of current system state"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            snapshot_path = f'/tmp/mvai_snapshot_{timestamp}.json'

            # Collect system state
            from monitoring import health_monitor
            state = {
                'timestamp': datetime.now().isoformat(),
                'health': health_monitor.get_overall_health(),
                'active_incidents': len(self.active_incidents),
                'maintenance_mode': self.maintenance_mode
            }

            with open(snapshot_path, 'w') as f:
                json.dump(state, f, indent=2)

            return True
        except:
            return False

    def resolve_incident(self, incident_id: int, resolution_notes: str, resolved_by: str) -> bool:
        """Resolve an incident"""
        try:
            with db.get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE incidents
                    SET status = 'resolved',
                        resolved_at = CURRENT_TIMESTAMP,
                        resolved_by = ?,
                        resolution_notes = ?
                    WHERE id = ?
                ''', (resolved_by, resolution_notes, incident_id))

            # Remove from active incidents
            if incident_id in self.active_incidents:
                del self.active_incidents[incident_id]

            return True
        except Exception as e:
            error_logger.log_exception(e, ErrorSeverity.MEDIUM, 'incident_response')
            return False

    def get_active_incidents(self) -> List[Dict]:
        """Get all active incidents"""
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM incidents
                WHERE status IN ('open', 'investigating', 'mitigating')
                ORDER BY
                    CASE severity
                        WHEN 'p0' THEN 1
                        WHEN 'p1' THEN 2
                        WHEN 'p2' THEN 3
                        ELSE 4
                    END,
                    created_at DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]

# Global incident manager
incident_manager = IncidentResponseManager()

# ═══════════════════════════════════════════════════════
# EXIT STRATEGY FUNCTIONS
# ═══════════════════════════════════════════════════════

def execute_emergency_exit_strategy(reason: str) -> Dict:
    """
    Execute complete emergency exit strategy
    - Backup alle data
    - Enable maintenance mode
    - Block all traffic
    - Alert admins
    """
    actions = []

    # 1. Create emergency backup
    backup_success = incident_manager._emergency_backup()
    actions.append({'action': 'emergency_backup', 'success': backup_success})

    # 2. Enable maintenance mode
    maintenance_success = incident_manager._enable_maintenance_mode()
    actions.append({'action': 'maintenance_mode', 'success': maintenance_success})

    # 3. Create system snapshot
    snapshot_success = incident_manager._snapshot_system_state()
    actions.append({'action': 'snapshot', 'success': snapshot_success})

    # 4. Log incident
    incident_id = incident_manager.create_incident(
        IncidentType.SYSTEM_DOWN,
        f'Emergency exit strategy executed: {reason}',
        metadata={'reason': reason},
        auto_respond=False
    )
    actions.append({'action': 'log_incident', 'success': True, 'incident_id': incident_id})

    return {
        'exit_strategy_executed': True,
        'timestamp': datetime.now().isoformat(),
        'reason': reason,
        'actions': actions,
        'incident_id': incident_id
    }

def check_maintenance_mode() -> bool:
    """Check if system is in maintenance mode"""
    try:
        if os.path.exists('/tmp/mvai_maintenance_mode'):
            with open('/tmp/mvai_maintenance_mode', 'r') as f:
                data = json.load(f)
                return data.get('enabled', False)
    except Exception:
        # Fail-safe: on any error while reading/parsing the maintenance file,
        # treat maintenance mode as disabled and return False below.
        pass
    return False

def disable_maintenance_mode() -> bool:
    """Disable maintenance mode"""
    try:
        if os.path.exists('/tmp/mvai_maintenance_mode'):
            os.remove('/tmp/mvai_maintenance_mode')
        incident_manager.maintenance_mode = False
        return True
    except:
        return False

# ═══════════════════════════════════════════════════════
# INCIDENT ANALYTICS
# ═══════════════════════════════════════════════════════

def get_incident_analytics(days: int = 30) -> Dict:
    """Get incident analytics"""
    with db.get_db() as conn:
        cursor = conn.cursor()

        # Incidents by type
        cursor.execute('''
            SELECT incident_type, COUNT(*) as count
            FROM incidents
            WHERE created_at >= datetime('now', ?)
            GROUP BY incident_type
            ORDER BY count DESC
        ''', (f'-{days} days',))
        by_type = [dict(row) for row in cursor.fetchall()]

        # Incidents by severity
        cursor.execute('''
            SELECT severity, COUNT(*) as count
            FROM incidents
            WHERE created_at >= datetime('now', ?)
            GROUP BY severity
            ORDER BY
                CASE severity
                    WHEN 'p0' THEN 1
                    WHEN 'p1' THEN 2
                    WHEN 'p2' THEN 3
                    ELSE 4
                END
        ''', (f'-{days} days',))
        by_severity = [dict(row) for row in cursor.fetchall()]

        # Mean Time To Resolve
        cursor.execute('''
            SELECT
                AVG(
                    CAST((julianday(resolved_at) - julianday(created_at)) * 24 * 60 AS INTEGER)
                ) as mttr_minutes
            FROM incidents
            WHERE resolved_at IS NOT NULL
            AND created_at >= datetime('now', ?)
        ''', (f'-{days} days',))
        mttr_row = cursor.fetchone()
        mttr = mttr_row['mttr_minutes'] if mttr_row and mttr_row['mttr_minutes'] else 0

        # Total incidents
        cursor.execute('''
            SELECT COUNT(*) as total FROM incidents
            WHERE created_at >= datetime('now', ?)
        ''', (f'-{days} days',))
        total = cursor.fetchone()['total']

        return {
            'total_incidents': total,
            'by_type': by_type,
            'by_severity': by_severity,
            'mttr_minutes': round(mttr, 1),
            'period_days': days
        }

if __name__ == '__main__':
    print("✓ Incident Response Module loaded")
    print(f"✓ Active Incidents: {len(incident_manager.get_active_incidents())}")
    print(f"✓ Maintenance Mode: {check_maintenance_mode()}")
