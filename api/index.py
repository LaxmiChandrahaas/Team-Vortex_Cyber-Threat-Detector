from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# --- Helper Functions (Simulating your backend logic) ---
def generate_traffic():
    """Simulate traffic data point"""
    return {
        "timestamp": datetime.now().isoformat(),
        "packets": random.randint(50, 400),
        "bytes": random.randint(5000, 80000)
    }

def generate_alert():
    """Simulate a threat alert (matches your 6 threat types)"""
    threat_types = ['DDoS', 'Port_Scan', 'Data_Exfiltration', 
                    'Botnet_C2_Beaconing', 'DGA_Domain', 'Malware_Encrypted']
    # Weighted probability to match your original demo
    threat = random.choices(threat_types, weights=[20, 18, 15, 12, 10, 8], k=1)[0]
    confidence = random.randint(65, 98)
    severity = "CRITICAL" if confidence > 85 else "HIGH" if confidence > 70 else "MEDIUM"
    
    return {
        "time": datetime.now().strftime('%H:%M:%S'),
        "threat": threat,
        "confidence": confidence,
        "severity": severity,
        "src": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
        "dst": f"10.0.0.{random.randint(1,255)}",
        "details": f"Anomaly score: {round(random.uniform(0.7, 0.99), 2)}"
    }

# --- API Endpoint to get initial HTML ---
@app.get("/")
async def root():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Team Vortex - Cyber Threat Detection</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background: linear-gradient(135deg, #0a0e17 0%, #1a1a2e 50%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        
        /* Header */
        .header {
            text-align: center;
            padding: 20px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 3rem;
            background: linear-gradient(135deg, #00ff88, #00ccff, #8800ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 40px rgba(0,255,136,0.3);
        }
        .header p {
            color: #8899bb;
            letter-spacing: 2px;
            font-size: 1.1rem;
        }
        .header .tagline {
            color: #445566;
            font-size: 0.9rem;
            margin-top: 5px;
        }

        /* Metrics */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .metric-card:hover { transform: translateY(-5px); border-color: #00ff88; }
        .metric-card .label { color: #8899bb; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
        .metric-card .value { 
            font-size: 2.5rem; 
            font-weight: 700; 
            background: linear-gradient(135deg, #00ff88, #00ccff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 5px 0;
        }
        .metric-card .value.red { background: linear-gradient(135deg, #ff4444, #ff8800); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .metric-card .sub { color: #667788; font-size: 0.8rem; }
        .status-online { color: #00ff88; font-weight: bold; }

        /* Main Layout */
        .main-grid {
            display: grid;
            grid-template-columns: 3fr 2fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 20px;
        }
        .card h3 { color: #aabbcc; margin-bottom: 15px; font-weight: 400; letter-spacing: 1px; }
        .chart-container { height: 300px; position: relative; }

        /* Alerts */
        .alert-feed {
            max-height: 350px;
            overflow-y: auto;
        }
        .alert-feed::-webkit-scrollbar { width: 5px; }
        .alert-feed::-webkit-scrollbar-thumb { background: #00ff88; border-radius: 10px; }
        .alert-item {
            padding: 10px 15px;
            margin: 5px 0;
            border-radius: 8px;
            border-left: 4px solid #ffcc00;
            animation: slideIn 0.3s ease;
            background: rgba(255,255,255,0.03);
        }
        .alert-item.critical { border-left-color: #ff3333; background: rgba(255,50,50,0.1); }
        .alert-item.high { border-left-color: #ff9933; background: rgba(255,150,50,0.08); }
        .alert-item.medium { border-left-color: #ffcc00; background: rgba(255,255,50,0.05); }
        .alert-item .top { display: flex; justify-content: space-between; align-items: center; }
        .alert-item .threat { font-weight: 600; }
        .alert-item .conf { color: #00ff88; }
        .alert-item .meta { font-size: 0.8rem; color: #667788; margin-top: 4px; }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-10px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-right: 5px;
        }
        .badge-ddos { background: #ff3333; color: white; }
        .badge-scan { background: #ffcc00; color: #1a1a2e; }
        .badge-exfil { background: #00ccff; color: #1a1a2e; }
        .badge-beacon { background: #ff8800; color: white; }
        .badge-dga { background: #cc33ff; color: white; }
        .badge-tls { background: #ff44aa; color: white; }

        .bottom-section {
            display: grid;
            grid-template-columns: 3fr 2fr;
            gap: 20px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }
        th { text-align: left; color: #8899bb; font-weight: 400; border-bottom: 1px solid #334455; padding: 8px 5px; }
        td { padding: 8px 5px; border-bottom: 1px solid rgba(255,255,255,0.03); }

        @media (max-width: 768px) {
            .metrics-grid { grid-template-columns: repeat(2, 1fr); }
            .main-grid { grid-template-columns: 1fr; }
            .bottom-section { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
<div class="container">
    <!-- Header -->
    <div class="header">
        <h1>🛡️ TEAM VORTEX</h1>
        <p>AI-Powered Cyber Threat Detection • Zero Return Path • Maximum Intelligence</p>
        <div class="tagline">6 Threat Types: DDoS · Botnet C2 · DGA · TLS Malware · Port Scan · Exfiltration</div>
    </div>

    <!-- Metrics -->
    <div class="metrics-grid" id="metrics">
        <div class="metric-card"><div class="label">Total Threats</div><div class="value" id="total-threats">0</div><div class="sub">↑ Live</div></div>
        <div class="metric-card"><div class="label">High Risk</div><div class="value red" id="high-risk">0</div><div class="sub">🚨 Critical</div></div>
        <div class="metric-card"><div class="label">Threat Types</div><div class="value" id="threat-types">0/6</div><div class="sub">🔍 Detected</div></div>
        <div class="metric-card"><div class="label">System Status</div><div class="status-online" style="font-size:1.5rem;">🟢 MONITORING</div><div class="sub">⚡ Active</div></div>
    </div>

    <!-- Middle Section -->
    <div class="main-grid">
        <div class="card">
            <h3>📈 LIVE TRAFFIC MONITOR</h3>
            <div class="chart-container">
                <canvas id="trafficChart"></canvas>
            </div>
        </div>
        <div class="card">
            <h3>🚨 REAL-TIME ALERTS</h3>
            <div class="alert-feed" id="alertFeed"></div>
        </div>
    </div>

    <!-- Bottom Section -->
    <div class="bottom-section">
        <div class="card">
            <h3>📋 DETAILED ALERT LOG</h3>
            <div style="max-height:250px; overflow-y:auto;">
                <table>
                    <thead><tr><th>Time</th><th>Threat</th><th>Conf</th><th>Source</th></tr></thead>
                    <tbody id="alertTableBody"></tbody>
                </table>
            </div>
        </div>
        <div class="card">
            <h3>📊 THREAT BREAKDOWN</h3>
            <div id="threatStats" style="color:#8899bb; text-align:center; padding:20px;">Waiting for data...</div>
        </div>
    </div>
    <div style="text-align:center; color:#445566; margin-top:30px; font-size:0.8rem; border-top:1px solid #223344; padding-top:20px;">
        ⚡ Team Vortex · AI-Based Detection of Cyber Threats in Unidirectional IP Traffic
    </div>
</div>

<script>
    // --- Data State ---
    let alerts = [];
    let trafficData = [];
    const MAX_ALERTS = 50;
    const MAX_TRAFFIC = 30;
    const CHART_TYPES = ['DDoS', 'Port_Scan', 'Data_Exfiltration', 'Botnet_C2_Beaconing', 'DGA_Domain', 'Malware_Encrypted'];
    const BADGE_CLASSES = {
        'DDoS': 'badge-ddos', 'Port_Scan': 'badge-scan', 'Data_Exfiltration': 'badge-exfil',
        'Botnet_C2_Beaconing': 'badge-beacon', 'DGA_Domain': 'badge-dga', 'Malware_Encrypted': 'badge-tls'
    };

    // --- Chart Setup ---
    const ctx = document.getElementById('trafficChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                { label: 'Packets/sec', data: [], borderColor: '#00ff88', backgroundColor: 'rgba(0,255,136,0.1)', fill: true, tension: 0.3, yAxisID: 'y' },
                { label: 'Bytes/sec', data: [], borderColor: '#00ccff', backgroundColor: 'rgba(0,204,255,0.05)', fill: true, tension: 0.3, yAxisID: 'y1' }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 200 },
            plugins: { legend: { labels: { color: '#8899bb' } } },
            scales: {
                x: { ticks: { color: '#667788' }, grid: { color: 'rgba(255,255,255,0.03)' } },
                y: { type: 'linear', position: 'left', ticks: { color: '#00ff88' }, grid: { color: 'rgba(255,255,255,0.03)' } },
                y1: { type: 'linear', position: 'right', ticks: { color: '#00ccff' }, grid: { drawOnChartArea: false } }
            }
        }
    });

    // --- Helper Functions ---
    function getSeverity(conf) {
        if (conf > 85) return 'critical';
        if (conf > 70) return 'high';
        return 'medium';
    }

    function generateTraffic() {
        return { packets: Math.floor(Math.random() * 350) + 50, bytes: Math.floor(Math.random() * 75000) + 5000 };
    }

    function generateAlert() {
        const weights = [20, 18, 15, 12, 10, 8];
        let total = weights.reduce((a,b) => a+b, 0);
        let r = Math.random() * total;
        let selected = CHART_TYPES[0];
        for (let i = 0; i < weights.length; i++) {
            r -= weights[i];
            if (r <= 0) { selected = CHART_TYPES[i]; break; }
        }
        const conf = Math.floor(Math.random() * 33) + 65;
        return {
            time: new Date().toLocaleTimeString(),
            threat: selected,
            confidence: conf,
            severity: getSeverity(conf),
            src: `192.168.${Math.floor(Math.random()*255)+1}.${Math.floor(Math.random()*255)+1}`,
            dst: `10.0.0.${Math.floor(Math.random()*255)+1}`
        };
    }

    // --- Update UI ---
    function updateMetrics() {
        document.getElementById('total-threats').innerText = alerts.length;
        const high = alerts.filter(a => a.confidence > 85).length;
        document.getElementById('high-risk').innerText = high;
        const types = new Set(alerts.map(a => a.threat));
        document.getElementById('threat-types').innerText = `${types.size}/6`;
        
        // Update Threat Breakdown
        const container = document.getElementById('threatStats');
        if (alerts.length === 0) {
            container.innerHTML = '<div style="color:#667788;">No threats detected</div>';
            return;
        }
        const counts = {};
        alerts.forEach(a => { counts[a.threat] = (counts[a.threat] || 0) + 1; });
        let html = '<div style="text-align:left; font-size:0.9rem;">';
        for (const [key, value] of Object.entries(counts).sort((a,b) => b[1] - a[1])) {
            const pct = Math.round((value / alerts.length) * 100);
            html += `<div style="display:flex; justify-content:space-between; padding:3px 0; border-bottom:1px solid #223344;">
                        <span><span class="badge ${BADGE_CLASSES[key] || 'badge-ddos'}">${key.replace('_', ' ')}</span></span>
                        <span>${value} (${pct}%)</span>
                     </div>`;
        }
        html += '</div>';
        container.innerHTML = html;
    }

    function renderAlerts() {
        const feed = document.getElementById('alertFeed');
        const tbody = document.getElementById('alertTableBody');
        feed.innerHTML = '';
        tbody.innerHTML = '';
        
        const display = alerts.slice(0, 20);
        display.forEach(a => {
            const div = document.createElement('div');
            div.className = `alert-item ${a.severity}`;
            const badge = BADGE_CLASSES[a.threat] || 'badge-ddos';
            div.innerHTML = `
                <div class="top">
                    <div><span class="badge ${badge}">${a.threat.replace('_', ' ')}</span></div>
                    <div class="conf">${a.confidence}%</div>
                </div>
                <div class="meta">${a.time} · ${a.src} → ${a.dst}</div>
            `;
            feed.appendChild(div);
            
            // Table row
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${a.time}</td><td>${a.threat}</td><td>${a.confidence}%</td><td>${a.src}</td>`;
            tbody.appendChild(tr);
        });
        
        if (alerts.length === 0) {
            feed.innerHTML = '<div style="color:#667788; padding:20px; text-align:center;">🛡️ No threats detected yet</div>';
        }
        updateMetrics();
    }

    function updateTraffic() {
        const point = generateTraffic();
        trafficData.push(point);
        if (trafficData.length > MAX_TRAFFIC) trafficData.shift();
        
        const labels = trafficData.map((_, i) => `T-${trafficData.length - i}`);
        const packets = trafficData.map(d => d.packets);
        const bytes = trafficData.map(d => d.bytes);
        
        chart.data.labels = labels;
        chart.data.datasets[0].data = packets;
        chart.data.datasets[1].data = bytes;
        chart.update('none');
    }

    // --- Main Simulation Loop ---
    function tick() {
        // Update traffic
        updateTraffic();
        
        // Generate random alert (15% chance)
        if (Math.random() < 0.15) {
            const alert = generateAlert();
            alerts.unshift(alert);
            if (alerts.length > MAX_ALERTS) alerts.pop();
            renderAlerts();
        } else {
            // Just refresh table if no new alert (to keep time up to date? No, we only add on alerts)
            // We will just re-render if needed.
        }
        // Update metrics even if no new alert (for stats)
        updateMetrics();
    }

    // Initial render
    renderAlerts();

    // Run every 1.5 seconds
    setInterval(tick, 1500);
    
    // Initial traffic fill
    for (let i = 0; i < 20; i++) {
        const p = generateTraffic();
        trafficData.push(p);
    }
    updateTraffic();
</script>
</body>
</html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# --- Optional: API endpoint for raw data (if needed) ---
@app.get("/api/alerts")
async def get_alerts():
    """Return the current alert list as JSON (for potential external integration)"""
    # Since this is serverless, we return a static random sample for the API.
    # The main HTML page handles its own state.
    sample = [generate_alert() for _ in range(5)]
    return sample

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "Team Vortex is running on Vercel!"}