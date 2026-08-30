"""
app_simple.py - Minimal working dashboard for Team Vortex
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Team Vortex - Cyber Threat Detection",
    page_icon="🛡️",
    layout="wide"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0e17 0%, #1a1a2e 50%, #16213e 100%);
    }
    .glow-text {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ff88, #00ccff, #8800ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(0,255,136,0.3);
    }
    .metric-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00ff88, #00ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .alert-critical {
        background: rgba(255,50,50,0.15);
        border-left: 4px solid #ff3333;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .alert-high {
        background: rgba(255,150,50,0.15);
        border-left: 4px solid #ff9933;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'running' not in st.session_state:
    st.session_state.running = False
if 'traffic_history' not in st.session_state:
    st.session_state.traffic_history = []

# ==================== HEADER ====================
st.markdown('<p class="glow-text" style="text-align:center;">🛡️ TEAM VORTEX</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#8899bb;">AI-Powered Cyber Threat Detection • Zero Return Path • Maximum Intelligence</p>', unsafe_allow_html=True)
st.divider()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### ⚙️ CONTROL CENTER")
    st.divider()
    
    # Start/Stop
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("▶️ START", use_container_width=True, type="primary"):
            st.session_state.running = True
    with col_b:
        if st.button("⏹️ STOP", use_container_width=True):
            st.session_state.running = False
    
    # Threshold
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=50, max_value=95, value=70, step=5
    )
    
    # Clear alerts
    if st.button("🗑️ CLEAR ALERTS", use_container_width=True):
        st.session_state.alerts = []
        st.rerun()
    
    # Stats
    st.divider()
    st.metric("Total Alerts", len(st.session_state.alerts))

# ==================== MAIN CONTENT ====================

# TOP ROW: Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="color:#8899bb;">TOTAL THREATS</div>
        <div class="metric-value">{len(st.session_state.alerts)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    high_risk = len([a for a in st.session_state.alerts if a.get('confidence', 0) > 85])
    st.markdown(f"""
    <div class="metric-card">
        <div style="color:#8899bb;">HIGH RISK</div>
        <div class="metric-value" style="background:linear-gradient(135deg,#ff4444,#ff8800);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{high_risk}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div style="color:#8899bb;">ACTIVE FLOWS</div>
        <div class="metric-value" style="background:linear-gradient(135deg,#00ccff,#8800ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">2,847</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    status_text = "🟢 MONITORING" if st.session_state.running else "⏸️ STOPPED"
    st.markdown(f"""
    <div class="metric-card">
        <div style="color:#8899bb;">SYSTEM STATUS</div>
        <div style="font-size:1.5rem; font-weight:bold; color:{'#00ff88' if st.session_state.running else '#ff4444'};">{status_text}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# MIDDLE ROW: Traffic Graph + Alerts
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("### 📈 LIVE TRAFFIC MONITOR")
    
    # Generate live traffic data
    if st.session_state.running:
        # Add new data point
        new_point = {
            'timestamp': datetime.now(),
            'packets': random.randint(50, 400),
            'bytes': random.randint(5000, 80000)
        }
        st.session_state.traffic_history.append(new_point)
        if len(st.session_state.traffic_history) > 60:
            st.session_state.traffic_history = st.session_state.traffic_history[-60:]
        
        # Simulate alert generation (15% chance)
        if random.random() < 0.15:
            threat_types = ['DDoS', 'Port Scan', 'Exfiltration']
            threat = random.choice(threat_types)
            confidence = random.randint(65, 98)
            
            if confidence >= confidence_threshold:
                alert = {
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'threat': threat,
                    'confidence': confidence,
                    'src': f"192.168.1.{random.randint(1,255)}",
                    'dst': f"10.0.0.{random.randint(1,255)}"
                }
                st.session_state.alerts.insert(0, alert)
                if len(st.session_state.alerts) > 50:
                    st.session_state.alerts = st.session_state.alerts[:50]
    
    # Plot traffic graph
    if st.session_state.traffic_history:
        df_traffic = pd.DataFrame(st.session_state.traffic_history)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_traffic['timestamp'],
            y=df_traffic['packets'],
            name='Packets/sec',
            line=dict(color='#00ff88', width=2),
            fill='tozeroy',
            fillcolor='rgba(0,255,136,0.1)'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_traffic['timestamp'],
            y=df_traffic['bytes'],
            name='Bytes/sec',
            line=dict(color='#00ccff', width=2),
            yaxis='y2'
        ))
        
        fig.update_layout(
            template='plotly_dark',
            height=350,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(title='Time', showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title='Packets/sec', showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis2=dict(
                title='Bytes/sec',
                overlaying='y',
                side='right',
                showgrid=False
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                bgcolor='rgba(0,0,0,0.3)'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("⏳ Click 'START' to begin monitoring")

with col_right:
    st.markdown("### 🚨 REAL-TIME ALERTS")
    
    if st.session_state.alerts:
        for alert in st.session_state.alerts[:15]:
            severity = "alert-critical" if alert['confidence'] > 85 else "alert-high"
            icon = "🔴" if alert['confidence'] > 85 else "🟠"
            st.markdown(f"""
            <div class="{severity}">
                <b>{icon} {alert['threat']}</b>
                <span style="float:right;color:#00ff88;">{alert['confidence']:.0f}%</span><br>
                <small style="color:#8899bb;">{alert['time']} · {alert['src']} → {alert['dst']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🛡️ No threats detected yet")

st.divider()

# BOTTOM ROW: Alert Log
st.markdown("### 📋 DETAILED ALERT LOG")

if st.session_state.alerts:
    alert_df = pd.DataFrame(st.session_state.alerts)[:20]
    st.dataframe(
        alert_df,
        use_container_width=True,
        column_config={
            'time': 'Timestamp',
            'threat': 'Threat Type',
            'confidence': st.column_config.NumberColumn('Confidence', format='%.0f%%'),
            'src': 'Source IP',
            'dst': 'Destination IP'
        }
    )
else:
    st.info("No alerts in log")

# ==================== FOOTER ====================
st.divider()
st.markdown("""
<div style="text-align:center; color:#445566; font-size:0.8rem;">
    ⚡ <b>Team Vortex</b> · AI-Based Detection of Cyber Threats in Unidirectional IP Traffic<br>
    <span style="color:#334455;">Zero Return Path · Maximum Intelligence</span>
</div>
""", unsafe_allow_html=True)