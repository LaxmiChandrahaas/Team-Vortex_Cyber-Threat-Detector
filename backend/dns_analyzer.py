"""
dns_analyzer.py - Detects DGA domains and DNS tunnelling using entropy and n-grams
"""

import re
import math
import random

def calculate_entropy(domain):
    """Calculate Shannon entropy of a domain name"""
    if not domain:
        return 0
    # Remove TLD (.com, .net, etc.) for better detection
    parts = domain.split('.')
    if len(parts) >= 2:
        domain = '.'.join(parts[:-1])  # Remove TLD
    
    # Count character frequencies
    freq = {}
    for char in domain:
        if char.isalnum():  # Only letters and numbers
            freq[char] = freq.get(char, 0) + 1
    
    total = sum(freq.values())
    if total == 0:
        return 0
    
    entropy = 0
    for count in freq.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def detect_dga(domain):
    """
    Detect DGA (Domain Generation Algorithm) domains.
    DGA domains have high entropy and random-looking characters.
    """
    if not domain:
        return False, 0
    
    entropy = calculate_entropy(domain)
    
    # Check for random-looking patterns (consecutive consonants/vowels)
    random_score = 0
    # Check for unusual character mixes
    if re.search(r'[0-9]{4,}', domain):  # 4+ numbers in a row
        random_score += 2
    if re.search(r'[aeiou]{1}[^aeiou]{4,}', domain, re.I):  # 4+ consonants after a vowel
        random_score += 2
    if re.search(r'[^aeiou]{5,}', domain, re.I):  # 5+ consonants in a row
        random_score += 1
    
    # Typical DGA domains have entropy > 3.5 (for English text)
    is_dga = (entropy > 3.5) or (random_score >= 2)
    confidence = min(95, 60 + (entropy - 3) * 20 + random_score * 5)
    
    return is_dga, min(confidence, 95)

def detect_dns_tunneling(query_length, record_type='TXT'):
    """
    Detect DNS tunneling based on query length and record type.
    Tunneling uses very long queries or unusual record types.
    """
    # Normal DNS queries are under 50 characters
    if query_length > 50:
        confidence = min(95, 70 + (query_length - 50) * 0.5)
        return True, confidence, "Long query length (exfiltration)"
    
    # Tunneling often uses TXT or NULL records
    if record_type in ['TXT', 'NULL'] and query_length > 20:
        return True, 75, "Unusual record type with moderate length"
    
    return False, 0, "Normal"

# --- For dashboard simulation ---
def simulate_dns_threat():
    """Generate synthetic DNS alerts for demo"""
    if random.random() < 0.12:
        # Generate a random-looking domain (like DGA)
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        domain = ''.join(random.choices(chars, k=random.randint(15, 25))) + '.xyz'
        
        # Check if it looks like DGA
        is_dga, conf = detect_dga(domain)
        
        if is_dga:
            return {
                'threat': 'DGA_Domain',
                'domain': domain,
                'confidence': conf,
                'entropy': round(calculate_entropy(domain), 2)
            }
        
        # Or simulate DNS Tunneling
        if random.random() < 0.5:
            long_query = 'A' * random.randint(60, 120)
            return {
                'threat': 'DNS_Tunneling',
                'domain': long_query + '.exfil.com',
                'confidence': random.randint(70, 92),
                'query_length': len(long_query) + 10
            }
    return None