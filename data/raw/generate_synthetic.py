import pandas as pd
import numpy as np
from datetime import datetime

# Generate 2000 synthetic flows
np.random.seed(42)
n = 2000

data = {
    'src_ip': [f"192.168.1.{np.random.randint(1,255)}" for _ in range(n)],
    'dst_ip': [f"10.0.0.{np.random.randint(1,255)}" for _ in range(n)],
    'src_port': np.random.randint(1024, 65535, n),
    'dst_port': np.random.choice([80, 443, 22, 53, 8080, 445, 21, 25], n),
    'protocol': np.random.choice(['TCP', 'UDP'], n),
    'packet_count': np.random.randint(1, 500, n),
    'byte_count': np.random.randint(100, 50000, n),
    'flow_duration': np.random.randint(1, 300, n),
    'unique_src_ports': np.random.randint(1, 10, n),
    'avg_packet_size': np.random.randint(40, 1500, n),
    'label': np.random.choice([0, 1], n, p=[0.8, 0.2])  # 20% malicious
}

df = pd.DataFrame(data)
df.to_csv('data/raw/synthetic_traffic.csv', index=False)
print(f"✅ Generated {len(df)} synthetic flows -> data/raw/synthetic_traffic.csv")
print(f"   Benign: {sum(df['label']==0)}, Malicious: {sum(df['label']==1)}")