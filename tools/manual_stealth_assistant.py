import mss
import pytesseract
from PIL import Image
import ollama
from flask import Flask
import threading
import time
import os
import socket
from pynput import keyboard

# --- CONFIGURATION ---
PROCESS_NAME = "WinSystemTask"
CAPTURE_REGION = {"top": 150, "left": 100, "width": 1200, "height": 800}
PORT = 5000

app = Flask(__name__)
latest_solution = "Press F9 on your laptop to analyze the screen."

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        return s.getsockname()[0]
    except:
        return '127.0.0.1'
    finally:
        s.close()

# --- OCR & AI LOGIC ---
def trigger_analysis():
    global latest_solution
    latest_solution = "Analysing... please wait."
    print(f"[{time.strftime('%H:%M:%S')}] F9 Pressed: Scanning screen...")
    
    try:
        with mss.mss() as sct:
            screenshot = sct.grab(CAPTURE_REGION)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            text = pytesseract.image_to_string(img)
            
            if len(text.strip()) < 20:
                latest_solution = "No readable text found in the capture zone."
                return

            prompt = f"Solve this coding task concisely for manual typing:\n\n{text}"
            response = ollama.generate(model='llama3', prompt=prompt)
            latest_solution = response['response']
            print(f"[{time.strftime('%H:%M:%S')}] Done! Solution sent to phone.")

    except Exception as e:
        latest_solution = f"Error: {e}"

# --- KEYBOARD LISTENER ---
def on_press(key):
    try:
        if key == keyboard.Key.f9:
            # Run analysis in a separate thread so it doesn't block the listener
            threading.Thread(target=trigger_analysis).start()
        
        if key == keyboard.Key.f12:
            print("Exiting...")
            os._exit(0) # Hard exit
    except:
        pass

# --- WEB SERVER ---
@app.route('/')
def home():
    return f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; padding: 20px; background: #000; color: #0F0; line-height: 1.6; }}
            pre {{ background: #111; padding: 15px; border-radius: 8px; white-space: pre-wrap; border: 1px solid #0F0; }}
            h1 {{ font-size: 1rem; color: #0F0; text-transform: uppercase; }}
        </style>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h1>SYS_MONITOR: READY</h1>
        <hr color="#0F0">
        <pre>{latest_solution}</pre>
    </body>
    </html>
    """

if __name__ == '__main__':
    print(f"\n{'='*40}")
    print(f"  {PROCESS_NAME} - ON DEMAND STEALTH")
    print(f"{'='*40}")
    print(f"1. Open on phone: http://{get_local_ip()}:{PORT}")
    print(f"2. Press F9 on laptop to get an answer.")
    print(f"3. Press F12 to kill this process.")
    print(f"{'='*40}\n")

    # Start keyboard listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Start Web Server
    app.run(host='0.0.0.0', port=PORT, debug=False)
