import os
import json
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DATA_FILE = 'mvai_data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"logs": [], "iso_compliance": True}
    try:
        with open(DATA_FILE, 'r') as f: return json.load(f)
    except: return {"logs": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f: json.dump(data, f, indent=4)

@app.route('/')
def index(): return render_template('dashboard.html')

@app.route('/api/save', methods=['POST'])
def save_entry():
    entry = request.json
    data = load_data()
    entry['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    data['logs'].append(entry)
    save_data(data)
    return jsonify({"status": "SAVED", "message": "Geborgd."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
