import streamlit as st
import requests
import pandas as pd
import altair as alt
from streamlit_autorefresh import st_autorefresh

# =====================================================
# API URLS
# =====================================================

API_URL = "https://traffic-backend.onrender.com/traffic"

VIDEO_URL = "https://traffic-backend.onrender.com/video"

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

    background-color: #111827;

    padding: 15px;

    border-radius: 10px;

    color: white;
}

img {

    border-radius: 12px;
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

            return response.json()

    except Exception as e:

        print(e)

    return None

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

    st.markdown(f"""
    <img src="{VIDEO_URL}"
    width="100%"
    style="border-radius:12px;">
    """, unsafe_allow_html=True)

# =====================================================
# ANALYTICS
# =====================================================

with col_stats:

    st.subheader("📊 Live Analytics")

    if data and "vehicle_count" in data:

        latest = int(data["vehicle_count"])

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

    else:

        st.warning("No data available")

# =====================================================
# GRAPH
# =====================================================

st.subheader("📈 Traffic Trend")

if data and "history" in data:

    history = data["history"]

    if len(history) > 0:

        df = pd.DataFrame(history)

        # convert count
        df["vehicle_count"] = pd.to_numeric(
            df["vehicle_count"],
            errors="coerce"
        )

        # convert time
        if "timestamp" in df.columns:

            try:

                df["time"] = pd.to_datetime(
                    df["timestamp"]
                ).dt.strftime("%H:%M:%S")

            except:

                df["time"] = df["timestamp"]

        else:

            df["time"] = range(len(df))

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

else:

    st.warning("No graph data available")

# =====================================================
# TABLE
# =====================================================

st.subheader("📋 Recent Data")

if data and "history" in data:

    history = data["history"]

    if len(history) > 0:

        df = pd.DataFrame(history)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.warning("No table data")

else:

    st.warning("No table data")
