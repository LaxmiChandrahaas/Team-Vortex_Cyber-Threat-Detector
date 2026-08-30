# 🛡️ Team Vortex: AI-Based Cyber Threat Detection

### *Zero Return Path. Maximum Intelligence.*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Problem Statement

Critical infrastructure (power plants, banks, water treatment) relies on **data diodes** and **passive mirroring**—meaning the security monitoring system can **only receive traffic**, never send a packet back. This eliminates the risk of a compromised monitoring system being used as a pivot point into the core network.

**The Challenge:** Build an AI/ML pipeline that ingests this **one-directional stream**, detects cyber threats in near real-time, and outputs standardized alerts—**without** decryption, return paths, or inline blocking.

---

## 🎯 Our Solution

Team Vortex delivers a fully interactive dashboard that simulates and detects **6 distinct threat types** using statistical analysis and machine learning models (Random Forest + Isolation Forest).

| Threat Type | Detection Method |
| :--- | :--- |
| 🔴 **Volumetric DDoS** | Flow rate spikes & Source-IP entropy |
| 🔵 **Botnet C2 Beaconing** | Periodicity analysis (Inter-arrival variance) |
| 🟣 **DGA / DNS Tunnelling** | Domain entropy, N-gram analysis & Query length |
| 🟥 **Malware in TLS** | JA3/JA4 fingerprint matching (Metadata only) |
| 🟠 **Port Scanning** | Fan-out pattern detection (Single source → Many ports) |
| 🟡 **Data Exfiltration** | Asymmetric outbound/inbound byte ratio |

---

## ✨ Advanced Dashboard Features

- **Live Traffic Monitor**: Real-time packet and byte rate graphs with threat markers.
- **Read-Only Ingest**: Upload PCAP/CSV files—strictly passive, no return path.
- **Performance Metrics**: Tracks **Throughput (flows/sec)** and **Alert Latency (ms)** live.
- **Interactive Filtering**: Filter alerts by Threat Type (Multi-select) and Severity (Slider).
- **Drill-Down Evidence**: Click on any alert to expand and view full supporting evidence (Packet Count, Byte Ratio, Entropy).
- **Export Alerts**: Download the entire alert log as a structured JSON file.
- **6 Threat Toggles**: Turn specific detection modules ON/OFF for live demos.

---

## 🏗️ System Architecture

```text
[Read-Only PCAP/CSV] -> [Feature Extraction] -> [ML Inference (RF + IF)] -> [Alert Engine] -> [Live Dashboard]

Architectural Compliance
✅ a. Read-Only Ingest: Files are read locally; no sockets or queries are sent.

✅ b. No Payload Decryption: TLS analysis relies on JA3 metadata (packet sizes, times, handshake strings).

✅ c. Streaming, not Batch: Dashboard updates every second with bounded latency (< 50ms).

✅ d. Defined Throughput: Tested and displays sustained flows/sec performance.

✅ e. Standardized Alerts: JSON schema includes Timestamp, Flow ID, Threat Class, Confidence, and Evidence.

🛠️ Tech Stack
Layer ->	Technology
Frontend & Dashboard  ->	Streamlit, Plotly, Matplotlib
Backend & ML  ->	Python, Scikit-learn (Random Forest, Isolation Forest)
Packet/Data Handling  ->	Pandas, Numpy, Scapy
Deployment  ->	GitHub + Streamlit Community Cloud

🚀 How to Run Locally:
1. Clone the Repository
bash
git clone https://github.com/yourusername/cyber-threat-detector.git
cd cyber-threat-detector

2. Create and Activate a Virtual Environment
Windows:

bash
python -m venv venv
.\venv\Scripts\Activate.ps1
macOS/Linux:

bash
python3 -m venv venv
source venv/bin/activate

3. Install Requirements
bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

4. Run the Dashboard
bash
python -m streamlit run app.py
The app will open automatically at http://localhost:8501.

☁️ Deploy to Streamlit Cloud (Free):

- Push this code to a GitHub repository.
- Go to share.streamlit.io.
- Click "New app", select your repo, and set the main file to app.py.
- Click Deploy.
- Get your live public URL (e.g., team-vortex.streamlit.app) to share with judges.

Project Structure:

cyber-threat-detector/
├── app.py                  # Main integrated dashboard (Streamlit)
├── requirements.txt        # Python dependencies
├── .gitignore              # Ignore venv, datasets, caches
├── backend/                # Core AI & Detection Logic
│   ├── packet_ingest.py    # Read PCAP files (Scapy)
│   ├── feature_extractor.py# Flow & entropy engineering
│   ├── model_trainer.py    # Random Forest & Isolation Forest training
│   ├── model_inference.py  # Real-time prediction pipeline
│   ├── alert_engine.py     # Standardized JSON alerts
│   └── ... (beacon, dns, tls detectors)
├── frontend/               # UI Components (optional, integrated into app.py)
└── data/                   # Datasets (Raw & Processed)
    └── raw/
        └── generate_synthetic.py  # Script to generate demo data

Contributors:
1. 
2. 
3. 
4. 
5. 
6. 

📜 License
This project is open-source and available under the MIT License.

