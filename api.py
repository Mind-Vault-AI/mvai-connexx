"""
MVAI Connexx - REST API Module
RESTful API endpoints voor third-party integraties
"""
from flask import Blueprint, request, jsonify
from functools import wraps
import database as db
import json
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# ═══════════════════════════════════════════════════════
# API AUTHENTICATION
# ═══════════════════════════════════════════════════════

def require_api_key(f):
    """Decorator voor API key authenticatie"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')

        if not api_key:
            return jsonify({
                'error': 'API key required',
                'message': 'Provide API key via X-API-Key header or api_key parameter'
            }), 401

        customer_id = db.verify_api_key(api_key)

        if not customer_id:
            return jsonify({
                'error': 'Invalid API key',
                'message': 'API key is invalid or has been revoked'
            }), 401

        # Sla customer_id op in request context
        request.customer_id = customer_id
        return f(*args, **kwargs)

    return decorated_function

# ═══════════════════════════════════════════════════════
# HEALTH & STATUS ENDPOINTS
# ═══════════════════════════════════════════════════════

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint voor monitoring"""
    try:
        # Test database connectie
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1')

        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected',
            'version': '2.0.0'
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 503

@api_bp.route('/status', methods=['GET'])
@require_api_key
def get_status():
    """Get customer account status"""
    customer = db.get_customer_by_id(request.customer_id)
    stats = db.get_customer_stats(request.customer_id)

    return jsonify({
        'customer': {
            'id': customer['id'],
            'name': customer['name'],
            'status': customer['status'],
            'created_at': customer['created_at']
        },
        'stats': stats
    }), 200

# ═══════════════════════════════════════════════════════
# LOGS ENDPOINTS
# ═══════════════════════════════════════════════════════

@api_bp.route('/logs', methods=['GET'])
@require_api_key
def get_logs():
    """Haal logs op voor authenticated customer"""
    limit = min(int(request.args.get('limit', 100)), 1000)  # Max 1000
    offset = int(request.args.get('offset', 0))

    logs = db.get_customer_logs(request.customer_id, limit=limit, offset=offset)

    return jsonify({
        'logs': logs,
        'count': len(logs),
        'limit': limit,
        'offset': offset
    }), 200

@api_bp.route('/logs', methods=['POST'])
@require_api_key
def create_log():
    """Maak nieuwe log entry via API"""
    if not request.json:
        return jsonify({'error': 'JSON body required'}), 400

    try:
        # Haal IP op
        if request.headers.getlist("X-Forwarded-For"):
            ip_address = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip_address = request.remote_addr

        # Data serialiseren
        data_str = json.dumps(request.json)

        # Opslaan
        log_id = db.create_log(
            customer_id=request.customer_id,
            ip_address=ip_address,
            data=data_str,
            metadata=None
        )

        return jsonify({
            'success': True,
            'log_id': log_id,
            'timestamp': datetime.now().isoformat()
        }), 201

    except Exception as e:
        return jsonify({
            'error': 'Failed to create log',
            'message': str(e)
        }), 500

@api_bp.route('/logs/<int:log_id>', methods=['GET'])
@require_api_key
def get_log(log_id):
    """Haal specifieke log op"""
    with db.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM logs
            WHERE id = ? AND customer_id = ?
        ''', (log_id, request.customer_id))

        log = cursor.fetchone()

        if not log:
            return jsonify({'error': 'Log not found'}), 404

        return jsonify(dict(log)), 200

@api_bp.route('/logs/search', methods=['GET'])
@require_api_key
def search_logs():
    """Zoek in logs via API"""
    query = request.args.get('q', '')

    if not query:
        return jsonify({'error': 'Query parameter "q" required'}), 400

    logs = db.search_logs(query, customer_id=request.customer_id)

    return jsonify({
        'query': query,
        'results': logs,
        'count': len(logs)
    }), 200

# ═══════════════════════════════════════════════════════
# ANALYTICS ENDPOINTS
# ═══════════════════════════════════════════════════════

@api_bp.route('/analytics/stats', methods=['GET'])
@require_api_key
def get_analytics_stats():
    """Haal analytics statistieken op"""
    stats = db.get_customer_stats(request.customer_id)

    return jsonify(stats), 200

@api_bp.route('/analytics/daily', methods=['GET'])
@require_api_key
def get_daily_analytics():
    """Haal dagelijkse activity op"""
    days = min(int(request.args.get('days', 30)), 365)

    with db.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM logs
            WHERE customer_id = ?
            AND timestamp >= DATE('now', ?)
            GROUP BY DATE(timestamp)
            ORDER BY date
        ''', (request.customer_id, f'-{days} days'))

        daily_data = [
            {'date': row['date'], 'count': row['count']}
            for row in cursor.fetchall()
        ]

    return jsonify({
        'period': f'{days} days',
        'data': daily_data
    }), 200

# ═══════════════════════════════════════════════════════
# EXPORT ENDPOINTS
# ═══════════════════════════════════════════════════════

@api_bp.route('/export/json', methods=['GET'])
@require_api_key
def export_json():
    """Export data als JSON"""
    limit = min(int(request.args.get('limit', 10000)), 100000)
    logs = db.get_customer_logs(request.customer_id, limit=limit)

    customer = db.get_customer_by_id(request.customer_id)

    return jsonify({
        'customer': {
            'id': customer['id'],
            'name': customer['name']
        },
        'exported_at': datetime.now().isoformat(),
        'log_count': len(logs),
        'logs': logs
    }), 200

# ═══════════════════════════════════════════════════════
# API KEY MANAGEMENT
# ═══════════════════════════════════════════════════════

@api_bp.route('/keys', methods=['GET'])
@require_api_key
def list_api_keys():
    """List alle API keys voor customer"""
    keys = db.get_customer_api_keys(request.customer_id)

    # Maskeer key values voor security
    for key in keys:
        key['key_value'] = key['key_value'][:15] + '...'

    return jsonify({
        'keys': keys,
        'count': len(keys)
    }), 200

# ═══════════════════════════════════════════════════════
# BATCH OPERATIONS
# ═══════════════════════════════════════════════════════

@api_bp.route('/logs/batch', methods=['POST'])
@require_api_key
def batch_create_logs():
    """Maak meerdere logs in één request"""
    if not request.json or 'logs' not in request.json:
        return jsonify({'error': 'JSON body with "logs" array required'}), 400

    logs_data = request.json['logs']

    if not isinstance(logs_data, list):
        return jsonify({'error': '"logs" must be an array'}), 400

    if len(logs_data) > 100:
        return jsonify({'error': 'Maximum 100 logs per batch'}), 400

    # Haal IP op
    if request.headers.getlist("X-Forwarded-For"):
        ip_address = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip_address = request.remote_addr

    created_ids = []
    errors = []

    for i, log_data in enumerate(logs_data):
        try:
            data_str = json.dumps(log_data)
            log_id = db.create_log(
                customer_id=request.customer_id,
                ip_address=ip_address,
                data=data_str,
                metadata=None
            )
            created_ids.append(log_id)
        except Exception as e:
            errors.append({
                'index': i,
                'error': str(e)
            })

    return jsonify({
        'success': True,
        'created_count': len(created_ids),
        'created_ids': created_ids,
        'errors': errors
    }), 201 if not errors else 207

# ═══════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════

@api_bp.errorhandler(404)
def api_not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@api_bp.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed'}), 405

@api_bp.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500
