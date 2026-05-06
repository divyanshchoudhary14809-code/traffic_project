# 🚦 Smart Traffic Monitoring System

A real-time AI-powered traffic monitoring system developed using YOLOv8, FastAPI, Streamlit, OpenCV, and IBM Cloudant.

The system performs:
- Vehicle Detection
- Vehicle Counting
- Live Traffic Monitoring
- Traffic Analytics Visualization
- Cloud Database Storage

---

## ✨ Features

✅ Real-time vehicle detection using YOLOv8  
✅ Live traffic video streaming  
✅ Vehicle counting and analytics  
✅ Interactive Streamlit dashboard  
✅ Traffic trend visualization  
✅ IBM Cloudant database integration  
✅ REST API communication using FastAPI  
✅ API testing using Postman  
✅ Cloud deployment support  

---

# 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Frontend | Streamlit, HTML/CSS |
| Backend | Python, FastAPI |
| AI / Computer Vision | YOLOv8 (Ultralytics), OpenCV |
| Database | IBM Cloudant NoSQL Database |
| API Testing | Postman |
| Deployment | Streamlit Cloud, Render |
| API Communication | REST API |
| Version Control | Git, GitHub |

---

# 📂 Project Structure

```bash
traffic_project/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   └── app.py
│
├── yolov8n.pt
├── traffic.mp4
├── requirements.txt
├── runtime.txt
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/divyanshchoudhary14809-code/traffic_project.git
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Backend

```bash
cd backend
python -m uvicorn main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

# ▶️ Run Frontend

```bash
cd frontend
python -m streamlit run app.py
```

Frontend runs on:

```bash
http://localhost:8501
```

---

# 📡 API Endpoints

| Endpoint | Description |
|---|---|
| `/` | Backend Status |
| `/video` | Live Video Stream |
| `/traffic` | Traffic Analytics Data |

---

# 🔄 Working Flow

```text
Traffic Video
      ↓
YOLOv8 Vehicle Detection
      ↓
Vehicle Counting
      ↓
Cloudant Database Storage
      ↓
FastAPI REST APIs
      ↓
Streamlit Dashboard
```

---

# 📊 Dashboard Features

- 🎥 Live Video Feed
- 🚗 Real-time Vehicle Count
- 📈 Traffic Trend Graph
- 📋 Traffic Analytics Table
- 🚦 Traffic Status Monitoring

---

# ☁️ Deployment

| Service | Platform |
|---|---|
| Frontend Deployment | Streamlit Cloud |
| Backend Deployment | Render |

---

# 🔗 GitHub Repository

```bash
https://github.com/divyanshchoudhary14809-code/traffic_project
```

---

# 👨‍💻 Developed By

## Divyansh Choudhary, Aditya Gairola,Deepanshu Manethiya,Anirudh Sharma
