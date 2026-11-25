
import streamlit as st
 
import pandas as pd
 
import plotly.express as px
 
import time
 
from database import (
 
    initialize_database,
 
    get_history,
 
    get_alerts,
 
    get_latest_prediction
 
)
 
 
# ==========================================
# PAGE CONFIG
# ==========================================
 
st.set_page_config(
 
    page_title=
 
    "AI Motor Health Monitoring",
 
 
    page_icon=
 
    "⚙️",
 
 
    layout=
 
    "wide"
 
)
 
 
# ==========================================
# DATABASE
# ==========================================
 
initialize_database()
 
 
# ==========================================
# TITLE
# ==========================================
 
st.title(
 
    "⚙️ AI-Based Industrial Motor Health Monitoring"
 
)
 
 
st.caption(
 
    "IoT • HiveMQ Cloud • Machine Learning • SQLite"
 
)
 
 
# ==========================================
# AUTO REFRESH
# ==========================================
 
refresh_time = 3
 
 
# ==========================================
# LOAD DATA
# ==========================================
 
history = get_history(
 
    100
 
)
 
 
prediction = (
 
    get_latest_prediction()
 
)
 
 
# ==========================================
# NO DATA
# ==========================================
 
if not history:
 
 
    st.warning(
 
        "Waiting for motor data..."
 
    )
 
 
    st.info(
 
        "Start mqtt_subscriber.py and motor_simulator.py"
 
    )
 
 
    time.sleep(
 
        refresh_time
 
    )
 
 
    st.rerun()
 
 
# ==========================================
# DATAFRAME
# ==========================================
 
df = pd.DataFrame(
 
    history
 
)
 
 
latest = df.iloc[-1]
 
 
# ==========================================
# LIVE SENSOR DATA
# ==========================================
 
st.subheader(
 
    "📡 Live Motor Parameters"
 
)
 
 
col1, col2, col3, col4 = st.columns(
 
    4
 
)
 
 
col1.metric(
 
    "Voltage",
 
    f"{latest['voltage']:.2f} V"
 
)
 
 
col2.metric(
 
    "Current",
 
    f"{latest['current']:.3f} A"
 
)
 
 
col3.metric(
 
    "Power",
 
    f"{latest['power_w']:.2f} W"
 
)
 
 
col4.metric(
 
    "Temperature",
 
    f"{latest['temperature']:.2f} °C"
 
)
 
 
col5, col6, col7 = st.columns(
 
    3
 
)
 
 
col5.metric(
 
    "RPM",
 
    f"{latest['rpm']:.0f}"
 
)
 
 
col6.metric(
 
    "Vibration RMS",
 
    f"{latest['vibration_rms']:.3f}"
 
)
 
 
col7.metric(
 
    "Operating Hours",
 
    f"{latest['operating_hours']:.2f}"
 
)
 
 
# ==========================================
# AI SECTION
# ==========================================
 
st.divider()
 
 
st.subheader(
 
    "🤖 AI Motor Health Analysis"
 
)
 
 
if prediction:
 
 
    ai1, ai2, ai3 = st.columns(
 
        3
 
    )
 
 
    condition = prediction.get(
 
        "condition",
 
        "Unknown"
 
    )
 
 
    health = prediction.get(
 
        "health_score",
 
        0
 
    )
 
 
    confidence = prediction.get(
 
        "confidence",
 
        0
 
    )
 
 
    ai1.metric(
 
        "Motor Condition",
 
        condition
 
    )
 
 
    ai2.metric(
 
        "Health Score",
 
        f"{health:.1f}%"
 
    )
 
 
    ai3.metric(
 
        "AI Confidence",
 
        f"{confidence:.1f}%"
 
    )
 
 
    # --------------------------------------
    # HEALTH STATUS
    # --------------------------------------
 
    if health >= 80:
 
 
        st.success(
 
            "🟢 MOTOR HEALTHY"
 
        )
 
 
    elif health >= 60:
 
 
        st.warning(
 
            "🟡 MOTOR NEEDS MONITORING"
 
        )
 
 
    else:
 
 
        st.error(
 
            "🔴 MOTOR MAINTENANCE REQUIRED"
 
        )
 
 
# ==========================================
# CHARTS
# ==========================================
 
st.divider()
 
 
st.subheader(
 
    "📊 Historical Motor Monitoring"
 
)
 
 
df["timestamp"] = pd.to_datetime(
 
    df["timestamp"]
 
)
 
 
chart1, chart2 = st.columns(
 
    2
 
)
 
 
with chart1:
 
 
    fig = px.line(
 
        df,
 
        x="timestamp",
 
        y="temperature",
 
        title="Motor Temperature"
 
    )
 
 
    st.plotly_chart(
 
        fig,
 
        use_container_width=True
 
    )
 
 
with chart2:
 
 
    fig = px.line(
 
        df,
 
        x="timestamp",
 
        y="vibration_rms",
 
        title="Motor Vibration"
 
    )
 
 
    st.plotly_chart(
 
        fig,
 
        use_container_width=True
 
    )
 
 
chart3, chart4 = st.columns(
 
    2
 
)
 
 
with chart3:
 
 
    fig = px.line(
 
        df,
 
        x="timestamp",
 
        y="current",
 
        title="Motor Current"
 
    )
 
 
    st.plotly_chart(
 
        fig,
 
        use_container_width=True
 
    )
 
 
with chart4:
 
 
    fig = px.line(
 
        df,
 
        x="timestamp",
 
        y="rpm",
 
        title="Motor RPM"
 
    )
 
 
    st.plotly_chart(
 
        fig,
 
        use_container_width=True
 
    )
 
 
# ==========================================
# ALERTS
# ==========================================
 
st.divider()
 
 
st.subheader(
 
    "⚠️ Recent Alerts"
 
)
 
 
alerts = get_alerts(
 
    10
 
)
 
 
if alerts:
 
 
    alerts_df = pd.DataFrame(
 
        alerts
 
    )
 
 
    st.dataframe(
 
        alerts_df,
 
        use_container_width=True
 
    )
 
 
else:
 
 
    st.success(
 
        "No alerts detected"
 
    )
 
 
# ==========================================
# RAW DATA
# ==========================================
 
with st.expander(
 
    "View Latest Sensor Data"
 
):
 
 
    st.dataframe(
 
        df.tail(10),
 
        use_container_width=True
 
    )
 
 
# ==========================================
# REFRESH
# ==========================================
 
time.sleep(
 
    refresh_time
 
)
 
 
st.rerun()