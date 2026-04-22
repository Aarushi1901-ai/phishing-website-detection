import re
from urllib.parse import urlparse

def extract_features(url: str):
    """
    Extract numerical features from a URL, compatible with scikit-learn.
    Features:
    1. URL length
    2. Number of dots
    3. Presence of '@'
    4. Presence of '-'
    5. HTTPS usage
    6. Number of subdomains
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # 1. URL length
    url_length = len(url)
    
    # 2. Number of dots in the URL
    num_dots = url.count('.')
    
    # 3. Presence of '@'
    has_at = 1 if '@' in url else 0
    
    # 4. Presence of '-' in domain
    has_hyphen_in_domain = 1 if '-' in domain else 0
    
    # 5. HTTPS usage
    is_https = 1 if parsed_url.scheme == 'https' else 0
    
    # 6. Number of subdomains
    domain_parts = domain.split('.')
    # if it's www.example.com, parts = 3, subdomains = 2 (www counts as a part). 
    # Simply using len(domain_parts) is a sufficient proxy for number of subdomains here.
    num_subdomains = len(domain_parts)
    
    # Return numerical array format for scikit-learn
    return [[url_length, num_dots, has_at, has_hyphen_in_domain, is_https, num_subdomains]]

def get_feature_names():
    return [
        "URL length",
        "Number of dots",
        "Presence of '@'",
        "Presence of '-'",
        "HTTPS usage",
        "Number of subdomains"
    ]
