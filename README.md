# AI Desktop Mentor

AI Desktop Mentor is an advanced Python-based desktop automation tool designed to emulate human-like interactions with a computer system. It leverages cutting-edge AI technologies, including YOLOv8 for UI element detection, Vosk for offline speech recognition, and DistilBERT for natural language processing (NLP), to perform tasks such as opening applications, navigating websites, logging in, and processing screenshots. With a Tkinter interface, it supports voice commands, task scripting, and automated workflows, making it ideal for business automation and personal productivity.

## Features

- **Automation**: Open applications (e.g., Chrome, Notepad), type text, navigate URLs, and log in to websites.
- **Screenshots**: Capture screenshots manually (`Ctrl+Shift+S`) or automatically (every 15 minutes).
- **AI Navigation**: YOLOv8 detects UI elements (e.g., login fields, buttons); OCR reads screen text.
- **Task Scripting**: Execute tasks defined in a `tasks.json` file.
- **Voice Control**: Offline voice commands via Vosk (e.g., "open Chrome", "log in to example.com").
- **NLP**: DistilBERT parses complex voice commands for natural language understanding.
- **Context Awareness**: Detects CAPTCHAs/pop-ups using OCR with basic error handling.
- **Cross-Platform**: Supports Windows, macOS, and Linux.

## Directory Structure

Below is the directory structure for the AI Desktop Mentor project:

```plaintext
  AIDesktopMentor/
  ├── automation/
  │   ├── automation_tool.py        # Main Python script for automation
  ├── config/
  │   ├── tasks.json            # JSON file defining automation tasks
  ├── docs/
  │   ├── README.md              # Project documentation (this file)
  │   └── requirements.txt       # Python dependencies list
  ├── models/
  │   ├── yolo_ui_model.pth       # YOLOv8 for UI detection (pre-trained or custom)
  │   └── vosk-model-small-en-us/ # Vosk model for speech recognition
  │       ├── am/
  │       ├── conf/
  │       ├── graph/
  │       └── ivector/
  ├── outputs/
  │   └── screenshots/           # Directory for storing screenshots
  ├── dataset/                   # (Optional) For custom YOLO training
  │   ├── images/
  │   │   ├── train/         # Training screenshots
  │   │   └── val/           # Validation screenshots
  │   ├── labels/
  │   │   ├── train/         # Training annotations
  │   │   └── val/           # Validation annotations
  │   └── data.yaml          # YOLO dataset configuration
```
Technical Workflow
The following Mermaid flowchart illustrates the technical workflow of AI Desktop Mentor, showing how components interact to process user inputs and execute tasks:
```mermaid
graph TD
    A[User Input] -->|GUI Button| B[GUI (Tkinter)]
    A -->|Voice Command| C[Voice Listener (Vosk)]
    C --> D[NLP Parser (DistilBERT)]
    D --> E[Command Processor]
    B --> E
    E -->|Open App| F[Automation Engine (PyAutoGUI)]
    E -->|Navigate URL| F
    E -->|Login| G[UI Detection (YOLOv8)]
    G --> F
    E -->|Screenshot| H[Screenshot Module]
    E -->|Read Text| I[OCR (Pytesseract)]
    E -->|Check Popups| I
    F --> J[OS Interaction]
    H --> K[Save to screenshots/]
    I --> L[Context Feedback]
    J --> M[Screen Output]
    L --> M
```
Explanation:

User Input: Via GUI buttons or voice commands.
Voice Processing: Vosk converts speech to text; DistilBERT parses complex commands.
Command Processor: Maps inputs to actions (e.g., open Chrome, login).
Automation: PyAutoGUI simulates mouse/keyboard actions.
UI Detection: YOLOv8 identifies login fields/buttons.
OCR: Pytesseract reads screen text for popups or queries.
Output: Screenshots saved, screen updated, feedback provided.

Business Workflow
This Mermaid flowchart outlines the business workflow, showing how AI Desktop Mentor supports user tasks in a business context:

graph TD
```mermaid
    A[Business User] --> B[Define Task]
    B -->|Manual| C[GUI Interaction]
    B -->|Automated| D[Configure tasks.json]
    B -->|Voice| E[Voice Command]
    C --> F[Execute Task]
    D --> F
    E --> F
    F -->|Open App| G[Access System]
    F -->|Login| H[Authenticate]
    F -->|Navigate| I[Access Resource]
    F -->|Screenshot| J[Generate Report]
    H -->|YOLO Detection| I
    I --> K[Perform Business Function]
    J --> L[Save Output]
    K --> M[Business Outcome]
    L --> M
```
Explanation:

User: Defines tasks (e.g., log in to CRM, capture dashboard).
Input Methods: GUI, JSON tasks, or voice commands.
Execution: Tasks automate app opening, logins, navigation.
YOLO: Ensures accurate login by detecting UI elements.
Output: Screenshots for reports, business functions completed.
Outcome: Improved efficiency, automated repetitive tasks.

Prerequisites

Python 3.8+
Tesseract OCR:
Windows: Install from Tesseract
macOS: brew install tesseract
Linux: sudo apt-get install tesseract-ocr


Vosk Model:
Download vosk-model-small-en-us from Vosk Models
Extract to vosk-model-small-en-us/


YOLO Model:
Use yolov8n.pt or train a custom model
Save as yolo_ui_model.pt


Python Libraries:pip install -r requirements.txt


Microphone: For voice control.
Permissions: Screen recording, input, microphone (macOS/Linux); pyaudio setup (Windows).

Installation

Clone the repository:git clone https://github.com/moses000/AIDesktopMentor.git
cd AIDesktopMentor


Set up directory structure:mkdir -p outputs/screenshots dataset/images/train dataset/images/val dataset/labels/train dataset/labels/val


Install dependencies:pip install -r requirements.txt


Install Tesseract OCR (see Prerequisites).
Extract vosk-model-small-en-us to models/vosk-model-small-en-us/.
Place yolo_ui_model.pt in models/ (see YOLO Setup).
(Optional) Create or modify config/tasks.json.

YOLO Setup
Option 1: Pre-trained Model

Download yolov8n.pt:from ultralytics import YOLO
model = YOLO("yolov8n.pt")


Rename:mv yolov8n.pt models/yolo_ui_model.pt


Note: Limited accuracy for UI elements.

Option 2: Custom Model

Collect 100–500 screenshots of login forms:import pyautogui
import time
for i in range(100):
    pyautogui.screenshot(f"dataset/images/train/login_{i}.png")
    time.sleep(2)


Annotate with LabelImg:pip install labelImg
labelImg dataset/images/train dataset/labels/train


Label: username_field, password_field, login_button.


Create dataset/data.yaml:train: dataset/images/train/
val: dataset/images/val/
nc: 3
names: ['username_field', 'password_field', 'login_button']


Train:from ultralytics import YOLO
model = YOLO("yolov8n.pt")
model.train(data="dataset/data.yaml", epochs=50, imgsz=640, batch=16)


Copy model:cp runs/train/exp/weights/best.pt models/yolo_ui_model.pt



Usage

Run the script:python automation/automation_tool.py


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
Automatic Screenshots: Every 15 minutes in outputs/screenshots/.
JSON Tasks: Edit config/tasks.json for custom workflows.

Example tasks.json
[
    {
        "action": "open",
        "app": "chrome"
    },
    {
        "action": "navigate",
        "url": "https://example.com"
    },
    {
        "action": "login",
        "url": "https://example.com"
    },
    {
        "action": "screenshot",
        "prefix": "login_task"
    }
]

Notes

Permissions: macOS/Linux require screen recording, input, microphone permissions. Windows may need pyaudio setup.
YOLO: Custom model recommended for UI accuracy. Without yolo_ui_model.pt, login tasks fail.
Vosk: Ensure vosk-model-small-en-us is in models/.
Credentials: GUI prompts for login credentials.
Performance: Keep INTERVAL ≥ 5s to avoid resource strain.
Deployment:pip install pyinstaller
pyinstaller --onefile automation/automation_tool.py


Troubleshooting:
YOLO errors: Verify yolo_ui_model.pt and class IDs.
Vosk errors: Check model path and microphone.
Permissions: Ensure all are granted.



Future Improvements

Train YOLO for more UI elements.
Add reinforcement learning for adaptive navigation.
Implement CAPTCHA solvers.
Support larger NLP models for better parsing.
GUI task editor for tasks.json.

License
MIT License
Contributing
Open issues or pull requests on GitHub.
Contact
Create a GitHub issue or email [im.imoleayomoses@gmail.com].
Acknowledgements

Ultralytics for YOLOv8
Vosk for speech recognition
Hugging Face for transformers



