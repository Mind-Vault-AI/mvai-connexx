"""
MVAI Connexx - Multi-Tenant Enterprise Platform
Flask applicatie met authentication en customer management
"""
import os
import json
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import database as db
import analytics
import csv
import io

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Rate limiting voor API protection
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Initialiseer database bij startup
with app.app_context():
    db.init_db()

# Registreer API Blueprint
from api import api_bp
app.register_blueprint(api_bp)

# ═══════════════════════════════════════════════════════
# DECORATORS VOOR AUTHENTICATION
# ═══════════════════════════════════════════════════════

def login_required(f):
    """Vereist dat gebruiker is ingelogd"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'customer_id' not in session and 'admin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Vereist admin rechten"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            flash('Admin rechten vereist', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ═══════════════════════════════════════════════════════
# HELPER FUNCTIES
# ═══════════════════════════════════════════════════════

def get_client_ip():
    """Haal client IP adres op (werkt achter proxy/load balancer)"""
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr

# ═══════════════════════════════════════════════════════
# PUBLIC ROUTES
# ═══════════════════════════════════════════════════════

@app.route('/')
def index():
    """Landing page - redirect naar login of dashboard"""
    if 'customer_id' in session:
        return redirect(url_for('customer_dashboard'))
    elif 'admin' in session:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login pagina voor klanten en admins"""
    if request.method == 'POST':
        access_code = request.form.get('access_code', '').strip()

        if not access_code:
            flash('Voer een access code in', 'error')
            return render_template('login.html')

        # Check voor admin login
        admin = db.verify_admin(access_code)
        if admin:
            session.permanent = True
            session['admin'] = True
            session['admin_username'] = admin['username']
            flash(f'Welkom Admin {admin["username"]}!', 'success')
            return redirect(url_for('admin_dashboard'))

        # Check voor customer login
        customer = db.get_customer_by_code(access_code)
        if customer:
            session.permanent = True
            session['customer_id'] = customer['id']
            session['customer_name'] = customer['name']
            flash(f'Welkom {customer["name"]}!', 'success')
            return redirect(url_for('customer_dashboard'))

        flash('Ongeldige access code', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Log uit en clear session"""
    session.clear()
    flash('Succesvol uitgelogd', 'success')
    return redirect(url_for('login'))

# ═══════════════════════════════════════════════════════
# CUSTOMER ROUTES
# ═══════════════════════════════════════════════════════

@app.route('/dashboard')
@login_required
def customer_dashboard():
    """Customer dashboard - alleen eigen data"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))

    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)
    stats = db.get_customer_stats(customer_id)
    logs = db.get_customer_logs(customer_id, limit=20)

    return render_template('customer_dashboard.html',
                         customer=customer,
                         stats=stats,
                         logs=logs)

@app.route('/api/save', methods=['POST'])
@login_required
def save_entry():
    """
    API endpoint om data op te slaan
    Behoud backward compatibility met oude /api/save
    """
    if 'admin' in session:
        return jsonify({"status": "error", "message": "Admin kan niet direct data opslaan"}), 403

    try:
        entry = request.json
        customer_id = session['customer_id']
        ip_address = get_client_ip()

        # Data serialiseren naar JSON string
        data_str = json.dumps(entry)

        # Opslaan in database
        log_id = db.create_log(
            customer_id=customer_id,
            ip_address=ip_address,
            data=data_str,
            metadata=None
        )

        return jsonify({
            "status": "SECURE_COMMIT",
            "message": "Data Encrypted & Stored.",
            "log_id": log_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/customer/logs')
@login_required
def customer_logs():
    """Bekijk alle logs voor customer"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))

    customer_id = session['customer_id']
    page = request.args.get('page', 1, type=int)
    limit = 50
    offset = (page - 1) * limit

    logs = db.get_customer_logs(customer_id, limit=limit, offset=offset)
    customer = db.get_customer_by_id(customer_id)

    return render_template('customer_logs.html',
                         customer=customer,
                         logs=logs,
                         page=page)

@app.route('/customer/export/csv')
@login_required
def customer_export_csv():
    """Export customer data naar CSV"""
    if 'admin' in session:
        return jsonify({"error": "Admin kan niet customer export gebruiken"}), 403

    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)
    logs = db.get_customer_logs(customer_id, limit=10000)

    # Maak CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(['ID', 'Timestamp', 'IP Address', 'Data'])

    # Data
    for log in logs:
        writer.writerow([
            log['id'],
            log['timestamp'],
            log['ip_address'],
            log['data']
        ])

    # Converteer naar bytes
    output.seek(0)
    bytes_output = io.BytesIO()
    bytes_output.write(output.getvalue().encode('utf-8'))
    bytes_output.seek(0)

    filename = f"mvai_export_{customer['name']}_{datetime.now().strftime('%Y%m%d')}.csv"

    return send_file(
        bytes_output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

@app.route('/customer/search')
@login_required
def customer_search():
    """Zoek in eigen logs"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))

    customer_id = session['customer_id']
    query = request.args.get('q', '')

    if query:
        logs = db.search_logs(query, customer_id=customer_id)
    else:
        logs = []

    customer = db.get_customer_by_id(customer_id)

    return render_template('customer_search.html',
                         customer=customer,
                         logs=logs,
                         query=query)

@app.route('/customer/analytics')
@login_required
def customer_analytics():
    """Advanced analytics dashboard voor klant"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))

    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)

    # Haal analytics op
    analytics_data = analytics.get_customer_analytics(customer_id, days=30)
    predictions = analytics.get_customer_predictions(customer_id)

    return render_template('customer_analytics.html',
                         customer=customer,
                         analytics=analytics_data,
                         predictions=predictions)

@app.route('/customer/api-keys')
@login_required
def customer_api_keys():
    """API key management voor klant"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))

    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)
    api_keys = db.get_customer_api_keys(customer_id)

    return render_template('customer_api_keys.html',
                         customer=customer,
                         api_keys=api_keys)

@app.route('/customer/api-keys/create', methods=['POST'])
@login_required
def customer_create_api_key():
    """Maak nieuwe API key aan"""
    if 'admin' in session:
        return jsonify({"error": "Admin kan niet customer API keys aanmaken"}), 403

    customer_id = session['customer_id']
    name = request.form.get('name', 'Default API Key')

    key_value = db.create_api_key(customer_id, name)

    # Log actie
    db.log_admin_action(
        admin_username=f'customer_{customer_id}',
        action='create_api_key',
        target_type='api_key',
        details=f'Created API key: {name}',
        ip_address=get_client_ip()
    )

    flash(f'API Key aangemaakt: {key_value}', 'success')
    return redirect(url_for('customer_api_keys'))

@app.route('/customer/api-keys/<int:key_id>/revoke', methods=['POST'])
@login_required
def customer_revoke_api_key(key_id):
    """Revoke API key"""
    if 'admin' in session:
        return jsonify({"error": "Admin moet admin panel gebruiken"}), 403

    customer_id = session['customer_id']

    # Verifieer ownership
    api_keys = db.get_customer_api_keys(customer_id)
    if not any(k['id'] == key_id for k in api_keys):
        return jsonify({"error": "API key niet gevonden"}), 404

    db.revoke_api_key(key_id)

    # Log actie
    db.log_admin_action(
        admin_username=f'customer_{customer_id}',
        action='revoke_api_key',
        target_type='api_key',
        target_id=key_id,
        ip_address=get_client_ip()
    )

    return jsonify({"success": True}), 200

# ═══════════════════════════════════════════════════════
# ADMIN ROUTES
# ═══════════════════════════════════════════════════════

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard met overzicht alle data"""
    stats = db.get_admin_stats()
    customers = db.get_all_customers()
    recent_logs = db.get_all_logs(limit=10)

    return render_template('admin_dashboard.html',
                         stats=stats,
                         customers=customers,
                         recent_logs=recent_logs)

@app.route('/admin/customers')
@admin_required
def admin_customers():
    """Overzicht alle klanten"""
    customers = db.get_all_customers()
    return render_template('admin_customers.html', customers=customers)

@app.route('/admin/customer/<int:customer_id>')
@admin_required
def admin_customer_detail(customer_id):
    """Detail pagina voor specifieke klant"""
    customer = db.get_customer_by_id(customer_id)
    if not customer:
        flash('Klant niet gevonden', 'error')
        return redirect(url_for('admin_customers'))

    stats = db.get_customer_stats(customer_id)
    logs = db.get_customer_logs(customer_id, limit=50)

    return render_template('admin_customer_detail.html',
                         customer=customer,
                         stats=stats,
                         logs=logs)

@app.route('/admin/customer/create', methods=['GET', 'POST'])
@admin_required
def admin_create_customer():
    """Maak nieuwe klant aan"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        contact_email = request.form.get('contact_email', '').strip()
        company_info = request.form.get('company_info', '').strip()

        if not name:
            flash('Bedrijfsnaam is verplicht', 'error')
            return render_template('admin_create_customer.html')

        try:
            customer = db.create_customer(name, contact_email, company_info)

            # Log admin actie
            db.log_admin_action(
                admin_username=session.get('admin_username', 'admin'),
                action='create_customer',
                target_type='customer',
                target_id=customer['id'],
                details=f'Created customer: {name}',
                ip_address=get_client_ip()
            )

            flash(f'Klant {name} aangemaakt! Access code: {customer["access_code"]}', 'success')
            return redirect(url_for('admin_customer_detail', customer_id=customer['id']))
        except Exception as e:
            flash(f'Fout bij aanmaken: {str(e)}', 'error')

    return render_template('admin_create_customer.html')

@app.route('/admin/customer/<int:customer_id>/toggle-status', methods=['POST'])
@admin_required
def admin_toggle_customer_status(customer_id):
    """Toggle customer status (active/inactive)"""
    customer = db.get_customer_by_id(customer_id)
    if not customer:
        return jsonify({"error": "Klant niet gevonden"}), 404

    new_status = 'inactive' if customer['status'] == 'active' else 'active'
    db.update_customer_status(customer_id, new_status)

    # Log admin actie
    db.log_admin_action(
        admin_username=session.get('admin_username', 'admin'),
        action='toggle_customer_status',
        target_type='customer',
        target_id=customer_id,
        details=f'Changed status to {new_status} for {customer["name"]}',
        ip_address=get_client_ip()
    )

    return jsonify({
        "status": "success",
        "new_status": new_status
    })

@app.route('/admin/logs')
@admin_required
def admin_all_logs():
    """Bekijk alle logs van alle klanten"""
    page = request.args.get('page', 1, type=int)
    limit = 50
    offset = (page - 1) * limit

    logs = db.get_all_logs(limit=limit, offset=offset)

    return render_template('admin_logs.html',
                         logs=logs,
                         page=page)

@app.route('/admin/search')
@admin_required
def admin_search():
    """Zoek klanten en logs"""
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'customers')

    if query:
        if search_type == 'customers':
            results = db.search_customers(query)
        else:
            results = db.search_logs(query)
    else:
        results = []

    return render_template('admin_search.html',
                         results=results,
                         query=query,
                         search_type=search_type)

@app.route('/admin/export/all-csv')
@admin_required
def admin_export_all_csv():
    """Export alle data naar CSV"""
    logs = db.get_all_logs(limit=100000)

    # Maak CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(['ID', 'Customer', 'Timestamp', 'IP Address', 'Data'])

    # Data
    for log in logs:
        writer.writerow([
            log['id'],
            log.get('customer_name', 'Unknown'),
            log['timestamp'],
            log['ip_address'],
            log['data']
        ])

    # Converteer naar bytes
    output.seek(0)
    bytes_output = io.BytesIO()
    bytes_output.write(output.getvalue().encode('utf-8'))
    bytes_output.seek(0)

    filename = f"mvai_admin_export_{datetime.now().strftime('%Y%m%d')}.csv"

    return send_file(
        bytes_output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

# ═══════════════════════════════════════════════════════
# API ENDPOINTS (voor toekomstige features)
# ═══════════════════════════════════════════════════════

@app.route('/api/stats')
@login_required
def api_stats():
    """API endpoint voor statistieken (JSON)"""
    if 'admin' in session:
        stats = db.get_admin_stats()
    else:
        customer_id = session['customer_id']
        stats = db.get_customer_stats(customer_id)

    return jsonify(stats)

# ═══════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error_code=404, message="Pagina niet gevonden"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error_code=500, message="Server fout"), 500

# ═══════════════════════════════════════════════════════
# STARTUP
# ═══════════════════════════════════════════════════════

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
