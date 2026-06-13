import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np
import cv2
import os
import sys
import time
from PIL import Image
import pyautogui

print("[INFO] Using device:", "cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    # Convert all path separators to the correct OS-specific separator
    relative_path = relative_path.replace("/", os.sep).replace("\\", os.sep)
    return os.path.join(base_path, relative_path)

# Load embedding model - let facenet_pytorch handle the download
print("[INFO] Loading face recognition model...")
try:
    # This will automatically download the model if not found
    model = InceptionResnetV1(pretrained='vggface2', classify=False).eval().to(device)
    print("[INFO] Model loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load model: {e}")
    print("[INFO] This might be due to network issues. Please check your internet connection.")
    print("[INFO] If the problem persists, you can try installing with: pip install --upgrade facenet-pytorch")
    sys.exit(1)

# Load MTCNN
print("[INFO] Loading face detector...")
mtcnn = MTCNN(image_size=160, margin=0, device=device)

# Load known faces
known_embeddings = []
known_names = []
faces_dir = get_resource_path("known_faces")

if not os.path.exists(faces_dir):
    print(f"[ERROR] known_faces folder not found at {faces_dir}")
    sys.exit(1)

for file in os.listdir(faces_dir):
    if file.lower().endswith((".jpg", ".png")):
        img_path = os.path.join(faces_dir, file)
        img = Image.open(img_path)
        face = mtcnn(img)
        if face is not None:
            emb = model(face.unsqueeze(0).to(device)).detach().cpu().numpy()
            known_embeddings.append(emb)
            known_names.append(file)
            print(f"[OK] Loaded: {file}")

print("[INFO] Looking for your face... (Ctrl+C to cancel)")
cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Failed to grab frame")
            continue

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        face = mtcnn(img)

        if face is not None:
            print("[INFO] Face detected. Computing embedding...")
            emb = model(face.unsqueeze(0).to(device)).detach().cpu().numpy()
            dists = [np.linalg.norm(e - emb) for e in known_embeddings]
            min_dist = min(dists)
            print(f"[DEBUG] Closest match distance: {min_dist:.4f}")

            if min_dist < 0.9:
                name = known_names[dists.index(min_dist)]
                print(f"[SUCCESS] Match found ({name}, Distance: {min_dist:.4f}) - Unlocking...")
                time.sleep(1)
                pyautogui.FAILSAFE = False
                pyautogui.write("2005", interval=0.1)
                pyautogui.press("enter")
                with open("unlock.signal", "w") as f:
                    f.write("unlocked")
                break
            else:
                print("[INFO] Face found but no match below threshold")

        else:
            print("[INFO] No face detected in frame")

        time.sleep(0.2)

except KeyboardInterrupt:
    print("[INFO] KeyboardInterrupt received. Exiting...")

finally:
    cap.release()
    # Do not call cv2.destroyAllWindows() to avoid PyInstaller crash
