"""
MVAI Connexx - Test Fixtures & Configuration
Shared fixtures voor alle test modules
"""
import os
import sys
import sqlite3
import tempfile
import pytest

# Voeg project root toe aan sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Stel test environment in VOOR imports
os.environ['FLASK_ENV'] = 'development'
os.environ['SECRET_KEY'] = 'test-secret-key-not-for-production'
os.environ['ENABLE_AI_ASSISTANT'] = 'false'
os.environ['ENABLE_DEMO_MODE'] = 'false'


@pytest.fixture
def temp_db(tmp_path):
    """Maak een tijdelijke database voor tests"""
    db_path = str(tmp_path / 'test_mvai.db')
    os.environ['DATABASE_PATH'] = db_path

    # Herlaad database module met nieuw pad
    import database as db_module
    original_db = db_module.DATABASE
    db_module.DATABASE = db_path

    # Initialiseer schema
    db_module.init_db()

    yield db_path

    # Herstel origineel pad
    db_module.DATABASE = original_db


@pytest.fixture
def db_conn(temp_db):
    """Geeft een database connectie voor directe queries"""
    import database as db_module
    with db_module.get_db() as conn:
        yield conn


@pytest.fixture
def sample_customer(temp_db):
    """Maak een test klant aan"""
    import database as db_module
    with db_module.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customers (name, access_code, status, contact_email)
            VALUES (?, ?, ?, ?)
        ''', ('Test Bedrijf BV', 'test-access-code-123', 'active', 'test@example.com'))
        customer_id = cursor.lastrowid
    return {
        'id': customer_id,
        'name': 'Test Bedrijf BV',
        'access_code': 'test-access-code-123',
        'email': 'test@example.com'
    }


@pytest.fixture
def sample_api_key(temp_db, sample_customer):
    """Maak een test API key aan"""
    import database as db_module
    key_value = 'mvai-test-key-abc123def456'
    with db_module.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO api_keys (customer_id, key_value, name, is_active)
            VALUES (?, ?, ?, 1)
        ''', (sample_customer['id'], key_value, 'Test API Key'))
    return key_value
