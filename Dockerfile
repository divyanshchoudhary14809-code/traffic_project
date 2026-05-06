FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install fastapi uvicorn streamlit pandas requests altair opencv-python ultralytics cloudant streamlit-autorefresh

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "frontend/app.py", "--server.address=0.0.0.0"]