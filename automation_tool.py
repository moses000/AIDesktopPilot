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
from tkinter import messagebox
import json

# Configuration
pyautogui.FAILSAFE = True  # Move mouse to top-left to abort
SAVE_PATH = "screenshots"
HOTKEY = "ctrl+shift+s"
INTERVAL = 600  # 10 minutes
TASKS_FILE = "tasks.json"
TEMPLATE_PATH = "button_template.png"  # Optional: for AI navigation

# Create save directory
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

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
            os.system(app_name)
        elif system == "Darwin":  # macOS
            os.system(f"open -a {app_name}")
        elif system == "Linux":
            os.system(app_name)
        else:
            raise Exception("Unsupported OS")
        time.sleep(1)  # Wait for app to open
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

# AI navigation: Find and click a button using template matching
def find_and_click_button(template_path, retries=3):
    for attempt in range(retries):
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save("temp.png")
            screen = cv2.imread("temp.png")
            template = cv2.imread(template_path)
            if template is None:
                raise Exception("Template image not found")

            result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val > 0.8:  # Confidence threshold
                x, y = max_loc
                pyautogui.click(x + template.shape[1] // 2, y + template.shape[0] // 2)
                print(f"Clicked button at ({x}, {y})")
                os.remove("temp.png")
                return True
            else:
                print(f"Button not found (attempt {attempt + 1}/{retries})")
                time.sleep(1)
        except Exception as e:
            print(f"Error in AI navigation (attempt {attempt + 1}/{retries}): {e}")
        finally:
            if os.path.exists("temp.png"):
                os.remove("temp.png")
    messagebox.showerror("Error", "Button not found after retries")
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
            elif action == "click_button":
                find_and_click_button(task.get("template", TEMPLATE_PATH))
            else:
                print(f"Unknown action: {action}")
        messagebox.showinfo("Success", "Tasks executed successfully")
    except Exception as e:
        print(f"Error executing tasks: {e}")
        messagebox.showerror("Error", f"Task execution failed: {e}")

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
        type_text()
        take_screenshot("sample_task")
        messagebox.showinfo("Success", "Sample task completed")
    except Exception as e:
        print(f"Error in sample task: {e}")
        messagebox.showerror("Error", f"Sample task failed: {e}")

# GUI
def create_gui():
    root = tk.Tk()
    root.title("AI Desktop Pilot")
    root.geometry("300x250")

    tk.Label(root, text="AI Desktop Pilot", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Perform Sample Task", command=perform_sample_task).pack(pady=5)
    tk.Button(root, text="Execute Tasks from JSON", command=execute_tasks).pack(pady=5)
    tk.Button(root, text="Take Screenshot", command=lambda: take_screenshot("manual")).pack(pady=5)
    tk.Button(root, text="Read Screen Text", command=read_screen_text).pack(pady=5)
    tk.Label(root, text=f"Manual hotkey: {HOTKEY}").pack(pady=5)
    tk.Label(root, text=f"Auto screenshots every {INTERVAL}s").pack(pady=5)

    return root

# Main function
def main():
    print(f"Starting AI Desktop Pilot\nSave path: {SAVE_PATH}\nManual hotkey: {HOTKEY}\nAuto interval: {INTERVAL}s")
    
    # Start automatic screenshot scheduler
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Start manual screenshot listener
    manual_thread = threading.Thread(target=manual_screenshot, daemon=True)
    manual_thread.start()

    # Start GUI
    root = create_gui()
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("AI Desktop Pilot stopped.")