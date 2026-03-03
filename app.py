"""
MVAI Connexx - Multi-Tenant Enterprise Platform
Flask applicatie met authentication en customer management
"""
import os
import sys
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
from config import Config, ConfigValidator

# Import structured logging
from logging_config import configure_structured_logging, get_logger, LogEvents

# Configure structured logging BEFORE any logging happens
environment = os.getenv('FLASK_ENV', 'development')
logger = configure_structured_logging('mvai-connexx', environment)

# Log application startup
logger.info(
    LogEvents.APP_STARTUP,
    environment=environment,
    python_version=sys.version.split()[0],
    flask_version="3.0.0"
)

# Valideer configuratie bij startup
if environment == 'production':
    try:
        ConfigValidator.validate_config(Config, environment='production')
        logger.info(
            LogEvents.CONFIG_VALIDATION_PASSED,
            environment="production",
            status="success",
            required_vars=ConfigValidator.REQUIRED_FOR_PRODUCTION
        )
    except ValueError as e:
        logger.error(
            LogEvents.CONFIG_VALIDATION_FAILED,
            environment="production",
            status="failed",
            error_type=type(e).__name__,
            error_message=str(e),
            action="exit_application",
            exit_code=1
        )
        sys.exit(1)
else:
    try:
        ConfigValidator.validate_config(Config, environment='development')
        logger.info(
            LogEvents.CONFIG_VALIDATION_PASSED,
            environment="development",
            status="success"
        )
    except ValueError as e:
        logger.warning(
            LogEvents.CONFIG_VALIDATION_WARNING,
            environment="development",
            error_type=type(e).__name__,
            error_message=str(e),
            note="Development mode allows missing config"
        )

app = Flask(__name__)

# Load config first to get SECRET_KEY from config.py
app.config.from_object(Config)

# Secret key: Use environment variable or fallback to config.py
app.secret_key = os.environ.get('SECRET_KEY') or Config.SECRET_KEY

# In development mode only: generate random key if using default
# (Production validation prevents app from starting with default key)
if app.secret_key == Config.DEFAULT_SECRET_KEY and environment != 'production':
    import secrets
    app.secret_key = secrets.token_hex(32)
    logger.warning(
        "secret_key_generated",
        environment="development",
        reason="using_default_key",
        note="Sessions will reset on restart"
    )

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
# HEALTH CHECK ENDPOINT (voor Fly.io monitoring)
# ═══════════════════════════════════════════════════════

@app.route('/health')
def health():
    """Basic liveness probe voor Fly.io - geen database check"""
    logger.debug(
        LogEvents.APP_HEALTH_CHECK,
        endpoint="/health",
        status="healthy"
    )
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

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Aparte admin login pagina"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        access_code = request.form.get('access_code', '').strip()
        admin = db.verify_admin(access_code)
        if admin:
            session.permanent = True
            session['admin'] = True
            session['admin_username'] = admin['username']
            flash(f'Welkom Admin {admin["username"]}!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Ongeldige admin code', 'error')
    return render_template('admin_login.html')

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

@app.route('/customer/ai/providers')
@login_required
def customer_ai_providers():
    """AI Provider beheer pagina voor klant (BYOK)"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))

    import json as _json
    from ai_providers import PROVIDERS, get_customer_provider_config

    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)
    current_config = get_customer_provider_config(customer_id)

    return render_template(
        'customer_ai_providers.html',
        customer=customer,
        providers=PROVIDERS,
        providers_json=_json.dumps(PROVIDERS),
        current_config=current_config
    )


@app.route('/customer/ai/providers/save', methods=['POST'])
@login_required
def customer_ai_providers_save():
    """Sla AI provider configuratie op voor klant"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))

    from ai_providers import save_customer_provider_config

    customer_id = session['customer_id']
    provider = request.form.get('provider', 'openai')
    model = request.form.get('model', '')
    api_key = request.form.get('api_key', '').strip() or None

    try:
        save_customer_provider_config(customer_id, provider, model, api_key)
        flash('AI provider instellingen opgeslagen!', 'success')
    except Exception as e:
        flash(f'Fout bij opslaan: {str(e)}', 'error')

    return redirect(url_for('customer_ai_providers'))


@app.route('/customer/ai/providers/test', methods=['POST'])
@login_required
def customer_ai_providers_test():
    """Test AI provider verbinding"""
    if 'admin' in session:
        return jsonify({"success": False, "message": "Admin heeft geen AI providers"}), 403

    from ai_providers import test_provider_config, get_customer_provider_config, decrypt_api_key

    customer_id = session['customer_id']
    data = request.get_json() or {}

    provider = data.get('provider', 'openai')
    model = data.get('model', '')
    api_key = data.get('api_key', '').strip()

    # Als geen key opgegeven, gebruik opgeslagen klant key
    if not api_key:
        config_row = get_customer_provider_config(customer_id)
        if config_row and config_row.get('api_key_encrypted'):
            try:
                api_key = decrypt_api_key(config_row['api_key_encrypted'])
            except Exception:
                pass

    if not api_key:
        return jsonify({"success": False, "message": "Geen API key beschikbaar om te testen"}), 400

    result = test_provider_config(provider, api_key, model)
    return jsonify(result)


@app.route('/customer/ai/providers/delete-key', methods=['POST'])
@login_required
def customer_ai_providers_delete_key():
    """Verwijder klant API key"""
    if 'admin' in session:
        return jsonify({"success": False}), 403

    from ai_providers import delete_customer_api_key

    customer_id = session['customer_id']
    delete_customer_api_key(customer_id)
    return jsonify({"success": True})


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

    # Process with OpenAI-powered chat (fallback to rule-based if OpenAI unavailable)
    result = assistant.chat(message)

    # Save conversation
    with db.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ai_conversations (customer_id, user_message, ai_response, intent)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, message, result['message'], result.get('intent', 'ai_chat')))

    return jsonify(result)

# ═══════════════════════════════════════════════════════
# SUBSCRIPTION & BILLING ROUTES
# ═══════════════════════════════════════════════════════

@app.route('/customer/subscription')
@login_required
def customer_subscription():
    """Subscription management pagina voor klanten"""
    if 'admin' in session:
        flash('Admin heeft geen subscription', 'error')
        return redirect(url_for('admin_dashboard'))

    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)

    # Import pricing tiers
    from unit_economics import PricingConfig
    pricing_tiers = PricingConfig.PRICING_TIERS

    # Get current tier details
    current_tier = customer.get('pricing_tier', 'demo')
    tier_details = pricing_tiers.get(current_tier, pricing_tiers['demo'])

    # Get current usage
    with db.get_db() as conn:
        cursor = conn.cursor()
        # Get logs count for current month
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM logs
            WHERE customer_id = ?
              AND timestamp >= date('now', 'start of month')
        ''', (customer_id,))
        current_usage = cursor.fetchone()['count']

    # Calculate usage percentage
    included_logs = tier_details['included_logs']
    usage_percentage = min(100, (current_usage / included_logs * 100) if included_logs > 0 else 0)

    usage = {
        'current': current_usage,
        'limit': included_logs,
        'percentage': round(usage_percentage, 1)
    }

    return render_template('customer_subscription.html',
                         current_tier=current_tier,
                         tier_details=tier_details,
                         pricing_tiers=pricing_tiers,
                         usage=usage,
                         customer=customer)

@app.route('/customer/upgrade/<tier>')
@login_required
def customer_upgrade(tier):
    """Upgrade customer tier via Stripe checkout"""
    if 'admin' in session:
        flash('Admin heeft geen subscription', 'error')
        return redirect(url_for('admin_dashboard'))

    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)

    from unit_economics import PricingConfig
    pricing_tiers = PricingConfig.PRICING_TIERS

    # Validate tier
    if tier not in pricing_tiers:
        flash('Ongeldige tier geselecteerd', 'error')
        return redirect(url_for('customer_subscription'))

    current_tier = customer.get('pricing_tier', 'demo')
    current_price = pricing_tiers[current_tier]['price_per_month']
    new_price = pricing_tiers[tier]['price_per_month']

    # Check if this is actually an upgrade
    if new_price <= current_price:
        flash('Dit is geen upgrade. Gebruik downgrade voor een lager tier.', 'error')
        return redirect(url_for('customer_subscription'))

    # Redirect to Gumroad checkout (PayPal backend na $100)
    try:
        from gumroad_integration import get_checkout_url

        # Get Gumroad checkout URL met customer info
        checkout_url = get_checkout_url(
            tier=tier,
            customer_id=customer_id,
            customer_email=customer.get('contact_email')
        )

        # Redirect to Gumroad (→ PayPal after $100)
        return redirect(checkout_url)

    except Exception as e:
        print(f"❌ Gumroad checkout error: {e}")
        flash(f'Fout bij betalingsverwerking: {str(e)}', 'error')
        return redirect(url_for('customer_subscription'))

@app.route('/customer/downgrade/<tier>')
@login_required
def customer_downgrade(tier):
    """Downgrade customer tier"""
    if 'admin' in session:
        flash('Admin heeft geen subscription', 'error')
        return redirect(url_for('admin_dashboard'))

    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)

    from unit_economics import PricingConfig
    pricing_tiers = PricingConfig.PRICING_TIERS

    # Validate tier
    if tier not in pricing_tiers:
        flash('Ongeldige tier geselecteerd', 'error')
        return redirect(url_for('customer_subscription'))

    current_tier = customer.get('pricing_tier', 'demo')
    current_price = pricing_tiers[current_tier]['price_per_month']
    new_price = pricing_tiers[tier]['price_per_month']

    # Check if this is actually a downgrade
    if new_price >= current_price:
        flash('Dit is geen downgrade. Gebruik upgrade voor een hoger tier.', 'error')
        return redirect(url_for('customer_subscription'))

    # Update tier
    with db.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE customers
            SET pricing_tier = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (tier, customer_id))

    flash(f'Downgrade naar {tier.upper()} gepland voor einde van de billing cycle', 'success')
    return redirect(url_for('customer_subscription'))

@app.route('/webhooks/gumroad', methods=['POST'])
def gumroad_webhook():
    """Handle Gumroad webhook events (payment confirmation)"""
    payload = request.form.to_dict()  # Gumroad sends form data

    from gumroad_integration import verify_gumroad_webhook

    try:
        # Verify and process webhook
        result = verify_gumroad_webhook(payload)

        if not result.get('valid'):
            print(f"⚠️ Invalid Gumroad webhook: {payload}")
            return jsonify({'error': 'Invalid webhook data'}), 400

        # Payment successful - upgrade customer tier
        customer_id = result.get('customer_id')
        tier = result.get('tier')
        email = result.get('email')
        sale_id = result.get('sale_id')

        if customer_id and tier:
            # Update customer tier in database
            with db.get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE customers
                    SET pricing_tier = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (tier, int(customer_id)))

            # Send upgrade confirmation email
            try:
                customer = db.get_customer_by_id(int(customer_id))
                from email_notifications import send_tier_upgrade_email
                from unit_economics import PricingConfig

                old_tier = customer.get('pricing_tier', 'demo')
                new_price = PricingConfig.PRICING_TIERS[tier]['price_per_month']

                send_tier_upgrade_email(
                    customer['name'],
                    customer.get('contact_email'),
                    old_tier,
                    tier,
                    new_price
                )
            except Exception as e:
                print(f"⚠️ Upgrade email failed: {e}")

            print(f"✅ Gumroad sale {sale_id}: Customer {customer_id} upgraded to {tier}")

        return jsonify({'success': True}), 200

    except Exception as e:
        print(f"❌ Gumroad webhook processing error: {e}")
        return jsonify({'error': str(e)}), 400

# Stripe webhook (DISABLED - wacht op KVK voor activatie)
@app.route('/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events (DISABLED TOT KVK)"""
    # TODO: Activeer zodra KVK nummer er is
    return jsonify({'error': 'Stripe disabled - waiting for KVK'}), 503

    # Originele Stripe code (behouden voor later):
    payload = request.get_data(as_text=True)
    signature = request.headers.get('Stripe-Signature')

    from stripe_integration import handle_webhook

    try:
        # Verify and process webhook
        result = handle_webhook(payload, signature)

        if not result:
            return jsonify({'error': 'Invalid signature'}), 400

        # Handle different webhook events
        if result['action'] == 'activate_subscription':
            # Payment successful - upgrade customer tier
            customer_id = int(result['customer_id'])
            tier = result['tier']
            stripe_customer_id = result.get('stripe_customer_id')

            # Update customer tier in database
            with db.get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE customers
                    SET pricing_tier = ?,
                        stripe_customer_id = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (tier, stripe_customer_id, customer_id))

            # Send upgrade confirmation email
            try:
                customer = db.get_customer_by_id(customer_id)
                from email_notifications import send_tier_upgrade_email
                from unit_economics import PricingConfig

                old_tier = customer.get('pricing_tier', 'demo')
                new_price = PricingConfig.PRICING_TIERS[tier]['price_per_month']

                send_tier_upgrade_email(
                    customer['name'],
                    customer.get('contact_email'),
                    old_tier,
                    tier,
                    new_price
                )
            except Exception as e:
                print(f"⚠️ Upgrade email failed: {e}")

            print(f"✅ Subscription activated for customer {customer_id} -> {tier}")

        elif result['action'] == 'cancel_subscription':
            # Subscription canceled - downgrade to demo
            customer_id = int(result['customer_id'])

            with db.get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE customers
                    SET pricing_tier = 'demo',
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (customer_id,))

            print(f"⚠️ Subscription canceled for customer {customer_id}")

        elif result['action'] == 'payment_failed':
            # Payment failed - send warning email
            customer_id = int(result['customer_id'])
            customer = db.get_customer_by_id(customer_id)

            try:
                from email_notifications import send_admin_alert
                send_admin_alert(
                    'Payment Failed',
                    f"Customer {customer['name']} (ID: {customer_id}) payment failed",
                    severity='HIGH'
                )
            except Exception as e:
                print(f"⚠️ Alert email failed: {e}")

        return jsonify({'success': True}), 200

    except Exception as e:
        print(f"❌ Webhook processing error: {e}")
        return jsonify({'error': str(e)}), 400

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


# ═══════════════════════════════════════════════════════
# SOCIAL LOGIN - GOOGLE & APPLE OAUTH2
# ═══════════════════════════════════════════════════════

def _setup_oauth():
    """Initialiseer OAuth clients als credentials beschikbaar zijn"""
    google_client_id = os.environ.get('GOOGLE_CLIENT_ID')
    if not google_client_id:
        return None
    try:
        from authlib.integrations.flask_client import OAuth
        oauth_inst = OAuth(app)
        oauth_inst.register(
            name='google',
            client_id=google_client_id,
            client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid email profile'},
        )
        apple_client_id = os.environ.get('APPLE_CLIENT_ID')
        if apple_client_id:
            oauth_inst.register(
                name='apple',
                client_id=apple_client_id,
                client_secret=os.environ.get('APPLE_CLIENT_SECRET'),
                authorize_url='https://appleid.apple.com/auth/authorize',
                access_token_url='https://appleid.apple.com/auth/token',
                client_kwargs={'scope': 'name email', 'response_mode': 'form_post'},
            )
        return oauth_inst
    except ImportError:
        return None

_oauth = _setup_oauth()


@app.route('/auth/google')
def auth_google():
    """Start Google OAuth2 flow"""
    if _oauth is None or not os.environ.get('GOOGLE_CLIENT_ID'):
        flash('Google login is niet geconfigureerd. Gebruik een access code.', 'error')
        return redirect(url_for('login'))
    redirect_uri = url_for('auth_google_callback', _external=True)
    return _oauth.google.authorize_redirect(redirect_uri)


@app.route('/auth/google/callback')
def auth_google_callback():
    """Verwerk Google OAuth2 callback"""
    if _oauth is None:
        return redirect(url_for('login'))
    try:
        token = _oauth.google.authorize_access_token()
        userinfo = token.get('userinfo') or _oauth.google.userinfo()
        email = userinfo.get('email')
        name = userinfo.get('name', email)
        provider_id = userinfo.get('sub')

        # Zoek bestaande social login
        customer = db.get_customer_by_social_login('google', provider_id)
        if not customer:
            # Probeer te matchen op email
            customer = db.get_customer_by_email(email)
            if customer:
                db.link_social_login(customer['id'], 'google', provider_id, email, name)
            else:
                flash(f'Geen account gevonden voor {email}. Vraag uw beheerder om een account.', 'error')
                return redirect(url_for('login'))
        else:
            db.link_social_login(customer['id'], 'google', provider_id, email, name)

        session.permanent = True
        session['customer_id'] = customer['id']
        session['customer_name'] = customer['name']
        flash(f'Welkom {customer["name"]}!', 'success')
        return redirect(url_for('customer_dashboard'))
    except Exception as e:
        flash('Google login mislukt. Probeer opnieuw.', 'error')
        return redirect(url_for('login'))


@app.route('/auth/apple', methods=['GET', 'POST'])
def auth_apple():
    """Start Apple Sign-In flow"""
    if _oauth is None or not os.environ.get('APPLE_CLIENT_ID'):
        flash('Apple login is niet geconfigureerd. Gebruik een access code.', 'error')
        return redirect(url_for('login'))
    redirect_uri = url_for('auth_apple_callback', _external=True)
    return _oauth.apple.authorize_redirect(redirect_uri)


@app.route('/auth/apple/callback', methods=['GET', 'POST'])
def auth_apple_callback():
    """Verwerk Apple Sign-In callback"""
    if _oauth is None:
        return redirect(url_for('login'))
    try:
        import jwt as _jwt
        token = _oauth.apple.authorize_access_token()
        id_token = token.get('id_token')
        claims = _jwt.decode(id_token, options={"verify_signature": False})
        email = claims.get('email')
        provider_id = claims.get('sub')

        customer = db.get_customer_by_social_login('apple', provider_id)
        if not customer:
            customer = db.get_customer_by_email(email) if email else None
            if customer:
                db.link_social_login(customer['id'], 'apple', provider_id, email)
            else:
                flash('Geen account gevonden. Vraag uw beheerder om een account.', 'error')
                return redirect(url_for('login'))
        else:
            db.link_social_login(customer['id'], 'apple', provider_id, email)

        session.permanent = True
        session['customer_id'] = customer['id']
        session['customer_name'] = customer['name']
        flash(f'Welkom {customer["name"]}!', 'success')
        return redirect(url_for('customer_dashboard'))
    except Exception as e:
        flash('Apple login mislukt. Probeer opnieuw.', 'error')
        return redirect(url_for('login'))


# ═══════════════════════════════════════════════════════
# ERP/WMS INTEGRATIES ROUTES
# ═══════════════════════════════════════════════════════

@app.route('/customer/integrations')
@login_required
def customer_integrations():
    """Integratie overzicht voor klant"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))
    import json as _json
    from integrations import INTEGRATION_CATALOG, INTEGRATION_CATEGORIES
    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)
    integrations = db.get_customer_integrations(customer_id)
    return render_template('customer_integrations.html',
                           customer=customer,
                           integrations=integrations,
                           catalog=INTEGRATION_CATALOG,
                           catalog_json=_json.dumps(INTEGRATION_CATALOG),
                           categories=INTEGRATION_CATEGORIES)


@app.route('/customer/integrations/connect', methods=['POST'])
@login_required
def customer_integration_connect():
    """Verbind nieuwe integratie"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))
    import json as _json
    from integrations import INTEGRATION_CATALOG, test_integration_connection
    customer_id = session['customer_id']
    integration_type = request.form.get('integration_type')
    name = request.form.get('name', integration_type)

    # Haal alle config_ velden op
    config = {}
    for key, val in request.form.items():
        if key.startswith('config_') and val:
            config[key[7:]] = val

    # Test verbinding
    result = test_integration_connection(integration_type, config)
    integration_id = db.create_integration(customer_id, integration_type, name, config)

    if result['success']:
        flash(f'✓ {name} succesvol verbonden. {result["message"]}', 'success')
    else:
        flash(f'⚠ Verbinding getest maar probleem gevonden: {result["message"]}', 'error')
    return redirect(url_for('customer_integrations'))


@app.route('/customer/integrations/<int:integration_id>/sync', methods=['POST'])
@login_required
def customer_integration_sync(integration_id):
    """Voer datasync uit voor integratie"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))
    import json as _json
    from integrations import sync_integration
    customer_id = session['customer_id']
    integrations = db.get_customer_integrations(customer_id)
    intg = next((i for i in integrations if i['id'] == integration_id), None)
    if not intg:
        flash('Integratie niet gevonden', 'error')
        return redirect(url_for('customer_integrations'))
    try:
        count = sync_integration(integration_id, intg['integration_type'], intg['config'], customer_id)
        flash(f'✓ Sync geslaagd: {count} records gesynchroniseerd', 'success')
    except Exception as e:
        flash(f'Sync mislukt: {str(e)[:100]}', 'error')
    return redirect(url_for('customer_integrations'))


@app.route('/customer/integrations/<int:integration_id>/delete', methods=['POST'])
@login_required
def customer_integration_delete(integration_id):
    """Verwijder integratie"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))
    customer_id = session['customer_id']
    db.delete_integration(integration_id, customer_id)
    flash('Integratie verwijderd', 'success')
    return redirect(url_for('customer_integrations'))


# ═══════════════════════════════════════════════════════
# OUTPUT MODULE - PDF, EMAIL, PRINT, WEBHOOKS
# ═══════════════════════════════════════════════════════

@app.route('/customer/export/pdf')
@login_required
def customer_export_pdf():
    """Exporteer klantlogs als PDF rapport"""
    if 'admin' in session:
        return jsonify({'error': 'Admin kan geen customer PDF exporteren'}), 403
    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)
    logs = db.get_customer_logs(customer_id, limit=500)

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.enums import TA_LEFT, TA_CENTER

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                leftMargin=2*cm, rightMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        story = []

        # Header
        title_style = ParagraphStyle('title', parent=styles['Heading1'],
                                     fontSize=18, textColor=colors.HexColor('#10b981'), spaceAfter=6)
        story.append(Paragraph('MVAI Connexx - Data Export', title_style))
        story.append(Paragraph(f'Klant: {customer["name"]}', styles['Normal']))
        story.append(Paragraph(f'Gegenereerd: {datetime.now().strftime("%d-%m-%Y %H:%M")}', styles['Normal']))
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(f'Totaal records: {len(logs)}', styles['Normal']))
        story.append(Spacer(1, 0.5*cm))

        # Tabel
        table_data = [['#', 'Tijdstip', 'IP', 'Data (beknopt)']]
        for log in logs[:200]:
            data_preview = str(log.get('data', ''))[:80]
            table_data.append([
                str(log['id']),
                str(log.get('timestamp', ''))[:16],
                str(log.get('ip_address', '')),
                data_preview
            ])

        t = Table(table_data, colWidths=[1.2*cm, 3.5*cm, 3.5*cm, None])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('FONTSIZE', (0,1), (-1,-1), 8),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#0a0a0a'), colors.HexColor('#111')]),
            ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor('#e0e0e0')),
            ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#333')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t)
        doc.build(story)
        buffer.seek(0)

        filename = f"mvai_rapport_{customer['name']}_{datetime.now().strftime('%Y%m%d')}.pdf"
        return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=filename)

    except Exception as e:
        flash(f'PDF generatie mislukt: {str(e)}', 'error')
        return redirect(url_for('customer_dashboard'))


@app.route('/customer/export/email', methods=['POST'])
@login_required
def customer_export_email():
    """Stuur data export per e-mail"""
    if 'admin' in session:
        return jsonify({'error': 'Admin kan dit niet uitvoeren'}), 403
    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)
    email = request.form.get('email') or customer.get('contact_email')
    if not email:
        flash('Geen e-mailadres opgegeven', 'error')
        return redirect(url_for('customer_dashboard'))
    try:
        from email_notifications import send_data_export_email
        logs = db.get_customer_logs(customer_id, limit=1000)
        send_data_export_email(customer['name'], email, logs)
        flash(f'✓ Export verzonden naar {email}', 'success')
    except Exception as e:
        flash(f'E-mail verzenden mislukt: {str(e)[:80]}', 'error')
    return redirect(url_for('customer_dashboard'))


@app.route('/customer/webhooks')
@login_required
def customer_webhooks():
    """Webhook beheer voor klant"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))
    customer_id = session['customer_id']
    customer = db.get_customer_by_id(customer_id)
    webhooks = db.get_customer_webhooks(customer_id)
    return render_template('customer_webhooks.html', customer=customer, webhooks=webhooks)


@app.route('/customer/webhooks/create', methods=['POST'])
@login_required
def customer_webhook_create():
    """Maak nieuwe webhook aan"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))
    customer_id = session['customer_id']
    name = request.form.get('name', 'Webhook')
    url = request.form.get('url', '').strip()
    events = request.form.get('events', 'all')
    if not url or not url.startswith('http'):
        flash('Ongeldige webhook URL', 'error')
        return redirect(url_for('customer_webhooks'))
    import secrets as _secrets
    secret = _secrets.token_hex(16)
    db.create_webhook(customer_id, name, url, secret, events)
    flash(f'✓ Webhook aangemaakt. Secret: {secret}', 'success')
    return redirect(url_for('customer_webhooks'))


@app.route('/customer/webhooks/<int:webhook_id>/delete', methods=['POST'])
@login_required
def customer_webhook_delete(webhook_id):
    """Verwijder webhook"""
    if 'admin' in session:
        return redirect(url_for('admin_dashboard'))
    customer_id = session['customer_id']
    db.delete_webhook(webhook_id, customer_id)
    flash('Webhook verwijderd', 'success')
    return redirect(url_for('customer_webhooks'))

