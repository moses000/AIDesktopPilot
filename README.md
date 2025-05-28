AI Desktop Pilot
AI Desktop Pilot is a Python-based desktop automation tool that mimics human interaction by opening applications, navigating UIs, taking screenshots, and performing tasks defined in a JSON file or via voice commands. It uses YOLOv8 for UI detection, Vosk for offline speech recognition, DistilBERT for NLP, and a Tkinter GUI for user control.
Features

Automation: Open apps (e.g., Chrome, Notepad), type text, navigate URLs, log in to websites.
Screenshots: Manual (Ctrl+Shift+S) or automatic (every 10 minutes).
AI Navigation: YOLOv8 detects UI elements (e.g., login fields, buttons); OCR reads screen text.
Task Scripting: Define tasks in tasks.json.
Voice Control: Offline voice commands via Vosk (e.g., "open Chrome", "log in to example.com").
NLP: DistilBERT parses complex commands.
Context Awareness: OCR-based CAPTCHA/popup detection.
Cross-Platform: Windows, macOS, Linux.

Directory Structure
AIDesktopPilot/
├── automation_tool.py
├── tasks.json
├── README.md
├── requirements.txt
├── yolo_ui_model.pt
├── vosk-model-small-en-us/
├── screenshots/
├── dataset/ (optional)
    ├── images/
    │   ├── train/
    │   └── val/
    ├── labels/
    │   ├── train/
    │   └── val/
    └── data.yaml

Prerequisites

Python 3.8+
Tesseract OCR
Windows: Tesseract
macOS: brew install tesseract
Linux: sudo apt-get install tesseract-ocr


Vosk Model
Download vosk-model-small-en-us from Vosk Models
Extract to vosk-model-small-en-us/


YOLO Model
Download yolov8n.pt from Ultralytics or train a custom model
Save as yolo_ui_model.pt


Python libraries:pip install -r requirements.txt


Microphone for voice control.

Installation

Clone the repository:git clone https://github.com/moses000/AIDesktopPilot.git
cd AIDesktopPilot


Install dependencies:pip install -r requirements.txt


Install Tesseract OCR.
Extract vosk-model-small-en-us to the project directory.
Place yolo_ui_model.pt in the project directory (see YOLO Setup).
(Optional) Create tasks.json.

YOLO Setup
Option 1: Pre-trained Model

Download yolov8n.pt:from ultralytics import YOLO
model = YOLO("yolov8n.pt")


Rename to yolo_ui_model.pt:mv yolov8n.pt yolo_ui_model.pt


Note: May have low accuracy for UI elements.

Option 2: Custom Model

Collect 100–500 screenshots of login forms:import pyautogui
for i in range(100):
    pyautogui.screenshot(f"dataset/images/train/login_{i}.png")
    time.sleep(2)


Annotate with LabelImg:pip install labelImg
labelImg


Label username_field, password_field, login_button.
Save annotations in dataset/labels/train/.


Organize dataset:dataset/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── data.yaml

data.yaml:train: dataset/images/train/
val: dataset/images/val/
nc: 3
names: ['username_field', 'password_field', 'login_button']


Train:from ultralytics import YOLO
model = YOLO("yolov8n.pt")
model.train(data="dataset/data.yaml", epochs=50, imgsz=640, batch=16)


Copy best model:cp runs/train/exp/weights/best.pt yolo_ui_model.pt



Usage

Run the script:python automation_tool.py


GUI:
Perform Sample Task: Opens Notepad, types, takes screenshot.
Execute Tasks from JSON: Runs tasks.json.
Take Screenshot: Manual screenshot.
Read Screen Text: OCR on screen.
Log in to Website: Prompts for credentials, logs in.
Toggle Voice Listening: Enables/disables voice commands.


Voice Commands:
"open Chrome"
"go to example.com"
"log in to example.com"
"type hello world"
"take screenshot"
"read text"
"execute tasks"
"stop listening"


Manual Screenshots: Ctrl+Shift+S.
Automatic Screenshots: Every 10 minutes in screenshots/.

Notes

Permissions: macOS/Linux need screen recording, input, microphone permissions. Windows may require pyaudio setup.
YOLO: Custom model recommended for UI accuracy. Without yolo_ui_model.pt, login fails.
Vosk: Ensure vosk-model-small-en-us is present.
Credentials: GUI prompts for login credentials.
Performance: Keep INTERVAL ≥ 5s.
Deployment:pyinstaller --onefile automation_tool.py



License
MIT License
Contributing
Open issues or pull requests on GitHub.
Contact
Create a GitHub issue or email [im.imoleayomoses@gmail.com]
