from fastapi import FastAPI
from cloudant.client import Cloudant
from ultralytics import YOLO
import cv2
import threading
import os
import time

app = FastAPI()

# =====================================================
# CLOUDANT CONFIG
# =====================================================

USERNAME = "apikey-v2-13l5ki1duy0sgm0a0h3h38odtlet8lxlqwp3syrb4y4u"

PASSWORD = "9a3515742bfe9492e0f0ca6e304a2616"

URL = "https://12e3523a-e90f-4f86-a7d9-d7575bc330c8-bluemix.cloudantnosqldb.appdomain.cloud"

client = Cloudant(
    USERNAME,
    PASSWORD,
    url=URL,
    connect=True
)

database_name = "traffic_data"

if database_name in client.all_dbs():

    db = client[database_name]

else:

    db = client.create_database(database_name)

print("✅ Cloudant Connected Successfully")

# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "yolov8n.pt"
)

VIDEO_PATH = os.path.join(
    BASE_DIR,
    "traffic.mp4"
)

SHARED_PATH = os.path.join(
    BASE_DIR,
    "shared"
)

os.makedirs(
    SHARED_PATH,
    exist_ok=True
)

FRAME_PATH = os.path.join(
    SHARED_PATH,
    "frame.jpg"
)

# =====================================================
# LOAD YOLO MODEL
# =====================================================

print("Loading YOLO model...")

model = YOLO(MODEL_PATH)

print("✅ YOLO Loaded")

# =====================================================
# LOAD VIDEO
# =====================================================

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():

    print("❌ ERROR: Cannot open video")

else:

    print("✅ Video Loaded")

# =====================================================
# VIDEO PROCESSING FUNCTION
# =====================================================

def process_video():

    while True:

        ret, frame = cap.read()

        # restart video
        if not ret:

            cap.set(
                cv2.CAP_PROP_POS_FRAMES,
                0
            )

            continue

        # YOLO detection
        results = model(frame)

        vehicle_count = 0

        for r in results:

            for box in r.boxes:

                cls = int(box.cls[0])

                # car, motorcycle, bus, truck
                if cls in [2, 3, 5, 7]:

                    vehicle_count += 1

                    x1, y1, x2, y2 = map(
                        int,
                        box.xyxy[0]
                    )

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 0, 255),
                        2
                    )

        # resize frame
        frame = cv2.resize(
            frame,
            (1200, 700)
        )

        # save frame
        cv2.imwrite(
            FRAME_PATH,
            frame
        )

        # save data to cloudant
        try:

            db.create_document({
                "vehicle_count": vehicle_count,
                "timestamp": str(time.time())
            })

        except Exception as e:

            print("Cloudant Error:", e)

        print("🚗 Vehicle Count:", vehicle_count)

        time.sleep(0.1)

# =====================================================
# START VIDEO THREAD
# =====================================================

threading.Thread(
    target=process_video,
    daemon=True
).start()

# =====================================================
# API ROUTES
# =====================================================

@app.get("/")
def home():

    return {
        "message": "API Running"
    }

@app.get("/traffic")
def get_traffic():

    docs = []

    try:

        for doc in db:

            docs.append({
                "vehicle_count": doc.get("vehicle_count"),
                "timestamp": doc.get("timestamp")
            })

    except Exception as e:

        print("Read Error:", e)

    return {
        "data": docs[-20:]
    }
