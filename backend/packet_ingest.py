from scapy.all import rdpcap, IP, TCP, UDP, ICMP
import pandas as pd
from datetime import datetime

def ingest_pcap(file_path, max_packets=None):
    """
    Read packets from a PCAP file (read-only mode).
    Returns a DataFrame with raw packet metadata.
    """
    packets = rdpcap(file_path)
    
    if max_packets:
        packets = packets[:max_packets]
        
    
    data = []
    for pkt in packets:
        if IP in pkt:
            # Extract 5-tuple: src_ip, dst_ip, src_port, dst_port, protocol
            ip_layer = pkt[IP]
            src_ip = ip_layer.src
            dst_ip = ip_layer.dst
            protocol = ip_layer.proto
            
            src_port = None
            dst_port = None
            
            if TCP in pkt:
                src_port = pkt[TCP].sport
                dst_port = pkt[TCP].dport
                protocol_name = 'TCP'
            elif UDP in pkt:
                src_port = pkt[UDP].sport
                dst_port = pkt[UDP].dport
                protocol_name = 'UDP'
            else:
                protocol_name = 'OTHER'
            
            data.append({
                'timestamp': datetime.now().isoformat(),
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'src_port': src_port,
                'dst_port': dst_port,
                'protocol': protocol_name,
                'packet_size': len(pkt),
                'ttl': ip_layer.ttl
            })
    
    return pd.DataFrame(data)

# Usage
# df = ingest_pcap('data/raw/sample.pcap', max_packets=1000)