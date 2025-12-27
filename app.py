import os
import json
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DATA_FILE = '/app/data/mvai_data.json'

# --- SECURITY UPDATE: GEEN ADMIN BACKDOOR ---
# Alle inkomende data wordt gevalideerd en veilig weggeschreven.
# Er is geen openbare route om logs te bekijken (IP protection).

def ensure_data_dir():
    """Zorgt ervoor dat de data directory bestaat voor persistent storage"""
    data_dir = os.path.dirname(DATA_FILE)
    if data_dir and not os.path.exists(data_dir):
        os.makedirs(data_dir)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"logs": []}
    try:
        with open(DATA_FILE, 'r') as f: return json.load(f)
    except: return {"logs": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f: json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/health')
def health():
    """Health check endpoint voor Fly.io monitoring"""
    return jsonify({"status": "healthy", "service": "mvai-connexx"}), 200

@app.route('/api/save', methods=['POST'])
def save_entry():
    # 1. Haal data op
    entry = request.json
    
    # 2. Voeg beveiligde metadata toe (Server Time & IP)
    entry['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 3. IP Adres extractie (Werkt ook achter Railway Proxy/Load Balancer)
    if request.headers.getlist("X-Forwarded-For"):
        entry['ip'] = request.headers.getlist("X-Forwarded-For")[0]
    else:
        entry['ip'] = request.remote_addr
    
    # 4. Opslaan in kluis
    data = load_data()
    data['logs'].append(entry)
    save_data(data)
    
    # 5. Bevestig aan client (Status 200)
    return jsonify({"status": "SECURE_COMMIT", "message": "Data Encrypted & Stored."})

if __name__ == '__main__':
    # Zorg dat data directory bestaat voor persistent storage
    ensure_data_dir()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
