import socket
import whois
import requests
from urllib.parse import urlparse
from datetime import datetime

def extract_domain(url: str) -> str:
    parsed = urlparse(url)
    domain = parsed.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def get_ip_from_domain(domain: str) -> str:
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def get_geolocation(ip: str) -> dict:
    if not ip:
        return {"country": "Unknown", "city": "Unknown"}
    try:
        # Using free ip-api.com
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get("status") == "success":
                return {"country": data.get("country", "Unknown"), "city": data.get("city", "Unknown")}
    except Exception as e:
        print(f"Geolocation API error: {e}")
    return {"country": "Unknown", "city": "Unknown"}

def get_domain_age(domain: str) -> int:
    try:
        domain_info = whois.whois(domain)
        creation_date = domain_info.creation_date
        
        if type(creation_date) is list:
            creation_date = creation_date[0]
            
        if isinstance(creation_date, datetime):
            now = datetime.now()
            age_days = (now - creation_date).days
            return age_days
            
        return -1 # Unknown
    except Exception as e:
        print(f"WHOIS error for {domain}: {e}")
        return -1

def get_domain_intelligence(url: str) -> dict:
    domain = extract_domain(url)
    if not domain:
        return {
            "ip": "Unknown",
            "country": "Unknown",
            "city": "Unknown",
            "domain_age": -1
        }
        
    ip = get_ip_from_domain(domain)
    geo = get_geolocation(ip)
    age = get_domain_age(domain)
    
    return {
        "ip": ip if ip else "Unknown",
        "country": geo.get("country", "Unknown"),
        "city": geo.get("city", "Unknown"),
        "domain_age": age
    }
