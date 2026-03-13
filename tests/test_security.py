"""
Tests voor security.py - Security module
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import database as db


class TestIPSecurityManager:
    """Test IP whitelisting en blacklisting"""

    @pytest.fixture
    def security_mgr(self, temp_db):
        """Maak een verse IPSecurityManager aan met test database"""
        from security import IPSecurityManager
        mgr = IPSecurityManager()
        return mgr

    def test_initial_state_empty(self, security_mgr):
        assert len(security_mgr.whitelist) == 0
        assert len(security_mgr.blacklist) == 0

    def test_is_whitelisted_false_by_default(self, security_mgr):
        assert security_mgr.is_whitelisted('192.168.1.1') is False

    def test_is_blacklisted_false_by_default(self, security_mgr):
        assert security_mgr.is_blacklisted('192.168.1.1') is False

    def test_add_to_whitelist(self, security_mgr):
        security_mgr.add_to_whitelist('10.0.0.1', reason='Office IP')
        assert security_mgr.is_whitelisted('10.0.0.1') is True

    def test_add_to_blacklist(self, security_mgr):
        security_mgr.add_to_blacklist('1.2.3.4', reason='Brute force', duration_hours=1)
        assert security_mgr.is_blacklisted('1.2.3.4') is True

    def test_whitelist_persists_in_db(self, security_mgr, temp_db):
        security_mgr.add_to_whitelist('10.0.0.5', reason='Test')
        with db.get_db() as conn:
            cursor = conn.execute(
                "SELECT ip_address FROM ip_whitelist WHERE ip_address = ?",
                ('10.0.0.5',)
            )
            row = cursor.fetchone()
            assert row is not None
            assert row['ip_address'] == '10.0.0.5'

    def test_blacklist_persists_in_db(self, security_mgr, temp_db):
        security_mgr.add_to_blacklist('6.6.6.6', reason='Evil')
        with db.get_db() as conn:
            cursor = conn.execute(
                "SELECT ip_address, reason FROM ip_blacklist WHERE ip_address = ?",
                ('6.6.6.6',)
            )
            row = cursor.fetchone()
            assert row is not None
            assert row['reason'] == 'Evil'

    def test_record_failed_attempt_below_threshold(self, security_mgr):
        """Minder dan 5 pogingen moet NIET auto-blacklisten"""
        result = security_mgr.record_failed_attempt('192.168.1.100', 'Wrong password')
        assert result is False or result is None

    def test_auto_blacklist_after_5_attempts(self, security_mgr):
        """5 pogingen binnen 10 minuten moet auto-blacklisten"""
        ip = '192.168.1.200'
        for i in range(4):
            security_mgr.record_failed_attempt(ip, f'Attempt {i+1}')
        # 5e poging moet blacklisten
        result = security_mgr.record_failed_attempt(ip, 'Attempt 5')
        assert result is True
        assert security_mgr.is_blacklisted(ip) is True


class TestCheckIpReputation:
    """Test IP reputatie checking"""

    @pytest.fixture
    def security_mgr(self, temp_db):
        from security import IPSecurityManager
        return IPSecurityManager()

    def test_blacklisted_ip_blocked(self, security_mgr):
        security_mgr.add_to_blacklist('1.1.1.1', 'Test')
        result = security_mgr.check_ip_reputation('1.1.1.1')
        assert result['status'] == 'blocked'
        assert result['threat_level'] == 'high'

    def test_whitelisted_ip_trusted(self, security_mgr):
        security_mgr.add_to_whitelist('10.0.0.1')
        result = security_mgr.check_ip_reputation('10.0.0.1')
        assert result['status'] == 'trusted'
        assert result['threat_level'] == 'none'

    def test_unknown_ip_low_threat(self, security_mgr):
        result = security_mgr.check_ip_reputation('8.8.8.8')
        assert result['status'] == 'unknown'
        assert result['threat_level'] == 'low'

    def test_suspicious_ip_after_failures(self, security_mgr):
        ip = '5.5.5.5'
        for _ in range(3):
            security_mgr.record_failed_attempt(ip, 'test')
        result = security_mgr.check_ip_reputation(ip)
        assert result['status'] == 'suspicious'
        assert result['threat_level'] == 'medium'


class TestAIThreatDetector:
    """Test de AI-powered threat detector"""

    @pytest.fixture
    def detector(self):
        from security import AIThreatDetector
        return AIThreatDetector()

    def test_clean_request_no_threat(self, detector):
        result = detector.analyze_request('Hello, I want to log my hours')
        assert result['is_threat'] is False
        assert result['threat_score'] == 0
        assert result['risk_level'] == 'low'

    def test_sql_injection_detected(self, detector):
        result = detector.analyze_request("'; DROP TABLE customers; --")
        assert result['is_threat'] is True
        assert result['threat_score'] > 0
        assert any(t['type'] == 'pattern_match' for t in result['threats'])

    def test_xss_detected(self, detector):
        result = detector.analyze_request('<script>alert("XSS")</script>')
        assert result['is_threat'] is True
        assert result['threat_score'] > 0

    def test_path_traversal_detected(self, detector):
        result = detector.analyze_request('../../etc/passwd')
        assert result['is_threat'] is True

    def test_command_injection_detected(self, detector):
        result = detector.analyze_request('system("rm -rf /")')
        assert result['is_threat'] is True

    def test_large_payload_flagged(self, detector):
        large_data = 'A' * 15000
        result = detector.analyze_request(large_data)
        assert any(t['type'] == 'large_payload' for t in result['threats'])

    def test_suspicious_chars_detected(self, detector):
        result = detector.analyze_request('<?php echo shell_exec("id"); ?>')
        assert result['is_threat'] is True
        assert any(t['type'] == 'suspicious_characters' for t in result['threats'])

    def test_null_byte_detected(self, detector):
        result = detector.analyze_request('file.txt%00.jpg')
        assert any(t['type'] == 'suspicious_characters' for t in result['threats'])


class TestHoneypotManager:
    """Test honeypot systeem"""

    @pytest.fixture
    def honeypot(self):
        from security import HoneypotManager
        return HoneypotManager()

    def test_known_honeypot_detected(self, honeypot):
        assert honeypot.is_honeypot('/wp-admin') is True
        assert honeypot.is_honeypot('/admin/phpMyAdmin') is True
        assert honeypot.is_honeypot('/.env') is True
        assert honeypot.is_honeypot('/config.php') is True

    def test_normal_path_not_honeypot(self, honeypot):
        assert honeypot.is_honeypot('/') is False
        assert honeypot.is_honeypot('/login') is False
        assert honeypot.is_honeypot('/api/v1/health') is False
        assert honeypot.is_honeypot('/dashboard') is False

    def test_trap_ip_adds_to_trapped(self, honeypot, temp_db):
        honeypot.trap_ip('1.2.3.4', '/wp-admin')
        assert '1.2.3.4' in honeypot.trapped_ips


class TestEncryptionHelpers:
    """Test encryptie en token hulpfuncties"""

    def test_encrypt_returns_hash(self):
        from security import encrypt_sensitive_data
        result = encrypt_sensitive_data('test_data')
        assert isinstance(result, str)
        assert len(result) == 64  # SHA-256 hex digest

    def test_encrypt_deterministic(self):
        from security import encrypt_sensitive_data
        hash1 = encrypt_sensitive_data('same_input')
        hash2 = encrypt_sensitive_data('same_input')
        assert hash1 == hash2

    def test_encrypt_different_inputs_differ(self):
        from security import encrypt_sensitive_data
        hash1 = encrypt_sensitive_data('input_a')
        hash2 = encrypt_sensitive_data('input_b')
        assert hash1 != hash2

    def test_generate_secure_token_length(self):
        from security import generate_secure_token
        token = generate_secure_token()
        assert isinstance(token, str)
        assert len(token) > 20  # token_urlsafe(32) produces ~43 chars

    def test_generate_secure_token_unique(self):
        from security import generate_secure_token
        tokens = {generate_secure_token() for _ in range(100)}
        assert len(tokens) == 100  # All tokens should be unique
