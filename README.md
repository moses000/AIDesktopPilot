AI Desktop Pilot
AI Desktop Pilot is a Python-based desktop automation tool that mimics human interaction by opening applications, navigating UIs, taking screenshots, and performing tasks defined in a JSON file. It uses computer vision (OpenCV, Tesseract OCR) for AI-driven navigation and includes a simple GUI for user control.
Features

Automation: Open apps (e.g., Notepad, TextEdit), type text, and perform actions.
Screenshots: Capture screenshots manually (Ctrl+Shift+S) or automatically (every 10 minutes).
AI Navigation: Detect and click UI elements using template matching; read screen text with OCR.
Task Scripting: Define custom tasks in a tasks.json file.
Cross-Platform: Supports Windows, macOS, and Linux (with OS-specific commands).
GUI: Simple Tkinter interface for triggering tasks.

Prerequisites

Python 3.8+
Tesseract OCR (for text recognition)
Windows: Install from Tesseract
macOS: brew install tesseract
Linux: sudo apt-get install tesseract-ocr


Python libraries:pip install pyautogui pynput opencv-python pytesseract schedule pillow



Installation

Clone the repository:git clone https://github.com/yourusername/AIDesktopPilot.git
cd AIDesktopPilot


Install dependencies:pip install -r requirements.txt


Install Tesseract OCR (see above).
(Optional) Create a button_template.png for AI navigation by cropping a button from a screenshot.

Usage

Run the script:python automation_tool.py


The GUI opens, showing:
Perform Sample Task: Opens Notepad, types text, and takes a screenshot.
Execute Tasks from JSON: Runs tasks from tasks.json.
Take Screenshot: Captures a manual screenshot.
Read Screen Text: Displays text on the screen via OCR.


Manual screenshots: Press Ctrl+Shift+S.
Automatic screenshots: Saved every 10 minutes in the screenshots folder.
Customize tasks in tasks.json (see example below).

Example tasks.json
[
    {
        "action": "open",
        "app": "notepad.exe"
    },
    {
        "action": "type",
        "value": "Hello from AI Desktop Pilot!"
    },
    {
        "action": "screenshot",
        "prefix": "task"
    },
    {
        "action": "click_button",
        "template": "button_template.png"
    }
]

Notes

Permissions: macOS/Linux may require screen recording/input permissions.
AI Navigation: Provide a button_template.png for button-clicking. Edit TEMPLATE_PATH in the script if needed.
Deployment: Package with PyInstaller:pip install pyinstaller
pyinstaller --onefile automation_tool.py



Future Improvements

Advanced AI with YOLO for UI element detection.
Region selection for screenshots.
Reinforcement learning for adaptive navigation.
Support for more complex task scripting.

License
MIT License
Contributing
Pull requests are welcome! Please open an issue to discuss changes.
Contact
For issues or suggestions, create a GitHub issue or contact [your email].
