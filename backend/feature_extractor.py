"""
feature_extractor.py - Extract features from packet data
"""

import pandas as pd
import numpy as np
from collections import defaultdict

def extract_flow_features(packet_df):
    """
    Convert raw packets into flow-level features.
    Each flow = unique (src_ip, dst_ip, dst_port, protocol)
    Returns features matching the model's expectations.
    """
    print("📊 Extracting flow features...")
    
    flows = defaultdict(lambda: {
        'packet_count': 0,
        'byte_count': 0,
        'src_ports': set(),
        'dst_ports': set(),
        'timestamps': []
    })
    
    for _, row in packet_df.iterrows():
        flow_key = (row.get('src_ip', '0.0.0.0'), 
                    row.get('dst_ip', '0.0.0.0'), 
                    row.get('dst_port', 0), 
                    row.get('protocol', 'TCP'))
        flow = flows[flow_key]
        flow['packet_count'] += 1
        flow['byte_count'] += row.get('packet_size', 0)
        flow['src_ports'].add(row.get('src_port', 0))
        flow['dst_ports'].add(row.get('dst_port', 0))
        flow['timestamps'].append(row.get('timestamp', 0))
    
    # Create DataFrame with features
    features = []
    for (src_ip, dst_ip, dst_port, protocol), flow in flows.items():
        features.append({
            'packet_count': flow['packet_count'],
            'byte_count': flow['byte_count'],
            'unique_src_ports': len(flow['src_ports']),
            'unique_dst_ports': len(flow['dst_ports']),
            'avg_packet_size': flow['byte_count'] / flow['packet_count'] if flow['packet_count'] > 0 else 0,
            'flow_duration': len(flow['timestamps']),
            # Add these to match the model's expectations (will be filled later)
            'src_port': 0,
            'dst_port': dst_port or 0,
        })
    
    df = pd.DataFrame(features)
    print(f"✅ Extracted features for {len(df)} flows")
    return df