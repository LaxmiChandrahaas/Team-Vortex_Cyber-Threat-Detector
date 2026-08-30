import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page config
st.set_page_config(
    page_title="Team Vortex - Cyber Threat Detector",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stAlert { background-color: #1e1e2e; }
    .css-1d391kg { background-color: #0e1117; }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🛡️ Team Vortex: AI-Based Cyber Threat Detection")
st.caption("Zero Return Path. Maximum Intelligence.")

# Sidebar - Controls
with st.sidebar:
    st.header("⚙️ Controls")
    
    # Data source selection
    data_source = st.radio(
        "Data Source",
        ["Live Capture", "Upload PCAP", "Replay Dataset"]
    )
    
    if data_source == "Upload PCAP":
        uploaded_file = st.file_uploader("Choose a PCAP file", type=['pcap', 'pcapng'])
    
    # Threat types to detect
    st.subheader("🎯 Threat Detection")
    detect_ddos = st.checkbox("Volumetric DDoS", value=True)
    detect_scan = st.checkbox("Port Scanning", value=True)
    detect_exfil = st.checkbox("Data Exfiltration", value=True)
    
    # Confidence threshold
    confidence_threshold = st.slider(
        "Confidence Threshold (%)",
        min_value=50, max_value=95, value=70
    )
    
    # Start/Stop
    if st.button("▶️ Start Detection", type="primary"):
        st.session_state.running = True
    
    if st.button("⏹️ Stop Detection"):
        st.session_state.running = False

# Main area - 3 columns layout
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.subheader("📊 Live Traffic Overview")
    
    # Simulated traffic data (replace with real data)
    traffic_data = pd.DataFrame({
        'timestamp': pd.date_range(end=datetime.now(), periods=50, freq='1s'),
        'packets': np.random.randint(10, 200, 50),
        'bytes': np.random.randint(1000, 50000, 50)
    })
    
    fig = px.line(traffic_data, x='timestamp', y=['packets', 'bytes'],
                  title='Network Traffic Volume',
                  labels={'value': 'Count', 'variable': 'Metric'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🚨 Recent Alerts")
    
    # Sample alerts
    alerts = [
        {"time": "12:34:56", "threat": "DDoS", "confidence": 92, "src": "192.168.1.100"},
        {"time": "12:34:52", "threat": "Port Scan", "confidence": 78, "src": "10.0.0.45"},
        {"time": "12:34:48", "threat": "Exfiltration", "confidence": 65, "src": "172.16.1.200"},
    ]
    
    for alert in alerts:
        color = "🔴" if alert['confidence'] > 80 else "🟡" if alert['confidence'] > 60 else "🟢"
        st.markdown(f"""
            <div style="background:#1e1e2e; padding:8px; border-radius:5px; margin:4px 0;">
                <b>{color} {alert['threat']}</b> 
                <span style="float:right;">{alert['confidence']}%</span><br>
                <small>{alert['time']} · {alert['src']}</small>
            </div>
        """, unsafe_allow_html=True)

with col3:
    st.subheader("📈 Threat Statistics")
    
    # Stats cards
    st.metric("Total Threats Detected", "47", delta="+12")
    st.metric("Avg Confidence", "82%", delta="+5%")
    st.metric("Active Flows", "1,284", delta="-3%")
    
    # Threat breakdown pie chart
    threat_counts = pd.DataFrame({
        'Threat': ['DDoS', 'Port Scan', 'Exfiltration', 'Beaconing'],
        'Count': [18, 14, 10, 5]
    })
    fig = px.pie(threat_counts, values='Count', names='Threat', 
                 title='Threat Breakdown', color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)

# Expanded alerts table
st.subheader("📋 Detailed Alert Log")
alert_data = pd.DataFrame({
    'Timestamp': ['12:34:56', '12:34:52', '12:34:48', '12:34:44', '12:34:40'],
    'Threat Class': ['DDoS', 'Port Scan', 'Exfiltration', 'Beaconing', 'DDoS'],
    'Confidence %': [92, 78, 65, 88, 71],
    'Source IP': ['192.168.1.100', '10.0.0.45', '172.16.1.200', '192.168.1.50', '10.0.0.12'],
    'Destination': ['8.8.8.8', '192.168.1.1', '203.0.113.5', '1.1.1.1', '8.8.4.4'],
    'Evidence': ['Rate: 4500 pkts/s', 'Ports: 22,80,443,8080', 'Ratio: 15:1', 'Interval: 30s', 'Rate: 3200 pkts/s']
})
st.dataframe(alert_data, use_container_width=True)

# Footer
st.divider()
st.caption("⚡ Team Vortex | AI-Based Detection of Cyber Threats in Unidirectional IP Traffic")