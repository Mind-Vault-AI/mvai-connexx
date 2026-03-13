"""
Tests voor database.py - Database module
"""
import os
import sqlite3
import time
import pytest
from unittest.mock import patch, MagicMock

import database as db


class TestGetDb:
    """Test de get_db context manager"""

    def test_connection_opens_and_closes(self, temp_db):
        with db.get_db() as conn:
            assert conn is not None
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            result = cursor.fetchone()
            assert result[0] == 1

    def test_wal_mode_enabled(self, temp_db):
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('PRAGMA journal_mode')
            mode = cursor.fetchone()[0]
            assert mode == 'wal'

    def test_auto_commit_on_success(self, temp_db):
        with db.get_db() as conn:
            conn.execute(
                "INSERT INTO customers (name, access_code) VALUES (?, ?)",
                ('AutoCommit Test', 'ac-test-123')
            )

        # Verify data persisted
        with db.get_db() as conn:
            cursor = conn.execute(
                "SELECT name FROM customers WHERE access_code = ?",
                ('ac-test-123',)
            )
            row = cursor.fetchone()
            assert row is not None
            assert row['name'] == 'AutoCommit Test'

    def test_rollback_on_exception(self, temp_db):
        try:
            with db.get_db() as conn:
                conn.execute(
                    "INSERT INTO customers (name, access_code) VALUES (?, ?)",
                    ('Rollback Test', 'rb-test-123')
                )
                raise ValueError("Force rollback")
        except ValueError:
            pass

        # Verify data was NOT persisted
        with db.get_db() as conn:
            cursor = conn.execute(
                "SELECT name FROM customers WHERE access_code = ?",
                ('rb-test-123',)
            )
            row = cursor.fetchone()
            assert row is None

    def test_row_factory_returns_dict_like(self, temp_db):
        with db.get_db() as conn:
            conn.execute(
                "INSERT INTO customers (name, access_code, contact_email) VALUES (?, ?, ?)",
                ('Dict Test', 'dt-123', 'dict@test.com')
            )
            cursor = conn.execute(
                "SELECT * FROM customers WHERE access_code = ?",
                ('dt-123',)
            )
            row = cursor.fetchone()
            # sqlite3.Row supports dict-like access
            assert row['name'] == 'Dict Test'
            assert row['contact_email'] == 'dict@test.com'


class TestInitDb:
    """Test database initialisatie"""

    def test_creates_customers_table(self, temp_db):
        with db.get_db() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='customers'"
            )
            assert cursor.fetchone() is not None

    def test_creates_logs_table(self, temp_db):
        with db.get_db() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='logs'"
            )
            assert cursor.fetchone() is not None

    def test_creates_api_keys_table(self, temp_db):
        with db.get_db() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='api_keys'"
            )
            assert cursor.fetchone() is not None

    def test_creates_security_tables(self, temp_db):
        with db.get_db() as conn:
            for table in ['ip_whitelist', 'ip_blacklist', 'security_incidents']:
                cursor = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (table,)
                )
                assert cursor.fetchone() is not None, f"Table {table} not created"

    def test_creates_audit_logs_table(self, temp_db):
        with db.get_db() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='audit_logs'"
            )
            assert cursor.fetchone() is not None

    def test_creates_ai_tables(self, temp_db):
        with db.get_db() as conn:
            for table in ['ai_assistant_preferences', 'ai_learning', 'ai_conversations']:
                cursor = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (table,)
                )
                assert cursor.fetchone() is not None, f"Table {table} not created"

    def test_idempotent_init(self, temp_db):
        """init_db() moet veilig meerdere keren uitgevoerd kunnen worden"""
        db.init_db()
        db.init_db()
        with db.get_db() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='customers'"
            )
            assert cursor.fetchone() is not None


class TestCustomerOperations:
    """Test klant CRUD operaties"""

    def test_insert_customer(self, temp_db):
        with db.get_db() as conn:
            conn.execute(
                "INSERT INTO customers (name, access_code, contact_email) VALUES (?, ?, ?)",
                ('Test BV', 'code-123', 'info@test.nl')
            )
        with db.get_db() as conn:
            cursor = conn.execute("SELECT * FROM customers WHERE name = ?", ('Test BV',))
            row = cursor.fetchone()
            assert row['name'] == 'Test BV'
            assert row['access_code'] == 'code-123'
            assert row['status'] == 'active'

    def test_unique_name_constraint(self, temp_db):
        with db.get_db() as conn:
            conn.execute(
                "INSERT INTO customers (name, access_code) VALUES (?, ?)",
                ('Uniek BV', 'code-1')
            )
        with pytest.raises(sqlite3.IntegrityError):
            with db.get_db() as conn:
                conn.execute(
                    "INSERT INTO customers (name, access_code) VALUES (?, ?)",
                    ('Uniek BV', 'code-2')
                )

    def test_unique_access_code_constraint(self, temp_db):
        with db.get_db() as conn:
            conn.execute(
                "INSERT INTO customers (name, access_code) VALUES (?, ?)",
                ('Bedrijf A', 'code-same')
            )
        with pytest.raises(sqlite3.IntegrityError):
            with db.get_db() as conn:
                conn.execute(
                    "INSERT INTO customers (name, access_code) VALUES (?, ?)",
                    ('Bedrijf B', 'code-same')
                )


class TestApiKeyOperations:
    """Test API key operaties"""

    def test_create_api_key(self, sample_customer, temp_db):
        with db.get_db() as conn:
            conn.execute(
                "INSERT INTO api_keys (customer_id, key_value, name) VALUES (?, ?, ?)",
                (sample_customer['id'], 'key-abc123', 'My API Key')
            )
            cursor = conn.execute(
                "SELECT * FROM api_keys WHERE key_value = ?",
                ('key-abc123',)
            )
            row = cursor.fetchone()
            assert row['customer_id'] == sample_customer['id']
            assert row['is_active'] == 1

    def test_unique_key_value_constraint(self, sample_customer, temp_db):
        with db.get_db() as conn:
            conn.execute(
                "INSERT INTO api_keys (customer_id, key_value) VALUES (?, ?)",
                (sample_customer['id'], 'key-duplicate')
            )
        with pytest.raises(sqlite3.IntegrityError):
            with db.get_db() as conn:
                conn.execute(
                    "INSERT INTO api_keys (customer_id, key_value) VALUES (?, ?)",
                    (sample_customer['id'], 'key-duplicate')
                )


class TestRetryOnLocked:
    """Test de retry_on_locked decorator"""

    def test_successful_execution_no_retry(self):
        call_count = 0

        @db.retry_on_locked(max_retries=3, initial_delay=0.01)
        def succeeds():
            nonlocal call_count
            call_count += 1
            return 'success'

        result = succeeds()
        assert result == 'success'
        assert call_count == 1

    def test_retries_on_locked_then_succeeds(self):
        call_count = 0

        @db.retry_on_locked(max_retries=5, initial_delay=0.01)
        def fails_then_succeeds():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise sqlite3.OperationalError("database is locked")
            return 'success'

        result = fails_then_succeeds()
        assert result == 'success'
        assert call_count == 3

    def test_raises_after_max_retries(self):
        @db.retry_on_locked(max_retries=2, initial_delay=0.01)
        def always_locked():
            raise sqlite3.OperationalError("database is locked")

        with pytest.raises(sqlite3.OperationalError, match="database is locked"):
            always_locked()

    def test_non_lock_error_raises_immediately(self):
        call_count = 0

        @db.retry_on_locked(max_retries=5, initial_delay=0.01)
        def other_error():
            nonlocal call_count
            call_count += 1
            raise sqlite3.OperationalError("no such table: foo")

        with pytest.raises(sqlite3.OperationalError, match="no such table"):
            other_error()
        assert call_count == 1
