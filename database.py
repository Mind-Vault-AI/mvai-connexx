"""
MVAI Connexx - Database Module
Multi-tenant SQLite database voor klantgegevens en logs
"""
import sqlite3
import secrets
import hashlib
import time
import functools
from datetime import datetime
from contextlib import contextmanager

DATABASE = 'mvai_connexx.db'

def retry_on_locked(max_retries=5, initial_delay=0.1):
    """
    Decorator to retry database operations on SQLITE_BUSY errors.
    Uses exponential backoff to handle concurrent access gracefully.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    error_msg = str(e).lower()
                    # Check for specific SQLite lock-related errors
                    is_locked = any(phrase in error_msg for phrase in [
                        'database is locked',
                        'table is locked',
                        'database table is locked'
                    ])
                    
                    if is_locked and attempt < max_retries - 1:
                        time.sleep(delay)
                        delay *= 2  # Exponential backoff
                    else:
                        raise
        return wrapper
    return decorator

@contextmanager
def get_db():
    """Context manager voor database connecties met WAL mode en timeouts"""
    conn = sqlite3.connect(DATABASE, timeout=30)
    conn.row_factory = sqlite3.Row
    
    # Enable WAL mode for better concurrency
    conn.execute('PRAGMA journal_mode=WAL')
    # Set busy timeout to 5 seconds
    conn.execute('PRAGMA busy_timeout=5000')
    # Use NORMAL synchronous mode for better performance
    conn.execute('PRAGMA synchronous=NORMAL')
    
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Initialiseer database met multi-tenant schema"""
    with get_db() as conn:
        cursor = conn.cursor()

        # Customers tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                access_code TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',
                contact_email TEXT,
                company_info TEXT,
                ai_assistant_enabled BOOLEAN DEFAULT 0
            )
        ''')

        # Logs tabel met foreign key naar customers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                ip_address TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data TEXT NOT NULL,
                metadata TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')

        # Admin users tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                access_code TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Audit logs tabel voor admin acties
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_username TEXT NOT NULL,
                action TEXT NOT NULL,
                target_type TEXT,
                target_id INTEGER,
                details TEXT,
                ip_address TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # API keys tabel voor programmatic access
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                key_value TEXT NOT NULL UNIQUE,
                name TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used_at TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')

        # IP Whitelist tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ip_whitelist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT NOT NULL UNIQUE,
                reason TEXT,
                added_by TEXT,
                is_active BOOLEAN DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # IP Blacklist tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ip_blacklist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT NOT NULL,
                reason TEXT,
                added_by TEXT,
                is_active BOOLEAN DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP
            )
        ''')

        # Security incidents tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT NOT NULL,
                incident_type TEXT NOT NULL,
                details TEXT,
                severity TEXT DEFAULT 'low',
                user_agent TEXT,
                request_path TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Private network access tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS private_networks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network_cidr TEXT NOT NULL UNIQUE,
                customer_id INTEGER,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')

        # AI Assistant preferences per klant
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_assistant_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL UNIQUE,
                language TEXT DEFAULT 'nl',
                tone TEXT DEFAULT 'professional',
                proactive_suggestions BOOLEAN DEFAULT 1,
                auto_reports BOOLEAN DEFAULT 0,
                notifications_enabled BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')

        # AI Learning data per klant (geïsoleerd)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_learning (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                command TEXT NOT NULL,
                result_type TEXT,
                success BOOLEAN DEFAULT 1,
                feedback TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')

        # AI Generated reports
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_generated_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')

        # AI Conversations (chat history)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                intent TEXT,
                success BOOLEAN DEFAULT 1,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')

        # ═══════════════════════════════════════════════════════
        # ICT MONITORING & ERROR REPORTING TABLES
        # ═══════════════════════════════════════════════════════

        # System errors tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_type TEXT NOT NULL,
                message TEXT NOT NULL,
                severity TEXT NOT NULL,
                component TEXT,
                stack_trace TEXT,
                customer_id INTEGER,
                metadata TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')

        # ICT Alerts tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ict_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_id INTEGER,
                alert_type TEXT NOT NULL,
                message TEXT NOT NULL,
                severity TEXT NOT NULL,
                status TEXT DEFAULT 'open',
                acknowledged_by TEXT,
                acknowledged_at TIMESTAMP,
                resolved_by TEXT,
                resolved_at TIMESTAMP,
                resolution_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (error_id) REFERENCES system_errors(id)
            )
        ''')

        # ═══════════════════════════════════════════════════════
        # INCIDENT RESPONSE TABLES
        # ═══════════════════════════════════════════════════════

        # Incidents tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                metadata TEXT,
                status TEXT DEFAULT 'open',
                response_actions TEXT,
                resolved_by TEXT,
                resolved_at TIMESTAMP,
                resolution_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # ═══════════════════════════════════════════════════════
        # LEAN SIX SIGMA TABLES
        # ═══════════════════════════════════════════════════════

        # DMAIC Projects tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dmaic_projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                problem_statement TEXT NOT NULL,
                goal TEXT NOT NULL,
                current_phase TEXT DEFAULT 'define',
                owner TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                results_summary TEXT,
                improvements_achieved TEXT,
                target_completion_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')

        # DMAIC Measurements tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dmaic_measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                notes TEXT,
                measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES dmaic_projects(id)
            )
        ''')

        # DMAIC Phase Logs tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dmaic_phase_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                phase TEXT NOT NULL,
                notes TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES dmaic_projects(id)
            )
        ''')

        # ═══════════════════════════════════════════════════════
        # MARKETING INTELLIGENCE TABLES
        # ═══════════════════════════════════════════════════════

        # Marketing Campaigns tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS marketing_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                channel TEXT NOT NULL,
                cost REAL DEFAULT 0,
                conversions INTEGER DEFAULT 0,
                converted BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Marketing Funnel tabel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS marketing_funnel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                funnel_stage TEXT NOT NULL,
                customer_id INTEGER,
                campaign_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (campaign_id) REFERENCES marketing_campaigns(id)
            )
        ''')

        # ═══════════════════════════════════════════════════════
        # ADDITIONAL CUSTOMER FIELDS FOR UNIT ECONOMICS
        # ═══════════════════════════════════════════════════════

        # Add pricing_tier column if not exists (for unit economics)
        cursor.execute("SELECT COUNT(*) FROM pragma_table_info('customers') WHERE name='pricing_tier'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("ALTER TABLE customers ADD COLUMN pricing_tier TEXT DEFAULT 'starter'")

        # Add suspended_reason column if not exists
        cursor.execute("SELECT COUNT(*) FROM pragma_table_info('customers') WHERE name='suspended_reason'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("ALTER TABLE customers ADD COLUMN suspended_reason TEXT")

        # Add updated_at column if not exists
        cursor.execute("SELECT COUNT(*) FROM pragma_table_info('customers') WHERE name='updated_at'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("ALTER TABLE customers ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

        # Add usage_count to api_keys if not exists
        cursor.execute("SELECT COUNT(*) FROM pragma_table_info('api_keys') WHERE name='usage_count'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("ALTER TABLE api_keys ADD COLUMN usage_count INTEGER DEFAULT 0")

        # Indices voor performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_customer ON logs(customer_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_customers_code ON customers(access_code)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_api_keys_value ON api_keys(key_value)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_security_incidents_ip ON security_incidents(ip_address)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_security_incidents_timestamp ON security_incidents(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ip_whitelist_ip ON ip_whitelist(ip_address)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ip_blacklist_ip ON ip_blacklist(ip_address)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ai_learning_customer ON ai_learning(customer_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ai_conversations_customer ON ai_conversations(customer_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ai_reports_customer ON ai_generated_reports(customer_id)')

        # Indices for new enterprise tables
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_system_errors_severity ON system_errors(severity)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_system_errors_component ON system_errors(component)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_system_errors_timestamp ON system_errors(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ict_alerts_status ON ict_alerts(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ict_alerts_severity ON ict_alerts(severity)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_incidents_type ON incidents(incident_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_dmaic_status ON dmaic_projects(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_dmaic_phase ON dmaic_projects(current_phase)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_marketing_channel ON marketing_campaigns(channel)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_funnel_stage ON marketing_funnel(funnel_stage)')

        conn.commit()

def generate_access_code(length=16):
    """Genereer veilige access code"""
    return secrets.token_urlsafe(length)

def hash_access_code(code):
    """Hash access code voor veilige opslag"""
    return hashlib.sha256(code.encode()).hexdigest()

# Customer functies
@retry_on_locked()
def create_customer(name, contact_email=None, company_info=None):
    """Maak nieuwe klant aan met unieke access code"""
    access_code = generate_access_code()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customers (name, access_code, contact_email, company_info)
            VALUES (?, ?, ?, ?)
        ''', (name, access_code, contact_email, company_info))
        customer_id = cursor.lastrowid

    return {
        'id': customer_id,
        'name': name,
        'access_code': access_code,
        'contact_email': contact_email
    }

def get_customer_by_code(access_code):
    """Haal klant op via access code"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE access_code = ? AND status = "active"', (access_code,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_customer_by_id(customer_id):
    """Haal klant op via ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_customers():
    """Haal alle klanten op (admin functie)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers ORDER BY created_at DESC')
        return [dict(row) for row in cursor.fetchall()]

@retry_on_locked()
def update_customer_status(customer_id, status):
    """Update klant status"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE customers SET status = ? WHERE id = ?', (status, customer_id))

# Log functies
@retry_on_locked()
def create_log(customer_id, ip_address, data, metadata=None):
    """Maak nieuwe log entry voor klant"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO logs (customer_id, ip_address, data, metadata)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, ip_address, data, metadata))
        return cursor.lastrowid

def get_customer_logs(customer_id, limit=100, offset=0):
    """Haal logs op voor specifieke klant"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM logs
            WHERE customer_id = ?
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        ''', (customer_id, limit, offset))
        return [dict(row) for row in cursor.fetchall()]

def get_all_logs(limit=100, offset=0):
    """Haal alle logs op (admin functie)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT l.*, c.name as customer_name
            FROM logs l
            JOIN customers c ON l.customer_id = c.id
            ORDER BY l.timestamp DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))
        return [dict(row) for row in cursor.fetchall()]

def get_customer_stats(customer_id):
    """Haal statistieken op voor klant"""
    with get_db() as conn:
        cursor = conn.cursor()

        # Totaal aantal logs
        cursor.execute('SELECT COUNT(*) as total FROM logs WHERE customer_id = ?', (customer_id,))
        total_logs = cursor.fetchone()['total']

        # Eerste log datum
        cursor.execute('SELECT MIN(timestamp) as first_log FROM logs WHERE customer_id = ?', (customer_id,))
        first_log = cursor.fetchone()['first_log']

        # Laatste log datum
        cursor.execute('SELECT MAX(timestamp) as last_log FROM logs WHERE customer_id = ?', (customer_id,))
        last_log = cursor.fetchone()['last_log']

        # Logs vandaag
        cursor.execute('''
            SELECT COUNT(*) as today
            FROM logs
            WHERE customer_id = ?
            AND DATE(timestamp) = DATE('now')
        ''', (customer_id,))
        logs_today = cursor.fetchone()['today']

        # Logs deze week
        cursor.execute('''
            SELECT COUNT(*) as week
            FROM logs
            WHERE customer_id = ?
            AND timestamp >= DATE('now', '-7 days')
        ''', (customer_id,))
        logs_week = cursor.fetchone()['week']

        return {
            'total_logs': total_logs,
            'first_log': first_log,
            'last_log': last_log,
            'logs_today': logs_today,
            'logs_week': logs_week
        }

def get_admin_stats():
    """Haal globale statistieken op (admin functie)"""
    with get_db() as conn:
        cursor = conn.cursor()

        # Totaal aantal klanten
        cursor.execute('SELECT COUNT(*) as total FROM customers WHERE status = "active"')
        total_customers = cursor.fetchone()['total']

        # Totaal aantal logs
        cursor.execute('SELECT COUNT(*) as total FROM logs')
        total_logs = cursor.fetchone()['total']

        # Logs vandaag
        cursor.execute('SELECT COUNT(*) as today FROM logs WHERE DATE(timestamp) = DATE("now")')
        logs_today = cursor.fetchone()['today']

        # Top 5 klanten
        cursor.execute('''
            SELECT c.name, COUNT(l.id) as log_count
            FROM customers c
            LEFT JOIN logs l ON c.id = l.customer_id
            WHERE c.status = "active"
            GROUP BY c.id
            ORDER BY log_count DESC
            LIMIT 5
        ''')
        top_customers = [dict(row) for row in cursor.fetchall()]

        return {
            'total_customers': total_customers,
            'total_logs': total_logs,
            'logs_today': logs_today,
            'top_customers': top_customers
        }

# Admin functies
@retry_on_locked()
def create_admin(username, password=None):
    """Maak admin gebruiker aan"""
    access_code = password if password else generate_access_code(24)

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO admins (username, access_code)
            VALUES (?, ?)
        ''', (username, access_code))

    return {
        'username': username,
        'access_code': access_code
    }

def verify_admin(access_code):
    """Verifieer admin access code"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admins WHERE access_code = ?', (access_code,))
        row = cursor.fetchone()
        return dict(row) if row else None

def search_customers(query):
    """Zoek klanten op naam (admin functie)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM customers
            WHERE name LIKE ?
            ORDER BY name
        ''', (f'%{query}%',))
        return [dict(row) for row in cursor.fetchall()]

def search_logs(query, customer_id=None):
    """Zoek logs op data inhoud"""
    with get_db() as conn:
        cursor = conn.cursor()
        if customer_id:
            cursor.execute('''
                SELECT * FROM logs
                WHERE customer_id = ? AND data LIKE ?
                ORDER BY timestamp DESC
                LIMIT 50
            ''', (customer_id, f'%{query}%'))
        else:
            cursor.execute('''
                SELECT l.*, c.name as customer_name
                FROM logs l
                JOIN customers c ON l.customer_id = c.id
                WHERE l.data LIKE ?
                ORDER BY l.timestamp DESC
                LIMIT 50
            ''', (f'%{query}%',))
        return [dict(row) for row in cursor.fetchall()]

# Audit logging functies
@retry_on_locked()
def log_admin_action(admin_username, action, target_type=None, target_id=None, details=None, ip_address=None):
    """Log admin actie voor audit trail"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO audit_logs (admin_username, action, target_type, target_id, details, ip_address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (admin_username, action, target_type, target_id, details, ip_address))
        return cursor.lastrowid

def get_audit_logs(limit=50, admin_username=None):
    """Haal audit logs op"""
    with get_db() as conn:
        cursor = conn.cursor()
        if admin_username:
            cursor.execute('''
                SELECT * FROM audit_logs
                WHERE admin_username = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (admin_username, limit))
        else:
            cursor.execute('''
                SELECT * FROM audit_logs
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]

# API Key functies
@retry_on_locked()
def create_api_key(customer_id, name=None):
    """Genereer API key voor klant"""
    key_value = f"mvai_{secrets.token_urlsafe(32)}"

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO api_keys (customer_id, key_value, name)
            VALUES (?, ?, ?)
        ''', (customer_id, key_value, name))

    return key_value

@retry_on_locked()
def verify_api_key(key_value):
    """
    Verifieer API key en return customer_id
    Note: Updates last_used_at timestamp, so requires write access
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT customer_id FROM api_keys
            WHERE key_value = ? AND is_active = 1
        ''', (key_value,))
        row = cursor.fetchone()

        if row:
            # Update last_used_at
            cursor.execute('''
                UPDATE api_keys
                SET last_used_at = CURRENT_TIMESTAMP
                WHERE key_value = ?
            ''', (key_value,))
            return row['customer_id']
        return None

def get_customer_api_keys(customer_id):
    """Haal alle API keys voor klant op"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM api_keys
            WHERE customer_id = ?
            ORDER BY created_at DESC
        ''', (customer_id,))
        return [dict(row) for row in cursor.fetchall()]

@retry_on_locked()
def revoke_api_key(key_id):
    """Deactiveer API key"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE api_keys
            SET is_active = 0
            WHERE id = ?
        ''', (key_id,))

if __name__ == '__main__':
    # Test database setup
    print("Initialiseer database...")
    init_db()
    print("Database geïnitialiseerd!")
