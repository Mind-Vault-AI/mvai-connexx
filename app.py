"""
MVAI Connexx - Multi-Tenant Enterprise Platform
Flask applicatie met authentication en customer management
"""
import os
import json
import logging
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import database as db
import analytics
import csv
import io
from config import Config

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mvai-connexx')

app = Flask(__name__)

# Secret key validation for production (before loading config)
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    if os.environ.get('FLASK_ENV') == 'development':
        app.secret_key = 'dev-secret-key-ONLY-FOR-LOCAL-DEV'
        logger.warning("⚠️ WARNING: Using development secret key - DO NOT USE IN PRODUCTION")
    else:
        raise RuntimeError("SECRET_KEY environment variable is required in production!")

# Load other config settings from Config class
app.config.from_object(Config)

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Rate limiting voor API protection
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# ═══════════════════════════════════════════════════════
# DATA DIRECTORY INITIALIZATION
# ═══════════════════════════════════════════════════════

def ensure_data_dir():
    """Zorg ervoor dat data directory bestaat voor persistent storage"""
    db_path = os.environ.get('DATABASE_PATH', 'mvai_connexx.db')
    data_dir = os.path.dirname(db_path)
    
    # Alleen maken als er een directory path is (niet bij relatief pad zoals '.' of '')
    if data_dir and data_dir != '.' and not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir, mode=0o755, exist_ok=True)
            logger.info(f"✓ Data directory aangemaakt: {data_dir}")
        except Exception as e:
            logger.error(f"⚠ Kon data directory niet aanmaken: {e}")
            logger.error("  → Check of DATABASE_PATH environment variabele correct is ingesteld")

# Zorg ervoor dat data directory bestaat (voor Gunicorn compatibiliteit)
ensure_data_dir()

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
# HEALTH CHECK ENDPOINT (voor Fly.io monitoring)
# ═══════════════════════════════════════════════════════

@app.route('/health')
def health():
    """Basic liveness probe voor Fly.io - geen database check"""
    return jsonify({"status": "healthy", "service": "mvai-connexx"}), 200

# ═══════════════════════════════════════════════════════
# PUBLIC ROUTES
# ═══════════════════════════════════════════════════════

@app.route('/')
def index():
    """Professional landing page voor MVAI Connexx platform"""
    # Redirect ingelogde gebruikers naar hun dashboard
    if 'customer_id' in session:
        return redirect(url_for('customer_dashboard'))
    elif 'admin' in session:
        return redirect(url_for('admin_dashboard'))

    # Toon luxury landing page voor nieuwe bezoekers
    return render_template('landing.html')

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
# AI ASSISTANT ROUTES
# ═══════════════════════════════════════════════════════

@app.route('/customer/ai')
@login_required
def customer_ai_assistant():
    """AI Assistant dashboard voor klant"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))

    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)
    ai_enabled = customer.get('ai_assistant_enabled', False)

    suggestions = []
    conversations = []

    if ai_enabled:
        from ai_assistant import get_assistant
        assistant = get_assistant(customer_id)
        suggestions = assistant.get_proactive_suggestions()

        # Load recent conversations
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_message, ai_response, timestamp
                FROM ai_conversations
                WHERE customer_id = ?
                ORDER BY timestamp DESC
                LIMIT 10
            ''', (customer_id,))
            conversations = [dict(row) for row in cursor.fetchall()]
            conversations.reverse()  # Show oldest first

    return render_template('customer_ai_assistant.html',
                         customer=customer,
                         ai_enabled=ai_enabled,
                         suggestions=suggestions,
                         conversations=conversations)

@app.route('/customer/ai/activate', methods=['POST'])
@login_required
def customer_ai_activate():
    """Activeer AI Assistant voor klant"""
    if 'admin' in session:
        return jsonify({"error": "Admin kan niet AI activeren"}), 403

    customer_id = session['customer_id']

    from ai_assistant import enable_assistant
    enable_assistant(customer_id)

    # Log actie
    db.log_admin_action(
        admin_username=f'customer_{customer_id}',
        action='activate_ai_assistant',
        target_type='customer',
        target_id=customer_id,
        details='Activated AI Assistant',
        ip_address=get_client_ip()
    )

    return jsonify({"success": True}), 200

@app.route('/customer/ai/chat', methods=['POST'])
@login_required
def customer_ai_chat():
    """Verwerk AI chat commando"""
    if 'admin' in session:
        return jsonify({"error": "Admin kan niet AI chat gebruiken"}), 403

    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)

    if not customer.get('ai_assistant_enabled', False):
        return jsonify({"error": "AI Assistant niet geactiveerd"}), 403

    message = request.json.get('message', '').strip()

    if not message:
        return jsonify({"error": "Geen bericht"}), 400

    from ai_assistant import get_assistant
    assistant = get_assistant(customer_id)

    # Process command
    result = assistant.process_command(message)

    # Save conversation
    with db.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ai_conversations (customer_id, user_message, ai_response, intent)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, message, result['message'], result.get('intent', 'unknown')))

    return jsonify(result)

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
# ENTERPRISE ADMIN ROUTES
# ═══════════════════════════════════════════════════════

@app.route('/admin/enterprise')
@admin_required
def admin_enterprise_dashboard():
    """Enterprise-grade admin dashboard met ICT, Unit Economics, Lean Six Sigma & Marketing"""
    from monitoring import health_monitor
    from unit_economics import get_business_metrics, get_customer_grades
    from lean_six_sigma import track_system_quality_metrics, get_improvement_recommendations, _calculate_sigma_belt
    from marketing_intelligence import get_marketing_dashboard

    # Get all metrics
    health_status = health_monitor.get_overall_health()
    business_metrics = get_business_metrics()
    customer_grades = get_customer_grades()
    quality_metrics = track_system_quality_metrics(30)
    marketing_dashboard = get_marketing_dashboard()

    # Get active alerts
    from monitoring import get_active_alerts
    active_alerts = get_active_alerts()

    # Get improvement recommendations
    improvement_recommendations = get_improvement_recommendations()

    # Get growth strategies
    growth_strategies = marketing_dashboard['growth_strategies']

    return render_template('admin_enterprise_dashboard.html',
                         health_status=health_status,
                         business_metrics=business_metrics,
                         customer_grades=customer_grades,
                         quality_metrics=quality_metrics,
                         marketing_summary=marketing_dashboard['summary'],
                         active_alerts=active_alerts,
                         improvement_recommendations=improvement_recommendations,
                         growth_strategies=growth_strategies,
                         sigma_belt=_calculate_sigma_belt(quality_metrics['sigma_level']))

@app.route('/admin/ict-monitoring')
@admin_required
def admin_ict_monitoring():
    """ICT Monitoring dashboard met errors, alerts en incidents"""
    from monitoring import health_monitor, get_active_alerts, get_error_analytics, get_recent_errors
    from incident_response import incident_manager

    health_status = health_monitor.get_overall_health()
    active_alerts = get_active_alerts()
    error_analytics = get_error_analytics(30)
    recent_errors = get_recent_errors(50)
    active_incidents = incident_manager.get_active_incidents()

    return render_template('admin_ict_monitoring.html',
                         health_status=health_status,
                         active_alerts=active_alerts,
                         error_analytics=error_analytics,
                         recent_errors=recent_errors,
                         active_incidents=active_incidents)

@app.route('/admin/unit-economics')
@admin_required
def admin_unit_economics():
    """Unit Economics dashboard met MRR, LTV, CAC en profitability"""
    from unit_economics import get_business_metrics, get_customer_grades, get_cohort_analysis

    business_metrics = get_business_metrics()
    customer_grades = get_customer_grades()
    cohort_analysis = get_cohort_analysis(6)

    return render_template('admin_unit_economics.html',
                         business_metrics=business_metrics,
                         customer_grades=customer_grades,
                         cohort_analysis=cohort_analysis)

@app.route('/admin/lean-six-sigma')
@admin_required
def admin_lean_six_sigma():
    """Lean Six Sigma dashboard met quality metrics, DMAIC projects en improvements"""
    from lean_six_sigma import track_system_quality_metrics, get_dmaic_dashboard, pareto_analysis_defects

    quality_metrics = track_system_quality_metrics(30)
    dmaic_dashboard = get_dmaic_dashboard()
    pareto_analysis = pareto_analysis_defects(30)

    return render_template('admin_lean_six_sigma.html',
                         quality_metrics=quality_metrics,
                         dmaic_dashboard=dmaic_dashboard,
                         pareto_analysis=pareto_analysis)

@app.route('/admin/marketing')
@admin_required
def admin_marketing():
    """Marketing Intelligence dashboard met funnel, channels, segments en growth strategies"""
    from marketing_intelligence import get_marketing_dashboard

    marketing_dashboard = get_marketing_dashboard()

    return render_template('admin_marketing.html',
                         marketing_dashboard=marketing_dashboard)

@app.route('/admin/security')
@admin_required
def admin_security():
    """Security monitoring dashboard with threat detection and audit logs"""
    from security import get_security_dashboard
    
    security_dashboard = get_security_dashboard()
    
    return render_template('admin_security.html',
                         security_dashboard=security_dashboard)

@app.route('/admin/incident-response/execute-exit-strategy', methods=['POST'])
@admin_required
def admin_execute_exit_strategy():
    """Execute emergency exit strategy"""
    from incident_response import execute_emergency_exit_strategy

    reason = request.form.get('reason', 'Manual trigger by admin')

    result = execute_emergency_exit_strategy(reason)

    flash(f'Emergency exit strategy executed! Incident ID: {result["incident_id"]}', 'warning')
    return redirect(url_for('admin_ict_monitoring'))

@app.route('/admin/alert/<int:alert_id>/acknowledge', methods=['POST'])
@admin_required
def admin_acknowledge_alert(alert_id):
    """Acknowledge an alert"""
    from monitoring import acknowledge_alert

    success = acknowledge_alert(alert_id, session.get('admin_username', 'admin'))

    if success:
        return jsonify({"success": True}), 200
    return jsonify({"error": "Failed to acknowledge alert"}), 500

@app.route('/admin/alert/<int:alert_id>/resolve', methods=['POST'])
@admin_required
def admin_resolve_alert(alert_id):
    """Resolve an alert"""
    from monitoring import resolve_alert

    resolution_notes = request.form.get('notes', '')
    success = resolve_alert(alert_id, session.get('admin_username', 'admin'), resolution_notes)

    if success:
        flash('Alert resolved successfully', 'success')
        return redirect(url_for('admin_ict_monitoring'))

    flash('Failed to resolve alert', 'error')
    return redirect(url_for('admin_ict_monitoring'))

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

# ═══════════════════════════════════════════════════════
# LEGAL & PUBLIC PAGES
# ═══════════════════════════════════════════════════════

@app.route('/legal')
def legal_pages():
    """Legal pages: Terms, Privacy Policy, Disclaimer"""
    return render_template('legal.html')

