"""
tls_analyzer.py - Detects malware in encrypted sessions using JA3-like fingerprints
"""

import hashlib
import random
import re

# Known malicious JA3 fingerprints (simplified for demo)
# In production, these would be from a threat intelligence feed
MALICIOUS_JA3 = [
    'e1e2e3e4e5e6e7e8e9e0f1f2f3f4f5f6',  # Example Cobalt Strike
    'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6',  # Example Metasploit
    'deadbeefcafebabefeedfacec0ffee12',  # Example Generic Malware
    'c0ffee1234567890abcdefabcdef12345'   # Example Suspicious Client
]

def extract_tls_metadata(packet_data):
    """
    Extract TLS Client Hello metadata (Version, Ciphers, Extensions).
    This is done WITHOUT decryption.
    """
    # In a real PCAP, we'd parse these fields.
    # For simulation, we generate a synthetic fingerprint.
    if not packet_data:
        return None
    
    # Simulated extraction (real code would use scapy's TLS layer)
    # We'll create a consistent hash based on packet size and random seed
    hash_input = f"{packet_data.get('src_ip', '')}_{packet_data.get('dst_port', 0)}_{packet_data.get('packet_size', 0)}"
    fingerprint = hashlib.md5(hash_input.encode()).hexdigest()
    
    return {
        'ja3_fingerprint': fingerprint[:32],
        'tls_version': 'TLSv1.2',  # Simulated
        'cipher_suites': ['TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384'],
        'extensions': ['server_name', 'supported_groups', 'ec_point_formats']
    }

def detect_malicious_tls(fingerprint, confidence_threshold=65):
    """
    Compare extracted JA3 fingerprint against known malicious ones.
    """
    if not fingerprint:
        return False, 0
    
    # Check if fingerprint matches known malicious patterns
    for malicious in MALICIOUS_JA3:
        if fingerprint[:16] == malicious[:16]:  # Partial match for demo
            return True, random.randint(75, 95)
    
    # Heuristics: Check for unusual TLS version or missing extensions
    # (Simplified for demo)
    return False, 0

# --- For dashboard simulation ---
def simulate_malicious_tls():
    """Generate synthetic TLS malware alerts for demo"""
    if random.random() < 0.10:
        malware_names = ['CobaltStrike', 'Metasploit', 'Meterpreter', 'DarkComet']
        return {
            'threat': 'Malware_Encrypted',
            'ja3_fingerprint': random.choice(MALICIOUS_JA3),
            'malware_family': random.choice(malware_names),
            'confidence': random.randint(68, 94),
            'tls_version': 'TLSv1.2'
        }
    return None