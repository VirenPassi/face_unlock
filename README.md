# Face Unlock for Windows

A Python-based facial recognition system designed to deploy a custom lock screen overlay and unlock the computer when a recognized face is detected. 

## ⚙️ How It Works

This project utilizes computer vision to mimic a secure lock screen environment:
1. **The Lock Screen**: `fake_lock_screen.py` deploys a full-screen, borderless window using a standard Windows background (`windows_lock_bg.jpg`) to restrict access.
2. **Face Detection & Recognition**: `face_unlock.py` uses OpenCV and Haar Cascades (`haarcascade_frontalface_default.xml`) to scan the webcam feed. It compares detected faces against authorized users stored in the `known_faces/` directory.
3. **The Unlock Mechanism**: A background monitor (`unlock_monitor.py`) watches for a successful match. Once authorization is confirmed, an `unlock.signal` is triggered, terminating the lock screen overlay and granting access.

## 🛠️ Tech Stack
* **Python** (Core Logic)
* **OpenCV** (Face detection and computer vision processing)
* **PyInstaller** (Compiled into standalone `.exe` files for native execution)
* **GitHub Actions** (Automated build workflows configured in `.github/workflows/build.yml`)

## 🚀 Running the Project
The application is compiled into executables for ease of use. Ensure the `known_faces/` directory contains an updated reference image before running the main executable to test the unlock flow.
