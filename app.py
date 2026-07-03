import time
import random
import threading
import os
from flask import Flask, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# ---------- CONFIG ----------
SIMULATION = os.environ.get('SIMULATION', 'True').lower() == 'true'
# SERIAL_PORT not needed in cloud – simulation only

# ---------- UPS STATE ----------
lock = threading.Lock()
state = { ... }   # same as before
history = { ... } # same as before

# ... (update_simulation function unchanged) ...

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    with lock:
        return jsonify({"live": state, "history": history})

@app.route('/api/set_grid', methods=['POST'])
def set_grid():
    global grid_connected
    grid_connected = not grid_connected
    return jsonify({"grid_connected": grid_connected})

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    if SIMULATION:
        print("🚀 Running SIMULATION mode (cloud)")
        threading.Thread(target=update_simulation, daemon=True).start()
    else:
        # Real serial would go here
        pass
    # Use Gunicorn in production; this is only for local testing
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)