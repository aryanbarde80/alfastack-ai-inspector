import requests
import time
import threading
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy", 
        "service": "AlfaStack AI",
        "timestamp": time.time(),
        "message": "Server is running"
    }), 200

@app.route('/')
def home():
    return jsonify({
        "message": "AlfaStack AI Health Monitor",
        "endpoints": {
            "health": "/health",
            "docs": "https://github.com/your-repo"
        }
    }), 200

def ping_render_app():
    """Ping the main Streamlit app every 14 minutes"""
    while True:
        try:
            response = requests.get("https://alfastack-ai-inspector.onrender.com", timeout=10)
            print(f"✅ Ping successful - Status: {response.status_code} - {time.ctime()}")
        except Exception as e:
            print(f"❌ Ping failed: {e}")
        time.sleep(840)  # 14 minutes

if __name__ == "__main__":
    print("🚀 Starting AlfaStack Health Monitor...")
    
    # Start ping service in background
    ping_thread = threading.Thread(target=ping_render_app, daemon=True)
    ping_thread.start()
    
    print("✅ Health monitor started. Pinging every 14 minutes...")
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5000, debug=False)
