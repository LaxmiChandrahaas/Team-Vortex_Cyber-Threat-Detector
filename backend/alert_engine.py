import json
from datetime import datetime

def generate_alert(flow, prediction, threat_type='anomaly'):
    """
    Generate a structured alert.
    Schema: timestamp, flow_id, threat_class, confidence_score, evidence
    """
    alert = {
        'timestamp': datetime.now().isoformat(),
        'flow_id': f"{flow['src_ip']}_{flow['dst_ip']}_{flow['dst_port']}",
        'threat_class': prediction['threat_class'],
        'confidence_score': prediction['confidence_score'],
        'threat_type': threat_type,
        'evidence': {
            'packet_count': flow['packet_count'],
            'byte_count': flow['byte_count'],
            'unique_src_ports': flow['unique_src_ports'],
            'avg_packet_size': flow['avg_packet_size']
        },
        'src_ip': flow['src_ip'],
        'dst_ip': flow['dst_ip'],
        'dst_port': flow['dst_port'],
        'protocol': flow['protocol']
    }
    return alert

def save_alert(alert, log_file='alerts.jsonl'):
    """Append alert to log file."""
    with open(log_file, 'a') as f:
        f.write(json.dumps(alert) + '\n')