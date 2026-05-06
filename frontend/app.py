import streamlit as st
import requests
import pandas as pd
import altair as alt
import cv2
import os
from streamlit_autorefresh import st_autorefresh

API_URL = "http://127.0.0.1:8000/traffic"

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Smart Traffic Dashboard",
    layout="wide"
)

# =====================================================
# AUTO REFRESH
# =====================================================

st_autorefresh(
    interval=2000,
    key="traffic_refresh"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #0E1117;
    color: white;
}

[data-testid="stMetric"] {
    background-color: #111;
    padding: 15px;
    border-radius: 10px;
    color: white;
}

img {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.title("🚦 Smart Traffic Monitoring System")

# =====================================================
# GET DATA
# =====================================================

def get_data():

    try:

        response = requests.get(API_URL)

        if response.status_code == 200:

            return response.json()["data"]

    except Exception as e:

        print(e)

        return []

    return []

# =====================================================
# FETCH DATA
# =====================================================

data = get_data()

# =====================================================
# LAYOUT
# =====================================================

col_video, col_stats = st.columns([3, 1])

# =====================================================
# VIDEO FEED
# =====================================================

with col_video:

    st.subheader("🎥 Live Traffic Feed")

    image_path = "../shared/frame.jpg"

    if os.path.exists(image_path):

        frame = cv2.imread(image_path)

        if frame is not None:

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            st.image(
                frame,
                use_container_width=True
            )

        else:

            st.warning("Frame loading failed")

    else:

        st.warning("Waiting for video feed...")

# =====================================================
# ANALYTICS
# =====================================================

with col_stats:

    st.subheader("📊 Live Analytics")

    if len(data) > 0:

        df = pd.DataFrame(data)

        latest = int(
            df.iloc[-1]["vehicle_count"]
        )

        st.metric(
            "🚗 Vehicles",
            latest
        )

        if latest < 20:

            st.success("🟢 LOW Traffic")

        elif latest < 35:

            st.warning("🟡 MEDIUM Traffic")

        else:

            st.error("🔴 HIGH Traffic")

        st.write("### Recent Count")
        st.write(latest)

    else:

        st.warning("No data available")

# =====================================================
# GRAPH
# =====================================================

st.subheader("📈 Traffic Trend")

if len(data) > 0:

    df = pd.DataFrame(data)

    # vehicle count numeric
    df["vehicle_count"] = pd.to_numeric(
        df["vehicle_count"],
        errors="coerce"
    )

    # timestamp convert
    df["timestamp"] = pd.to_datetime(
        df["timestamp"].astype(float),
        unit="s"
    )

    # readable time
    df["time"] = df["timestamp"].dt.strftime(
        "%H:%M:%S"
    )

    chart = alt.Chart(df).mark_line(
        point=True
    ).encode(
        x=alt.X(
            "time:N",
            title="Time"
        ),
        y=alt.Y(
            "vehicle_count:Q",
            title="Vehicles"
        ),
        tooltip=[
            "time",
            "vehicle_count"
        ]
    ).properties(
        height=400
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )

else:

    st.warning("No graph data available")

# =====================================================
# TABLE
# =====================================================

st.subheader("📋 Recent Data")

if len(data) > 0:

    st.dataframe(
        df,
        use_container_width=True
    )
