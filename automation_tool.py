import pyautogui
import cv2
import pytesseract
import os
import time
from datetime import datetime
import platform
from pynput import keyboard
import schedule
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from vosk import Model, KaldiRecognizer
import pyaudio
from transformers import pipeline
from ultralytics import YOLO
from urllib.parse import urlparse
import numpy as np

# Configuration
pyautogui.FAILSAFE = True  # Move mouse to top-left to abort
SAVE_PATH = "screenshots"
HOTKEY = "ctrl+shift+s"
INTERVAL = 600  # 10 minutes
TASKS_FILE = "tasks.json"
YOLO_MODEL_PATH = "yolo_ui_model.pt"  # YOLOv8 model
VOSK_MODEL_PATH = "vosk-model-small-en-us"  # Vosk model
VOICE_LISTENING = False  # Voice listening state

# Create save directory
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

# Initialize YOLO and NLP
yolo_model = YOLO(YOLO_MODEL_PATH) if os.path.exists(YOLO_MODEL_PATH) else None
nlp = pipeline("text-classification", model="distilbert-base-uncased")

# Function to take a screenshot
def take_screenshot(prefix="screenshot"):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{SAVE_PATH}/{prefix}_{timestamp}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print(f"Screenshot saved: {filename}")
        return filename
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        messagebox.showerror("Error", f"Screenshot failed: {e}")
        return None

# Function to open an application
def open_application(app_name):
    try:
        system = platform.system()
        if system == "Windows":
            if "chrome" in app_name.lower():
                os.system("start chrome")
            else:
                os.system(app_name)
        elif system == "Darwin":  # macOS
            if "chrome" in app_name.lower():
                os.system("open -a 'Google Chrome'")
            else:
                os.system(f"open -a {app_name}")
        elif system == "Linux":
            if "chrome" in app_name.lower():
                os.system("google-chrome")
            else:
                os.system(app_name)
        else:
            raise Exception("Unsupported OS")
        time.sleep(2)  # Wait for app to open
        print(f"Opened {app_name}")
    except Exception as e:
        print(f"Error opening application {app_name}: {e}")
        messagebox.showerror("Error", f"Failed to open {app_name}: {e}")

# Function to type text in the active application
def type_text(text):
    try:
        pyautogui.write(text)
        time.sleep(0.5)
        print(f"Typed: {text}")
    except Exception as e:
        print(f"Error typing text: {e}")
        messagebox.showerror("Error", f"Typing failed: {e}")

# AI navigation: Detect UI elements with YOLO
def detect_ui_elements(element_type, retries=3):
    if not yolo_model:
        print("YOLO model not loaded")
        messagebox.showerror("Error", "YOLO model not found")
        return False
    element_map = {
        "username_field": 0,  # Class IDs from data.yaml
        "password_field": 1,
        "login_button": 2
    }
    class_id = element_map.get(element_type)
    if class_id is None:
        print(f"Invalid element type: {element_type}")
        return False
    for attempt in range(retries):
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save("temp.png")
            img = cv2.imread("temp.png")
            results = yolo_model.predict(img)
            for result in results:
                for box in result.boxes:
                    if int(box.cls) == class_id:
                        x, y, w, h = box.xywh[0]
                        pyautogui.click(x + w / 2, y + h / 2)
                        print(f"Clicked {element_type} at ({x}, {y})")
                        os.remove("temp.png")
                        return True
            print(f"{element_type} not found (attempt {attempt + 1}/{retries})")
            time.sleep(1)
        except Exception as e:
            print(f"Error detecting {element_type} (attempt {attempt + 1}/{retries}): {e}")
        finally:
            if os.path.exists("temp.png"):
                os.remove("temp.png")
    messagebox.showerror("Error", f"{element_type} not found after retries")
    return False

# OCR: Read text from the screen
def read_screen_text():
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save("temp.png")
        text = pytesseract.image_to_string(cv2.imread("temp.png"))
        os.remove("temp.png")
        print(f"Screen text: {text}")
        messagebox.showinfo("Screen Text", text if text.strip() else "No text detected")
        return text
    except Exception as e:
        print(f"Error reading screen text: {e}")
        messagebox.showerror("Error", f"OCR failed: {e}")
        return ""

# Check for CAPTCHAs or pop-ups
def check_for_popups():
    try:
        text = read_screen_text()
        if any(keyword in text.lower() for keyword in ["captcha", "verify", "popup", "error"]):
            print("Detected potential CAPTCHA or popup")
            messagebox.showwarning("Warning", "Possible CAPTCHA or popup detected")
            pyautogui.press("esc")
            time.sleep(1)
            return True
        return False
    except Exception as e:
        print(f"Error checking for popups: {e}")
        return False

# Navigate to a URL
def navigate_to_url(url):
    try:
        pyautogui.hotkey("ctrl", "t")  # Open new tab
        time.sleep(0.5)
        pyautogui.write(url)
        pyautogui.press("enter")
        time.sleep(2)  # Wait for page to load
        print(f"Navigated to {url}")
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        messagebox.showerror("Error", f"Navigation failed: {e}")

# Log in to a website
def login_to_website(url, username=None, password=None):
    try:
        root = tk.Tk()
        root.withdraw()
        username = username or simpledialog.askstring("Input", "Enter username:", parent=root)
        password = password or simpledialog.askstring("Input", "Enter password:", show="*", parent=root)
        root.destroy()
        if not username or not password:
            raise Exception("Username or password not provided")

        open_application("chrome")
        navigate_to_url(url)
        
        check_for_popups()
        
        if detect_ui_elements("username_field"):
            time.sleep(0.5)
            pyautogui.write(username)
            print("Entered username")
        
        if detect_ui_elements("password_field"):
            time.sleep(0.5)
            pyautogui.write(password)
            print("Entered password")
        
        if detect_ui_elements("login_button"):
            time.sleep(1)
            print("Clicked login button")
            check_for_popups()
            take_screenshot("login")
        else:
            raise Exception("Login button not found")
        
        messagebox.showinfo("Success", f"Logged in to {url}")
    except Exception as e:
        print(f"Error logging in to {url}: {e}")
        messagebox.showerror("Error", f"Login failed: {e}")

# Execute tasks from JSON
def execute_tasks():
    try:
        if not os.path.exists(TASKS_FILE):
            raise Exception(f"{TASKS_FILE} not found")
        with open(TASKS_FILE, 'r') as f:
            tasks = json.load(f)
        
        for task in tasks:
            action = task.get("action")
            if action == "open":
                open_application(task.get("app", "notepad.exe"))
            elif action == "type":
                type_text(task.get("value", "Hello, AI!"))
            elif action == "screenshot":
                take_screenshot(task.get("prefix", "task"))
            elif action == "navigate":
                navigate_to_url(task.get("url"))
            elif action == "login":
                login_to_website(
                    task.get("url"),
                    task.get("username"),
                    task.get("password")
                )
            else:
                print(f"Unknown action: {action}")
        messagebox.showinfo("Success", "Tasks executed successfully")
    except Exception as e:
        print(f"Error executing tasks: {e}")
        messagebox.showerror("Error", f"Task execution failed: {e}")

# Parse voice commands with NLP
def parse_command(command):
    try:
        result = nlp(command)
        intent = result[0]["label"]
        if "open" in command.lower():
            if "chrome" in command.lower():
                return lambda: open_application("chrome")
            elif "notepad" in command.lower():
                return lambda: open_application("notepad.exe" if platform.system() == "Windows" else "TextEdit")
        elif "type" in command.lower():
            text = command.replace("type", "").strip() or "Hello from voice command!"
            return lambda: type_text(text)
        elif "screenshot" in command.lower():
            return lambda: take_screenshot("voice")
        elif "read text" in command.lower():
            return read_screen_text
        elif "execute tasks" in command.lower():
            return execute_tasks
        elif "go to" in command.lower():
            url = command.replace("go to", "").strip()
            if not url.startswith("http"):
                url = "https://" + url
            return lambda: navigate_to_url(url)
        elif "log in" in command.lower():
            url = "https://example.com"
            for word in command.split():
                if "." in word and not word.startswith("log"):
                    url = "https://" + word if not word.startswith("http") else word
            return lambda: login_to_website(url)
        elif "stop listening" in command.lower():
            return lambda: toggle_voice_listening(None)
        print(f"Unknown command: {command}")
        return None
    except Exception as e:
        print(f"Error parsing command: {e}")
        return None

# Voice command listener with Vosk
def voice_listener():
    global VOICE_LISTENING
    model = Model(VOSK_MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    while VOICE_LISTENING:
        try:
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                command = result.get("text", "").lower()
                if command:
                    print(f"Voice command: {command}")
                    action = parse_command(command)
                    if action:
                        action()
                    else:
                        messagebox.showinfo("Voice", f"Unknown command: {command}")
        except Exception as e:
            print(f"Voice listener error: {e}")
            messagebox.showerror("Error", f"Voice listener failed: {e}")

    stream.stop_stream()
    stream.close()
    p.terminate()

# Toggle voice listening
def toggle_voice_listening(label):
    global VOICE_LISTENING
    VOICE_LISTENING = not VOICE_LISTENING
    if VOICE_LISTENING:
        threading.Thread(target=voice_listener, daemon=True).start()
        if label:
            label.config(text="Voice Listening: ON")
        print("Voice listening started")
    else:
        if label:
            label.config(text="Voice Listening: OFF")
        print("Voice listening stopped")

# Manual screenshot via hotkey
def manual_screenshot():
    def on_hotkey():
        take_screenshot("manual")
        messagebox.showinfo("Screenshot", "Manual screenshot taken!")

    with keyboard.GlobalHotKeys({HOTKEY: on_hotkey}):
        while True:
            time.sleep(0.1)

# Automatic screenshot scheduler
def run_scheduler():
    schedule.every(INTERVAL).seconds.do(take_screenshot, prefix="auto")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Perform a sample task: Open app, type, screenshot
def perform_sample_task():
    try:
        open_application("notepad.exe" if platform.system() == "Windows" else "TextEdit")
        type_text("Hello, AI!")
        take_screenshot("sample_task")
        messagebox.showinfo("Success", "Sample task completed")
    except Exception as e:
        print(f"Error in sample task: {e}")
        messagebox.showerror("Error", f"Sample task failed: {e}")

# GUI
def create_gui():
    root = tk.Tk()
    root.title("AI Desktop Pilot")
    root.geometry("300x350")

    tk.Label(root, text="AI Desktop Pilot", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Perform Sample Task", command=perform_sample_task).pack(pady=5)
    tk.Button(root, text="Execute Tasks from JSON", command=execute_tasks).pack(pady=5)
    tk.Button(root, text="Take Screenshot", command=lambda: take_screenshot("manual")).pack(pady=5)
    tk.Button(root, text="Read Screen Text", command=read_screen_text).pack(pady=5)
    tk.Button(root, text="Log in to Website", command=lambda: login_to_website("https://example.com")).pack(pady=5)
    voice_label = tk.Label(root, text="Voice Listening: OFF")
    voice_label.pack(pady=5)
    tk.Button(root, text="Toggle Voice Listening", command=lambda: toggle_voice_listening(voice_label)).pack(pady=5)
    tk.Label(root, text=f"Manual hotkey: {HOTKEY}").pack(pady=5)
    tk.Label(root, text=f"Auto screenshots every {INTERVAL}s").pack(pady=5)

    return root

# Main function
def main():
    print(f"Starting AI Desktop Pilot\nSave path: {SAVE_PATH}\nManual hotkey: {HOTKEY}\nAuto interval: {INTERVAL}s")
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    manual_thread = threading.Thread(target=manual_screenshot, daemon=True)
    manual_thread.start()

    root = create_gui()
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("AI Desktop Pilot stopped.")