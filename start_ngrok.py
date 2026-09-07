from pyngrok import ngrok
import subprocess
import time
import os

# Replace with YOUR actual token from ngrok.com
AUTH_TOKEN = "35V9EJqge4wCAeaeH0S4yEMAxzl_3yM1onxxf9rGNeLhWucaw"

# Authenticate
ngrok.set_auth_token(AUTH_TOKEN)

# Start Streamlit in the background (if not already running)
print("🚀 Starting Streamlit...")
subprocess.Popen(["streamlit", "run", "app.py", "--server.port", "8501"])

# Wait for Streamlit to start
time.sleep(5)

# Create the tunnel
public_url = ngrok.connect(8501)
print(f"✅ Public URL: {public_url}")
print("🔗 Share this link with the judges!")
print("⚠️ Keep this terminal open. Press Ctrl+C to stop.")

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("🛑 Shutting down...")
    ngrok.disconnect(public_url)
    ngrok.kill()