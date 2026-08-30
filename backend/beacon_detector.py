"""
beacon_detector.py - Detects Botnet C2 beaconing using periodicity analysis
"""

import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import datetime, timedelta

def detect_beaconing(flow_df, time_window_seconds=60, threshold_std=0.1):
    """
    Detect C2 beaconing by analyzing flow intervals.
    Beaconing has very low variance in inter-arrival times.
    
    Args:
        flow_df: DataFrame with columns ['src_ip', 'dst_ip', 'timestamp']
        time_window_seconds: Window to look for patterns
        threshold_std: Standard deviation threshold for periodicity
    
    Returns:
        List of alerts
    """
    alerts = []
    
    # Group flows by (src_ip, dst_ip)
    grouped = flow_df.groupby(['src_ip', 'dst_ip'])
    
    for (src, dst), group in grouped:
        if len(group) < 5:  # Need at least 5 packets to detect periodicity
            continue
            
        # Sort by timestamp
        group = group.sort_values('timestamp')
        timestamps = group['timestamp'].values
        
        # Calculate inter-arrival times (in seconds)
        diffs = np.diff(timestamps)
        
        if len(diffs) < 3:
            continue
        
        # Check if intervals are highly regular (low standard deviation)
        std_dev = np.std(diffs)
        mean = np.mean(diffs)
        
        # If std_dev is very small relative to mean, it's periodic (beaconing)
        if mean > 0 and (std_dev / mean) < threshold_std:
            alerts.append({
                'src_ip': src,
                'dst_ip': dst,
                'threat': 'Botnet_C2_Beaconing',
                'interval_avg': round(mean, 2),
                'interval_std': round(std_dev, 2),
                'packet_count': len(group),
                'confidence': min(95, 70 + (1 - (std_dev / mean)) * 30)
            })
    
    return alerts

# --- For dashboard simulation (if no real data) ---
def simulate_beaconing():
    """Generate synthetic beaconing alerts for demo"""
    import random
    if random.random() < 0.15:  # 15% chance
        src = f"192.168.1.{random.randint(100, 150)}"
        dst = f"45.33.{random.randint(1,255)}.{random.randint(1,255)}"
        return {
            'src_ip': src,
            'dst_ip': dst,
            'threat': 'Botnet_C2_Beaconing',
            'interval_avg': round(random.uniform(15, 30), 1),
            'interval_std': round(random.uniform(0.5, 2.5), 2),
            'packet_count': random.randint(10, 50),
            'confidence': random.randint(78, 96)
        }
    return None