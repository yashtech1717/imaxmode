"""
AURA // Minimalist Dark Text Canvas Launcher (with Mobile Network Access)
Run with: python run.py
"""
import os
import uvicorn
import webbrowser
import threading
import time
import socket

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    local_ip = get_local_ip()
    port = 8000
    
    print("=" * 65)
    print("✦ AURA // CINEMATIC TEXT CANVAS")
    print(f"💻 On this PC:    http://127.0.0.1:{port} or http://localhost:{port}")
    print(f"📱 On your Mobile: http://{local_ip}:{port}")
    print("   (Ensure your phone and PC are connected to the same Wi-Fi)")
    print("=" * 65)
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Bind to 0.0.0.0 so mobile phones on local Wi-Fi can connect
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
