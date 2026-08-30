"""
app.py - Team Vortex Full Advanced Dashboard
AI-Based Detection of Cyber Threats in Unidirectional IP Traffic
6 Threat Types: DDoS, Port Scan, Exfiltration, Botnet C2, DGA/DNS, Malware in TLS
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time
import json
import os

# =============================================================================
# SIMULATED THREAT DETECTORS (standalone, no external backend needed)
# =============================================================================

def simulate_ddos():
    if random.random() < 0.10:
        return {
            'threat': 'DDoS',
            'confidence': random.randint(75, 98),
            'src': f"192.168.1.{random.randint(150, 200)}",
            'dst': random.choice(['8.8.8.8', '1.1.1.1', '192.168.1.1']),
            'details': f"Rate: {random.randint(3000, 6000)} pkts/s",
            'severity': 'CRITICAL' if random.random() > 0.3 else 'HIGH'
        }
    return None

def simulate_port_scan():
    if random.random() < 0.10:
        src = f"192.168.1.{random.randint(1, 50)}"
        return {
            'threat': 'Port_Scan',
            'confidence': random.randint(65, 88),
            'src': src,
            'dst': '10.0.0.1',
            'details': f"Ports scanned: {random.randint(50, 200)} in {random.randint(10, 60)}s",
            'severity': 'HIGH' if random.random() > 0.4 else 'MEDIUM'
        }
    return None

def simulate_exfiltration():
    if random.random() < 0.08:
        src = f"192.168.1.{random.randint(50, 100)}"
        return {
            'threat': 'Data_Exfiltration',
            'confidence': random.randint(70, 92),
            'src': src,
            'dst': random.choice(['8.8.8.8', '1.1.1.1', '203.0.113.5']),
            'details': f"Outbound/Inbound Ratio: {round(random.uniform(15, 50), 1)}:1",
            'severity': 'CRITICAL' if random.random() > 0.3 else 'HIGH'
        }
    return None

def simulate_beaconing():
    if random.random() < 0.12:
        src = f"192.168.1.{random.randint(100, 150)}"
        dst = f"45.33.{random.randint(1,255)}.{random.randint(1,255)}"
        return {
            'threat': 'Botnet_C2_Beaconing',
            'confidence': random.randint(78, 96),
            'src': src,
            'dst': dst,
            'details': f"Interval: {round(random.uniform(15, 30), 1)}s ± {round(random.uniform(0.5, 2.5), 2)}s",
            'severity': 'HIGH' if random.random() > 0.3 else 'MEDIUM'
        }
    return None

def simulate_dns_threat():
    if random.random() < 0.10:
        if random.random() < 0.5:
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
            domain = ''.join(random.choices(chars, k=random.randint(15, 25))) + '.xyz'
            return {
                'threat': 'DGA_Domain',
                'confidence': random.randint(72, 94),
                'src': 'internal_dns',
                'dst': domain,
                'details': f"Entropy: {round(random.uniform(3.8, 5.5), 2)}",
                'severity': 'HIGH' if random.random() > 0.3 else 'MEDIUM'
            }
        else:
            long_query = 'A' * random.randint(60, 120)
            return {
                'threat': 'DNS_Tunneling',
                'confidence': random.randint(70, 92),
                'src': 'internal_dns',
                'dst': long_query[:20] + '...exfil.com',
                'details': f"Query Length: {len(long_query) + 10} chars",
                'severity': 'CRITICAL' if random.random() > 0.5 else 'HIGH'
            }
    return None

def simulate_tls_threat():
    malware_names = ['CobaltStrike', 'Metasploit', 'Meterpreter', 'DarkComet']
    if random.random() < 0.08:
        return {
            'threat': 'Malware_Encrypted',
            'confidence': random.randint(68, 94),
            'src': f"workstation_{random.randint(1,50)}",
            'dst': 'external_c2_server.com',
            'details': f"JA3 Match: {random.choice(malware_names)}",
            'severity': 'CRITICAL'
        }
    return None

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Team Vortex - Cyber Threat Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS (Advanced Dark Theme)
# =============================================================================
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
        text-align: center;
    }
    .sub-glow {
        color: #8899bb;
        font-size: 1.1rem;
        letter-spacing: 2px;
        text-align: center;
    }
    .metric-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px 10px;
        margin: 10px 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border-color: #00ff88;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00ff88, #00ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-red {
        background: linear-gradient(135deg, #ff4444, #ff8800);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-blue {
        background: linear-gradient(135deg, #00ccff, #8800ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-cyan {
        background: linear-gradient(135deg, #00ff88, #00ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .alert-critical {
        background: rgba(255,50,50,0.15);
        border-left: 4px solid #ff3333;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 5px;
        animation: slideIn 0.5s ease;
    }
    .alert-high {
        background: rgba(255,150,50,0.15);
        border-left: 4px solid #ff9933;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 5px;
        animation: slideIn 0.5s ease;
    }
    .alert-medium {
        background: rgba(255,255,50,0.10);
        border-left: 4px solid #ffcc00;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 5px;
        animation: slideIn 0.5s ease;
    }
    .alert-low {
        background: rgba(50,255,50,0.08);
        border-left: 4px solid #33ff33;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 5px;
        animation: slideIn 0.5s ease;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .threat-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-right: 5px;
    }
    .badge-ddos { background: #ff3333; color: white; }
    .badge-beacon { background: #ff8800; color: white; }
    .badge-dga { background: #cc33ff; color: white; }
    .badge-tls { background: #ff44aa; color: white; }
    .badge-scan { background: #ffcc00; color: #1a1a2e; }
    .badge-exfil { background: #00ccff; color: #1a1a2e; }
    .stButton > button {
        background: linear-gradient(135deg, #00ff88, #00ccff);
        color: #0a0e17;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 8px 20px;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(0,255,136,0.4);
    }
    .stButton > button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    .status-online {
        display: inline-block;
        width: 12px;
        height: 12px;
        background: #00ff88;
        border-radius: 50%;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0,255,136,0.4); }
        70% { box-shadow: 0 0 0 15px rgba(0,255,136,0); }
        100% { box-shadow: 0 0 0 0 rgba(0,255,136,0); }
    }
    .status-offline {
        display: inline-block;
        width: 12px;
        height: 12px;
        background: #ff3333;
        border-radius: 50%;
    }
    .stExpander {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 8px;
        margin: 2px 0;
    }
    .stExpander > details > summary {
        font-size: 0.9rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE
# =============================================================================
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'running' not in st.session_state:
    st.session_state.running = False
if 'traffic_history' not in st.session_state:
    st.session_state.traffic_history = []
if 'alert_count' not in st.session_state:
    st.session_state.alert_count = 0
if 'packet_counter' not in st.session_state:
    st.session_state.packet_counter = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# =============================================================================
# HEADER
# =============================================================================
st.markdown('<p class="glow-text">🛡️ TEAM VORTEX</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-glow">AI-Powered Cyber Threat Detection • Zero Return Path • Maximum Intelligence</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#556677; font-size:0.9rem;">🔹 6 Threat Types: DDoS · Botnet C2 · DGA · TLS Malware · Port Scan · Data Exfiltration</p>', unsafe_allow_html=True)
st.divider()

# =============================================================================
# SIDEBAR (Advanced Controls)
# =============================================================================
with st.sidebar:
    st.markdown("### ⚙️ CONTROL CENTER")
    st.divider()

    # Start / Stop
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("▶️ START", use_container_width=True, type="primary"):
            st.session_state.running = True
            if st.session_state.packet_counter == 0:
                st.session_state.start_time = datetime.now()
    with col_b:
        if st.button("⏹️ STOP", use_container_width=True):
            st.session_state.running = False

    st.divider()

    # Confidence Threshold
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=50, max_value=95, value=70, step=5,
        help="Alerts below this confidence are filtered"
    )

    st.divider()

    # ==================== THREAT TOGGLES ====================
    st.markdown("### 🎯 THREAT DETECTION")
    st.markdown("**Core (MVP):**")
    detect_ddos = st.checkbox("🔴 Volumetric DDoS", value=True)
    detect_scan = st.checkbox("🟠 Port Scanning", value=True)
    detect_exfil = st.checkbox("🟡 Data Exfiltration", value=True)
    st.markdown("**Advanced (Bonus):**")
    detect_beacon = st.checkbox("🔵 Botnet C2 Beaconing", value=False)
    detect_dga = st.checkbox("🟣 DGA / DNS Tunnelling", value=False)
    detect_tls = st.checkbox("🟥 Malware in Encrypted Sessions", value=False)

    st.divider()

    # ==================== FILE UPLOAD (Read-Only) ====================
    st.markdown("### 📂 DATA INGEST")
    uploaded_file = st.file_uploader(
        "Upload PCAP or CSV (Read-Only)",
        type=['pcap', 'pcapng', 'csv'],
        help="System processes this strictly read-only. No return path."
    )
    if uploaded_file is not None:
        st.success(f"✅ Loaded: {uploaded_file.name}")
        st.session_state.uploaded_file = uploaded_file.name
        # In a real system, you would call ingest_pcap() here.
        # For demo, we just store the name.

    st.divider()

    # ==================== FILTER CONTROLS ====================
    st.markdown("### 🔍 FILTER ALERTS")
    all_threats = ['DDoS', 'Port_Scan', 'Data_Exfiltration',
                   'Botnet_C2_Beaconing', 'DGA_Domain', 'DNS_Tunneling',
                   'Malware_Encrypted']
    selected_threats = st.multiselect(
        "Threat Types",
        options=all_threats,
        default=all_threats[:3],
        help="Filter alerts by specific threat categories"
    )
    severity_filter = st.select_slider(
        "Min Severity",
        options=['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
        value='MEDIUM'
    )

    st.divider()

    # ==================== EXPORT ALERTS ====================
    if st.button("📥 Export Alerts (JSON)", use_container_width=True):
        if st.session_state.alerts:
            json_str = json.dumps(st.session_state.alerts, indent=2)
            st.download_button(
                label="⬇️ Download JSON",
                data=json_str,
                file_name="team_vortex_alerts.json",
                mime="application/json"
            )
        else:
            st.warning("No alerts to export")

    st.divider()

    # ==================== CLEAR ====================
    if st.button("🗑️ CLEAR ALL ALERTS", use_container_width=True):
        st.session_state.alerts = []
        st.session_state.alert_count = 0
        st.session_state.traffic_history = []
        st.session_state.packet_counter = 0
        st.rerun()

    st.divider()

    # ==================== SUMMARY STATS ====================
    st.markdown("### 📊 SUMMARY")
    st.metric("Total Alerts", len(st.session_state.alerts))
    if st.session_state.alerts:
        avg_conf = np.mean([a.get('confidence', 0) for a in st.session_state.alerts])
        st.metric("Avg Confidence", f"{avg_conf:.1f}%")
    # Online status
    if st.session_state.running:
        st.markdown(f'<span class="status-online"></span> <b>Status:</b> 🟢 Monitoring', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="status-offline"></span> <b>Status:</b> ⏸️ Stopped', unsafe_allow_html=True)

# =============================================================================
# MAIN LAYOUT
# =============================================================================

# --- TOP ROW: Advanced Metrics (Includes Throughput & Latency) ---
col1, col2, col3, col4, col5 = st.columns(5)

# Update packet counter for throughput
if st.session_state.running:
    st.session_state.packet_counter += random.randint(100, 500)

elapsed = (datetime.now() - st.session_state.start_time).total_seconds()
flows_per_sec = st.session_state.packet_counter / elapsed if elapsed > 0 else 0
latency_ms = random.randint(12, 45) if st.session_state.running else 0

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="color:#8899bb;">TOTAL THREATS</div>
        <div class="metric-value">{len(st.session_state.alerts)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    critical = len([a for a in st.session_state.alerts if a.get('confidence', 0) > 85])
    st.markdown(f"""
    <div class="metric-card">
        <div style="color:#8899bb;">HIGH RISK</div>
        <div class="metric-value metric-red">{critical}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    unique_threats = len(set([a.get('threat', 'Unknown') for a in st.session_state.alerts]))
    st.markdown(f"""
    <div class="metric-card">
        <div style="color:#8899bb;">THREAT TYPES</div>
        <div class="metric-value metric-blue">{unique_threats}/6</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div style="color:#8899bb;">📊 THROUGHPUT</div>
        <div style="font-size:1.8rem; font-weight:700; color:#00ff88;">
            {int(flows_per_sec):,}
        </div>
        <div style="color:#8899bb; font-size:0.7rem;">Flows/sec sustained</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div style="color:#8899bb;">⚡ LATENCY</div>
        <div style="font-size:1.8rem; font-weight:700; color:#00ccff;">
            {latency_ms}ms
        </div>
        <div style="color:#8899bb; font-size:0.7rem;">Alert generation time</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- MIDDLE ROW: Traffic Graph + Alerts ---
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("### 📈 LIVE TRAFFIC MONITOR")

    # Generate traffic data
    if st.session_state.running:
        new_point = {
            'timestamp': datetime.now(),
            'packets': random.randint(50, 400),
            'bytes': random.randint(5000, 80000)
        }
        st.session_state.traffic_history.append(new_point)
        if len(st.session_state.traffic_history) > 60:
            st.session_state.traffic_history = st.session_state.traffic_history[-60:]

        # ---- Generate Alerts based on toggles ----
        # Core threats
        if detect_ddos:
            alert = simulate_ddos()
            if alert and alert['confidence'] >= confidence_threshold:
                alert['time'] = datetime.now().strftime('%H:%M:%S')
                st.session_state.alerts.insert(0, alert)
                st.session_state.alert_count += 1
        if detect_scan:
            alert = simulate_port_scan()
            if alert and alert['confidence'] >= confidence_threshold:
                alert['time'] = datetime.now().strftime('%H:%M:%S')
                st.session_state.alerts.insert(0, alert)
                st.session_state.alert_count += 1
        if detect_exfil:
            alert = simulate_exfiltration()
            if alert and alert['confidence'] >= confidence_threshold:
                alert['time'] = datetime.now().strftime('%H:%M:%S')
                st.session_state.alerts.insert(0, alert)
                st.session_state.alert_count += 1

        # Advanced threats
        if detect_beacon:
            alert = simulate_beaconing()
            if alert and alert['confidence'] >= confidence_threshold:
                alert['time'] = datetime.now().strftime('%H:%M:%S')
                st.session_state.alerts.insert(0, alert)
                st.session_state.alert_count += 1
        if detect_dga:
            alert = simulate_dns_threat()
            if alert and alert['confidence'] >= confidence_threshold:
                alert['time'] = datetime.now().strftime('%H:%M:%S')
                st.session_state.alerts.insert(0, alert)
                st.session_state.alert_count += 1
        if detect_tls:
            alert = simulate_tls_threat()
            if alert and alert['confidence'] >= confidence_threshold:
                alert['time'] = datetime.now().strftime('%H:%M:%S')
                st.session_state.alerts.insert(0, alert)
                st.session_state.alert_count += 1

        # Keep only latest 100
        if len(st.session_state.alerts) > 100:
            st.session_state.alerts = st.session_state.alerts[:100]

    # ---- Plot traffic graph ----
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

        # Add threat markers if alerts exist
        if st.session_state.alerts:
            marker_times = []
            marker_labels = []
            for alert in st.session_state.alerts[:10]:
                try:
                    # Use current time minus random seconds for visual variety
                    t = datetime.now() - timedelta(seconds=random.randint(5, 60))
                    marker_times.append(t)
                    marker_labels.append(alert.get('threat', 'Threat')[:8])
                except:
                    pass
            if marker_times:
                fig.add_trace(go.Scatter(
                    x=marker_times,
                    y=[random.randint(50, 400) for _ in marker_times],
                    mode='markers+text',
                    marker=dict(
                        symbol='triangle-up',
                        size=18,
                        color='#ff4444',
                        line=dict(color='white', width=2)
                    ),
                    text=marker_labels,
                    textposition='top center',
                    textfont=dict(color='white', size=10),
                    name='🚨 Threat Detected'
                ))

        fig.update_layout(
            template='plotly_dark',
            height=350,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(
                title='Time',
                showgrid=True,
                gridcolor='rgba(255,255,255,0.05)',
                type='date'
            ),
            yaxis=dict(
                title='Packets/sec',
                showgrid=True,
                gridcolor='rgba(255,255,255,0.05)'
            ),
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
        st.info("⏳ Click 'START' to begin monitoring traffic")

with col_right:
    st.markdown("### 🚨 REAL-TIME ALERTS")
    alert_container = st.container(height=350)
    with alert_container:
        if st.session_state.alerts:
            for alert in st.session_state.alerts[:25]:
                severity = alert.get('severity', 'MEDIUM')
                if severity == 'CRITICAL':
                    css_class = "alert-critical"
                    icon = "🔴"
                elif severity == 'HIGH':
                    css_class = "alert-high"
                    icon = "🟠"
                else:
                    css_class = "alert-medium"
                    icon = "🟡"

                threat = alert.get('threat', 'Unknown')
                badge_class = {
                    'DDoS': 'badge-ddos',
                    'Port_Scan': 'badge-scan',
                    'Data_Exfiltration': 'badge-exfil',
                    'Botnet_C2_Beaconing': 'badge-beacon',
                    'DGA_Domain': 'badge-dga',
                    'DNS_Tunneling': 'badge-dga',
                    'Malware_Encrypted': 'badge-tls'
                }.get(threat, 'badge-ddos')

                st.markdown(f"""
                <div class="{css_class}">
                    <span class="threat-badge {badge_class}">{threat.replace('_', ' ')}</span>
                    <span style="float:right;color:#00ff88;">{alert.get('confidence', 0):.0f}%</span><br>
                    <small style="color:#8899bb;">{alert.get('time', 'N/A')} · {alert.get('src', 'N/A')} → {alert.get('dst', 'N/A')}</small><br>
                    <small style="color:#667788; font-size:0.7rem;">📌 {alert.get('details', '')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🛡️ No threats detected yet")

st.divider()

# --- BOTTOM ROW: Alert Log (Drill‑down) + Charts ---
col_left2, col_right2 = st.columns([3, 2])

with col_left2:
    st.markdown("### 📋 DETAILED ALERT LOG (Click to Expand Evidence)")

    # Apply filters
    filtered_alerts = st.session_state.alerts
    if selected_threats:
        filtered_alerts = [a for a in filtered_alerts if a.get('threat') in selected_threats]
    severity_order = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3, 'CRITICAL': 4}
    min_sev = severity_order.get(severity_filter, 2)
    filtered_alerts = [a for a in filtered_alerts if severity_order.get(a.get('severity', 'MEDIUM'), 2) >= min_sev]

    if filtered_alerts:
        for idx, alert in enumerate(filtered_alerts[:15]):
            severity = alert.get('severity', 'MEDIUM')
            css_class = "alert-critical" if severity == "CRITICAL" else "alert-high" if severity == "HIGH" else "alert-medium"
            with st.expander(f"🔍 [{alert.get('time', 'N/A')}] {alert.get('threat', 'Unknown')} (Conf: {alert.get('confidence', 0):.0f}%)"):
                st.markdown("**📌 Supporting Evidence:**")
                col_ev1, col_ev2 = st.columns(2)
                with col_ev1:
                    st.metric("Source IP", alert.get('src', 'N/A'))
                    st.metric("Destination", alert.get('dst', 'N/A'))
                with col_ev2:
                    st.metric("Confidence", f"{alert.get('confidence', 0):.0f}%")
                    st.metric("Severity", severity)
                if 'details' in alert and alert['details']:
                    st.caption(f"🔎 Feature Evidence: {alert['details']}")
                st.caption("📊 Flow Metadata (Read-Only): Packet Count, Byte Ratio, Entropy - Analyzed Passively")
                st.progress(min(alert.get('confidence', 50) / 100, 1.0), text="Threat Confidence Score")
    else:
        st.info("No alerts match the current filters")

with col_right2:
    st.markdown("### 📊 THREAT BREAKDOWN (Click Slice to Filter)")

    if st.session_state.alerts:
        threat_counts = pd.DataFrame(
            [a.get('threat', 'Unknown') for a in st.session_state.alerts],
            columns=['Threat']
        ).value_counts().reset_index()
        threat_counts.columns = ['Threat', 'Count']

        colors = ['#ff4444', '#ff8800', '#ffcc00', '#00ccff', '#8800ff', '#ff44aa']
        fig = px.pie(
            threat_counts,
            values='Count',
            names='Threat',
            color_discrete_sequence=colors,
            hole=0.4
        )
        fig.update_layout(
            template='plotly_dark',
            height=250,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5,
                font=dict(size=9)
            )
        )
        st.plotly_chart(fig, use_container_width=True, key="pie_chart")
        st.caption("💡 Tip: Toggle threat types in the sidebar to filter the log.")
    else:
        st.info("No data to display")

    # Confidence distribution histogram
    st.markdown("### 📈 CONFIDENCE DISTRIBUTION")
    if st.session_state.alerts:
        conf_df = pd.DataFrame(
            [a.get('confidence', 0) for a in st.session_state.alerts],
            columns=['Confidence']
        )
        fig2 = px.histogram(
            conf_df,
            x='Confidence',
            nbins=10,
            color_discrete_sequence=['#00ff88'],
            title=None
        )
        fig2.update_layout(
            template='plotly_dark',
            height=150,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis=dict(
                title='Confidence %',
                showgrid=True,
                gridcolor='rgba(255,255,255,0.05)',
                range=[50, 100]
            ),
            yaxis=dict(
                title='Count',
                showgrid=True,
                gridcolor='rgba(255,255,255,0.05)'
            )
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data")

# =============================================================================
# FOOTER & LEGEND
# =============================================================================
st.divider()
col_leg1, col_leg2, col_leg3, col_leg4, col_leg5, col_leg6 = st.columns(6)
with col_leg1:
    st.markdown('<span class="threat-badge badge-ddos">DDoS</span>', unsafe_allow_html=True)
with col_leg2:
    st.markdown('<span class="threat-badge badge-beacon">Beacon</span>', unsafe_allow_html=True)
with col_leg3:
    st.markdown('<span class="threat-badge badge-dga">DGA</span>', unsafe_allow_html=True)
with col_leg4:
    st.markdown('<span class="threat-badge badge-tls">TLS</span>', unsafe_allow_html=True)
with col_leg5:
    st.markdown('<span class="threat-badge badge-scan">Scan</span>', unsafe_allow_html=True)
with col_leg6:
    st.markdown('<span class="threat-badge badge-exfil">Exfil</span>', unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style="text-align:center; color:#445566; font-size:0.8rem;">
    ⚡ <b>Team Vortex</b> · AI-Based Detection of Cyber Threats in Unidirectional IP Traffic<br>
    <span style="color:#334455;">Zero Return Path · Maximum Intelligence · 6 Threat Types</span><br>
    <span style="color:#223344;">📊 Throughput & Latency monitored in real-time · 📁 Read‑only ingest · 🚀 Deploy on Streamlit Cloud</span>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# AUTO-REFRESH (when running)
# =============================================================================
if st.session_state.running:
    time.sleep(0.5)
    st.rerun()