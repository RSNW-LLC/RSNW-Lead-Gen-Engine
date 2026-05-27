import mss
import pytesseract
from PIL import Image
import ollama
from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import os
import socket

app = Flask(__name__)
CORS(app)

# Global variables to store the latest task and solution
latest_solution = "Waiting for task..."

# REGION: (top, left, width, height) - Adjust to your screen!
# You MUST change these to match where the task text is on your screen
CAPTURE_REGION = {"top": 150, "left": 100, "width": 1200, "height": 800}

def get_solution():
    global latest_solution
    last_text = ""
    
    while True:
        try:
            with mss.mss() as sct:
                screenshot = sct.grab(CAPTURE_REGION)
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                text = pytesseract.image_to_string(img)
                
                # Only trigger if the text is significant and new
                if len(text.strip()) > 50 and text[:50] != last_text[:50]:
                    last_text = text[:50]
                    print("[WinSystemTimer] Syncing with server...")
                    
                    prompt = (
                        "Provide a concise coding solution for the following task. "
                        "Format it so it is easy for a human to read and type manually. "
                        "Avoid unnecessary boilerplate:\n\n" + text
                    )
                    
                    response = ollama.generate(model='llama3', prompt=prompt)
                    latest_solution = response['response']
            
            time.sleep(10) # Check every 10 seconds to stay stealthy
        except Exception as e:
            latest_solution = f"Error: {e}"
            time.sleep(5)

@app.after_request
def remove_header(response):
    # Remove identifying headers to harden the service
    response.headers['Server'] = 'WinSystemSvc'
    return response

@app.route('/')
def home():
    # Simple HTML page for your phone
    # Auto-refreshes every 5 seconds
    return f"""
    <html>
    <head>
        <title>WinSystemTimer Status</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                padding: 20px; 
                background: #121212; 
                color: #e0e0e0; 
                line-height: 1.6; 
            }}
            pre {{ 
                background: #1e1e1e; 
                padding: 15px; 
                border-radius: 8px; 
                white-space: pre-wrap; 
                border-left: 4px solid #00ff00;
                font-size: 14px;
            }}
            h1 {{ 
                color: #00ff00; 
                font-size: 1.1rem; 
                text-transform: uppercase;
                letter-spacing: 2px;
            }}
            .timestamp {{
                color: #666;
                font-size: 0.8rem;
                margin-bottom: 10px;
            }}
        </style>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h1>System Monitor: Active</h1>
        <div class="timestamp">Last Updated: {time.strftime('%H:%M:%S')}</div>
        <hr style="border: 0; border-top: 1px solid #333; margin-bottom: 20px;">
        <pre>{latest_solution}</pre>
    </body>
    </html>
    """

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':
    local_ip = get_local_ip()
    print("\n" + "="*50)
    print("      WIN SYSTEM TIMER: STEALTH SERVICE")
    print("="*50)
    print(f"[*] Access URL on your PHONE: http://{local_ip}:5000")
    print("[*] Monitoring Region:", CAPTURE_REGION)
    print("[!] Ensure Ollama is running (ollama serve)")
    print("="*50 + "\n")

    # Start the background screen-watcher thread
    threading.Thread(target=get_solution, daemon=True).start()
    
    # Start the web server
    # Running on 0.0.0.0 makes it accessible from other devices on the same Wi-Fi
    app.run(host='0.0.0.0', port=5000, debug=False)
