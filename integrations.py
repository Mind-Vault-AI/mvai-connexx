"""
MVAI Connexx - ERP/WMS/Universele Integratie Module
Ondersteunt: SAP, Exact Online, AFAS, Shopify, WooCommerce, Odoo,
             Microsoft Dynamics, Magento, Wix, en generieke REST/webhook koppelingen
Zowel cloud als on-premise IP-gebaseerde verbindingen
"""
import json
import os
import secrets
import requests
from datetime import datetime


# ═══════════════════════════════════════════════════════
# ONDERSTEUNDE INTEGRATIES
# ═══════════════════════════════════════════════════════

INTEGRATION_CATALOG = {
    # ── ERP Systemen ────────────────────────────────────
    'exact_online': {
        'name': 'Exact Online',
        'category': 'ERP',
        'logo': '🟦',
        'description': 'Koppel uw Exact Online administratie. Facturen, orders en relaties automatisch synchroniseren.',
        'auth_type': 'oauth2',
        'fields': ['client_id', 'client_secret', 'division'],
        'docs_url': 'https://support.exactonline.com/community/s/knowledge-base',
        'popular': True,
    },
    'afas': {
        'name': 'AFAS Software',
        'category': 'ERP',
        'logo': '🟨',
        'description': 'Koppel AFAS Profit via de App Connector REST API.',
        'auth_type': 'api_key',
        'fields': ['environment_url', 'api_token', 'connector_name'],
        'docs_url': 'https://help.afas.nl/help/NL/SE/App/Help/AF_connector.htm',
        'popular': True,
    },
    'sap': {
        'name': 'SAP Business One / S/4HANA',
        'category': 'ERP',
        'logo': '🔷',
        'description': 'Integratie via SAP OData API. On-premise of cloud. Artikelen, orders, voorraden.',
        'auth_type': 'basic',
        'fields': ['base_url', 'company_db', 'username', 'password'],
        'docs_url': 'https://help.sap.com/docs/SAP_BUSINESS_ONE',
        'popular': True,
    },
    'odoo': {
        'name': 'Odoo',
        'category': 'ERP',
        'logo': '🟣',
        'description': 'Koppel Odoo via XML-RPC of REST API. Klanten, producten, inkoop- en verkooporders.',
        'auth_type': 'api_key',
        'fields': ['url', 'database', 'api_key'],
        'docs_url': 'https://www.odoo.com/documentation/16.0/developer/api/external_api.html',
        'popular': False,
    },
    'microsoft_dynamics': {
        'name': 'Microsoft Dynamics 365',
        'category': 'ERP',
        'logo': '🔵',
        'description': 'Business Central of Finance & Operations via OAuth2 / Azure AD.',
        'auth_type': 'oauth2',
        'fields': ['tenant_id', 'client_id', 'client_secret', 'environment'],
        'docs_url': 'https://docs.microsoft.com/en-us/dynamics365/',
        'popular': False,
    },
    # ── WMS / Logistiek ──────────────────────────────────
    'wms_generic': {
        'name': 'WMS (Generiek REST)',
        'category': 'WMS',
        'logo': '🏭',
        'description': 'Verbind met elk WMS dat een REST API biedt. Instelbaar endpoint, headers en authenticatie.',
        'auth_type': 'api_key',
        'fields': ['base_url', 'api_key', 'warehouse_id'],
        'docs_url': None,
        'popular': True,
    },
    'wms_on_premise': {
        'name': 'WMS On-Premise (IP)',
        'category': 'WMS',
        'logo': '🖥️',
        'description': 'Directe verbinding via bedrijfs-IP. Gebruikt basis-authenticatie of token over intern netwerk.',
        'auth_type': 'basic',
        'fields': ['ip_address', 'port', 'username', 'password', 'endpoint_path'],
        'docs_url': None,
        'popular': True,
    },
    # ── E-Commerce ──────────────────────────────────────
    'shopify': {
        'name': 'Shopify',
        'category': 'E-Commerce',
        'logo': '🟩',
        'description': 'Synchroniseer producten, orders en klanten vanuit uw Shopify webshop.',
        'auth_type': 'api_key',
        'fields': ['shop_domain', 'api_key', 'api_secret'],
        'docs_url': 'https://shopify.dev/docs/api',
        'popular': True,
    },
    'woocommerce': {
        'name': 'WooCommerce',
        'category': 'E-Commerce',
        'logo': '🟪',
        'description': 'WordPress WooCommerce REST API v3. Orders, producten, klanten, voorraden.',
        'auth_type': 'api_key',
        'fields': ['store_url', 'consumer_key', 'consumer_secret'],
        'docs_url': 'https://woocommerce.github.io/woocommerce-rest-api-docs/',
        'popular': True,
    },
    'magento': {
        'name': 'Magento 2',
        'category': 'E-Commerce',
        'logo': '🟠',
        'description': 'Magento 2 REST API via Integration Token. Catalogus, orders, klanten.',
        'auth_type': 'api_key',
        'fields': ['base_url', 'access_token'],
        'docs_url': 'https://devdocs.magento.com/guides/v2.4/rest/bk-rest.html',
        'popular': False,
    },
    'wix': {
        'name': 'Wix',
        'category': 'E-Commerce',
        'logo': '⬛',
        'description': 'Wix Stores via Wix REST API. Orders, producten en contacten.',
        'auth_type': 'api_key',
        'fields': ['site_id', 'api_key'],
        'docs_url': 'https://dev.wix.com/docs/rest',
        'popular': False,
    },
    # ── Communicatie / Output ────────────────────────────
    'email_smtp': {
        'name': 'E-mail (SMTP)',
        'category': 'Output',
        'logo': '📧',
        'description': 'Stuur automatisch rapporten, alerts of exports via uw eigen mailserver.',
        'auth_type': 'basic',
        'fields': ['smtp_host', 'smtp_port', 'username', 'password', 'from_email'],
        'docs_url': None,
        'popular': True,
    },
    'webhook_out': {
        'name': 'Uitgaande Webhook',
        'category': 'Output',
        'logo': '🔗',
        'description': 'Stuur data automatisch naar elk extern systeem via HTTP POST (JSON).',
        'auth_type': 'api_key',
        'fields': ['url', 'secret_header', 'events'],
        'docs_url': None,
        'popular': True,
    },
    'printer_network': {
        'name': 'Netwerk Printer / Label',
        'category': 'Output',
        'logo': '🖨️',
        'description': 'Direct printen naar netwerk- of labelprinter via IP adres (ZPL, PCL, PDF).',
        'auth_type': 'none',
        'fields': ['printer_ip', 'printer_port', 'print_format'],
        'docs_url': None,
        'popular': False,
    },
}

INTEGRATION_CATEGORIES = ['Alles', 'ERP', 'WMS', 'E-Commerce', 'Output']


# ═══════════════════════════════════════════════════════
# VERBINDING TESTEN
# ═══════════════════════════════════════════════════════

def test_integration_connection(integration_type, config):
    """
    Test de verbinding met een integratie.
    Geeft {'success': bool, 'message': str} terug.
    """
    try:
        if integration_type == 'exact_online':
            return _test_exact_online(config)
        elif integration_type == 'afas':
            return _test_afas(config)
        elif integration_type == 'shopify':
            return _test_shopify(config)
        elif integration_type == 'woocommerce':
            return _test_woocommerce(config)
        elif integration_type in ('wms_generic', 'wms_on_premise', 'magento', 'wix', 'sap', 'odoo', 'microsoft_dynamics'):
            return _test_generic_rest(config)
        elif integration_type == 'email_smtp':
            return _test_smtp(config)
        elif integration_type == 'webhook_out':
            return _test_webhook(config)
        elif integration_type == 'printer_network':
            return _test_printer(config)
        else:
            return {'success': True, 'message': 'Configuratie opgeslagen (handmatige verificatie vereist)'}
    except Exception as e:
        return {'success': False, 'message': f'Verbindingsfout: {str(e)}'}


def _test_shopify(config):
    shop = config.get('shop_domain', '').rstrip('/')
    key = config.get('api_key')
    secret = config.get('api_secret')
    if not shop or not key:
        return {'success': False, 'message': 'Ontbrekende velden: shop_domain en api_key zijn verplicht'}
    url = f"https://{shop}/admin/api/2024-01/shop.json"
    r = requests.get(url, auth=(key, secret), timeout=8)
    if r.status_code == 200:
        shop_name = r.json().get('shop', {}).get('name', shop)
        return {'success': True, 'message': f'Verbonden met Shopify winkel: {shop_name}'}
    return {'success': False, 'message': f'Shopify API fout (HTTP {r.status_code})'}


def _test_woocommerce(config):
    url = config.get('store_url', '').rstrip('/')
    ck = config.get('consumer_key')
    cs = config.get('consumer_secret')
    if not url or not ck:
        return {'success': False, 'message': 'Ontbrekende velden'}
    r = requests.get(f"{url}/wp-json/wc/v3/system_status", auth=(ck, cs), timeout=8)
    if r.status_code == 200:
        return {'success': True, 'message': f'Verbonden met WooCommerce op {url}'}
    return {'success': False, 'message': f'WooCommerce API fout (HTTP {r.status_code})'}


def _test_exact_online(config):
    # Exact Online gebruikt OAuth2 - we controleren of de velden aanwezig zijn
    client_id = config.get('client_id')
    if not client_id:
        return {'success': False, 'message': 'Client ID is verplicht voor Exact Online'}
    return {'success': True, 'message': 'Exact Online configuratie opgeslagen. Voltooi OAuth2 autorisatie via het integratiepaneel.'}


def _test_afas(config):
    env_url = config.get('environment_url', '').rstrip('/')
    token = config.get('api_token')
    if not env_url or not token:
        return {'success': False, 'message': 'Ontbrekende velden: environment_url en api_token zijn verplicht'}
    headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}
    try:
        r = requests.get(f"{env_url}/profitrestservices/connectors", headers=headers, timeout=8)
        if r.status_code in (200, 204):
            return {'success': True, 'message': f'Verbonden met AFAS omgeving: {env_url}'}
        return {'success': False, 'message': f'AFAS API fout (HTTP {r.status_code})'}
    except Exception:
        return {'success': False, 'message': 'Kan AFAS omgeving niet bereiken. Controleer URL en netwerktoegang.'}


def _test_generic_rest(config):
    base_url = config.get('base_url') or config.get('url') or config.get('ip_address')
    if not base_url:
        return {'success': False, 'message': 'Basis URL of IP-adres ontbreekt'}
    return {'success': True, 'message': f'Configuratie opgeslagen voor {base_url}'}


def _test_smtp(config):
    import smtplib
    host = config.get('smtp_host')
    port = int(config.get('smtp_port', 587))
    username = config.get('username')
    password = config.get('password')
    if not host or not username:
        return {'success': False, 'message': 'SMTP host en gebruikersnaam zijn verplicht'}
    try:
        with smtplib.SMTP(host, port, timeout=8) as s:
            s.ehlo()
            s.starttls()
            s.login(username, password)
        return {'success': True, 'message': f'SMTP verbinding geslaagd met {host}:{port}'}
    except Exception as e:
        return {'success': False, 'message': f'SMTP fout: {str(e)}'}


def _test_webhook(config):
    url = config.get('url')
    if not url:
        return {'success': False, 'message': 'Webhook URL is verplicht'}
    try:
        payload = {'test': True, 'source': 'mvai-connexx', 'timestamp': datetime.utcnow().isoformat()}
        headers = {'Content-Type': 'application/json', 'X-MVAI-Test': '1'}
        secret = config.get('secret_header')
        if secret:
            headers['X-MVAI-Secret'] = secret
        r = requests.post(url, json=payload, headers=headers, timeout=8)
        return {'success': r.status_code < 400, 'message': f'Webhook test: HTTP {r.status_code}'}
    except Exception as e:
        return {'success': False, 'message': f'Webhook fout: {str(e)}'}


def _test_printer(config):
    import socket
    ip = config.get('printer_ip')
    port = int(config.get('printer_port', 9100))
    if not ip:
        return {'success': False, 'message': 'Printer IP is verplicht'}
    try:
        s = socket.create_connection((ip, port), timeout=4)
        s.close()
        return {'success': True, 'message': f'Printer bereikbaar op {ip}:{port}'}
    except Exception as e:
        return {'success': False, 'message': f'Printer niet bereikbaar: {str(e)}'}


# ═══════════════════════════════════════════════════════
# DATA SYNC (generiek)
# ═══════════════════════════════════════════════════════

def sync_integration(integration_id, integration_type, config_str, customer_id):
    """
    Voer een datasync uit voor een integratie.
    Geeft het aantal gesynchroniseerde records terug.
    """
    import database as _db
    try:
        config = json.loads(config_str) if config_str else {}
        records = _pull_data(integration_type, config)
        # Sla elk record op als log
        for record in records:
            _db.create_log(
                customer_id=customer_id,
                ip_address='integration-sync',
                data=json.dumps(record),
                metadata=json.dumps({'source': integration_type, 'integration_id': integration_id})
            )
        _db.update_integration_sync(integration_id, status='active')
        return len(records)
    except Exception as e:
        _db.update_integration_sync(integration_id, status='error', error=str(e))
        raise


def _pull_data(integration_type, config):
    """Haal data op uit externe integratie"""
    if integration_type == 'shopify':
        return _pull_shopify(config)
    elif integration_type == 'woocommerce':
        return _pull_woocommerce(config)
    elif integration_type == 'wms_generic':
        return _pull_generic_wms(config)
    elif integration_type == 'afas':
        return _pull_afas(config)
    else:
        return []


def _pull_shopify(config):
    shop = config.get('shop_domain', '').rstrip('/')
    key = config.get('api_key')
    secret = config.get('api_secret')
    r = requests.get(f"https://{shop}/admin/api/2024-01/orders.json?status=any&limit=50",
                     auth=(key, secret), timeout=15)
    r.raise_for_status()
    return r.json().get('orders', [])


def _pull_woocommerce(config):
    url = config.get('store_url', '').rstrip('/')
    ck = config.get('consumer_key')
    cs = config.get('consumer_secret')
    r = requests.get(f"{url}/wp-json/wc/v3/orders?per_page=50",
                     auth=(ck, cs), timeout=15)
    r.raise_for_status()
    return r.json()


def _pull_generic_wms(config):
    base = config.get('base_url', '').rstrip('/')
    key = config.get('api_key', '')
    path = config.get('endpoint_path', '/api/stock')
    headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
    r = requests.get(f"{base}{path}", headers=headers, timeout=15)
    r.raise_for_status()
    data = r.json()
    return data if isinstance(data, list) else [data]


def _pull_afas(config):
    env_url = config.get('environment_url', '').rstrip('/')
    token = config.get('api_token')
    connector = config.get('connector_name', 'Profit_Article')
    headers = {'Authorization': f'AfasToken {token}', 'Content-Type': 'application/json'}
    r = requests.get(f"{env_url}/profitrestservices/connectors/{connector}",
                     headers=headers, timeout=15)
    r.raise_for_status()
    return r.json().get('rows', [])
