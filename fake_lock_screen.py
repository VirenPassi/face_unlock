import tkinter as tk
import threading
import os
import sys
import time
import cv2
import torch
import numpy as np
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1

def get_resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path.replace("/", os.sep).replace("\\", os.sep))

def recognize_face_and_unlock(callback_on_success):
    print("[INFO] Using device:", "cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print("[INFO] Loading model...")
    model = InceptionResnetV1(pretrained='vggface2', classify=False).eval().to(device)
    mtcnn = MTCNN(image_size=160, margin=0, device=device)

    known_embeddings = []
    known_names = []
    faces_dir = get_resource_path("known_faces")

    if not os.path.exists(faces_dir):
        print(f"[ERROR] known_faces folder not found at {faces_dir}")
        return

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

    print("[INFO] Starting camera for live face detection...")
    cap = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
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
                    callback_on_success()
                    break
            else:
                print("[INFO] No face detected")
            time.sleep(0.2)
    finally:
        cap.release()

def launch_fake_screen():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")

    label = tk.Label(root, text="Enter PIN:", font=("Arial", 24), fg="white", bg="black")
    label.pack(pady=20)

    pin_entry = tk.Entry(root, show="*", font=("Arial", 24))
    pin_entry.pack(pady=10)

    def try_unlock():
        if pin_entry.get() == "2005":
            print("[INFO] Correct PIN entered, unlocking...")
            with open("unlock.signal", "w") as f:
                f.write("unlocked")
            root.destroy()

    unlock_btn = tk.Button(root, text="Unlock", font=("Arial", 20), command=try_unlock)
    unlock_btn.pack(pady=20)

    # When face is matched, insert PIN and auto-click unlock
    def on_face_match():
        root.after(100, lambda: pin_entry.insert(0, "2005"))
        root.after(600, try_unlock)

    # Run face recognition in parallel thread
    threading.Thread(target=lambda: recognize_face_and_unlock(on_face_match), daemon=True).start()

    root.mainloop()

    # Clean up
    if os.path.exists("unlock.signal"):
        os.remove("unlock.signal")

if __name__ == "__main__":
    launch_fake_screen()
