"""
MVAI Connexx - Database Module
Multi-tenant SQLite database voor klantgegevens en logs
"""
import sqlite3
import secrets
import hashlib
from datetime import datetime
from contextlib import contextmanager

DATABASE = 'mvai_connexx.db'

@contextmanager
def get_db():
    """Context manager voor database connecties"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
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
                company_info TEXT
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

        # Indices voor performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_customer ON logs(customer_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_customers_code ON customers(access_code)')

        conn.commit()

def generate_access_code(length=16):
    """Genereer veilige access code"""
    return secrets.token_urlsafe(length)

def hash_access_code(code):
    """Hash access code voor veilige opslag"""
    return hashlib.sha256(code.encode()).hexdigest()

# Customer functies
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

def update_customer_status(customer_id, status):
    """Update klant status"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE customers SET status = ? WHERE id = ?', (status, customer_id))

# Log functies
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

if __name__ == '__main__':
    # Test database setup
    print("Initialiseer database...")
    init_db()
    print("Database geïnitialiseerd!")
