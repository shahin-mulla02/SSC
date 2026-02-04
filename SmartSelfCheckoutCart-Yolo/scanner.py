import cv2
from pyzbar.pyzbar import decode
import pygame
import json
import os
import time
from db import products_col
import threading
from yolo_detector import run_yolo
import pyttsx3  # still imported for CustomerDashboard


# ---------------------- Speak Welcome (used elsewhere) ----------------------
def speak_welcome():
    engine = pyttsx3.init()
    engine.say("Welcome to Smart Self Checkout!")
    engine.runAndWait()


# ---------------------- Main Scanner ----------------------
def run_scanner():
    # Load items from MongoDB
    items_dict = {item["code"]: item for item in products_col.find()}

    # Initialize pygame for sound
    pygame.mixer.init()

    # Mobile camera URL (IP Webcam)
    url = "http://100.87.168.1:8080/video"
    cap = cv2.VideoCapture(url)

    last_scan_time = {}
    scan_delay = 5  # seconds
    scanned_items = {}

    def save_to_file():
        with open("static/scanned_items.json", "w") as f:
            json.dump(list(scanned_items.values()), f, indent=4)

    print("📸 Mobile camera connected. Press 'q' to quit.")

    # Start YOLO in background
    threading.Thread(
        target=run_yolo,
        args=(url,),
        daemon=True
    ).start()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame from mobile camera.")
            break

        for barcode in decode(frame):
            barcode_data = barcode.data.decode("utf-8")
            item = items_dict.get(barcode_data)

            now = time.time()
            last_time = last_scan_time.get(barcode_data, 0)

            if item and (now - last_time) >= scan_delay:
                name = item["name"]
                price = item["price"]

                if barcode_data in scanned_items:
                    scanned_items[barcode_data]["quantity"] += 1
                else:
                    scanned_items[barcode_data] = {
                        "name": name,
                        "price": price,
                        "quantity": 1,
                        "expiry_date": item.get("expiry_date")
                    }

                save_to_file()
                print(f"✅ Scanned: {name} | ₹{price}")
                last_scan_time[barcode_data] = now

                if item.get("sound"):
                    sound_path = os.path.join("static", "sounds", item["sound"])
                    try:
                        pygame.mixer.music.load(sound_path)
                        pygame.mixer.music.play()
                    except Exception as e:
                        print("⚠️ Sound file error:", e)

        # Hide scanner window
        # cv2.imshow("📱 Mobile Camera View", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# ---------------------- Run Scanner Only ----------------------
if __name__ == "__main__":
    run_scanner()  # no speak_welcome() here
