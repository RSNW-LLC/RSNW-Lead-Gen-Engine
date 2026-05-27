import mss
import pytesseract
from PIL import Image
import ollama
import os
import time
import sys

# Generic name for the process
PROCESS_NAME = "system_monitor"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_ocr_text(region):
    """Captures a specific part of the screen and extracts text."""
    try:
        with mss.mss() as sct:
            screenshot = sct.grab(region)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            text = pytesseract.image_to_string(img)
            return text
    except Exception as e:
        return f"Error: {e}"

def generate_solution(text):
    """Sends extracted text to local AI for a solution."""
    if len(text.strip()) < 20:
        return None

    try:
        # Prompt optimized for manual typing (concise, clear)
        prompt = f"Analyze the following task and provide a clean, concise coding solution. Format it so it is easy for a human to read and type manually. Avoid unnecessary boilerplate:\n\n{text}"
        response = ollama.generate(model='llama3', prompt=prompt)
        return response['response']
    except Exception as e:
        return f"AI Error: {e}"

def main():
    # SETUP REGION: (top, left, width, height)
    # You MUST adjust these to match your screen layout
    # Use a tool like 'GIMP' or 'Screenshot' to find your X/Y coordinates
    capture_region = {"top": 150, "left": 100, "width": 900, "height": 700}
    
    clear_screen()
    print(f"[{PROCESS_NAME}] Service Started.")
    print("-" * 30)
    print(f"[*] Target Region: {capture_region}")
    print("[*] Monitoring screen for tasks...")
    print("[!] Press Ctrl+C to safely terminate.")
    
    last_text = ""
    
    while True:
        try:
            # 1. Capture and Read
            current_text = get_ocr_text(capture_region)
            
            # 2. Only trigger if the text is new and looks like a task
            # (Checking first 50 chars to see if the page content shifted)
            if current_text[:50] != last_text[:50] and len(current_text) > 50:
                last_text = current_text
                
                print("\n" + "="*60)
                print("NEW TASK DETECTED. GENERATING...")
                print("="*60)
                
                solution = generate_solution(current_text)
                
                if solution:
                    clear_screen()
                    print(f"[{PROCESS_NAME}] SOLUTION READY:")
                    print("-" * 60)
                    print(solution)
                    print("-" * 60)
                    print("\n[*] Waiting for screen change or next task...")
            
            # 3. Frequency: Check every 5 seconds to stay stealthy
            time.sleep(5)
            
        except KeyboardInterrupt:
            print(f"\n[{PROCESS_NAME}] Service Terminated.")
            sys.exit()

if __name__ == "__main__":
    main()
