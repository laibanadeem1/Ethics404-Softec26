import re
import dns.resolver

def extract_domain(email_text: str) -> str:
    #Looks for "From: name@domain.com" and extracts "domain.com"
    match = re.search(r'From:\s*.*?[<]?.*?@([\w.-]+)[>]?', email_text, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return None

#Hardcoded lists (move these to a JSON file later)
TRUSTED_TLDS = [".edu", ".edu.pk", ".ac.pk", ".gov", ".gov.pk"]
TRUSTED_DOMAINS = ["hec.gov.pk", "nu.edu.pk", "pasha.org.pk", "fulbright.org"]
SUSPICIOUS_DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]

def check_domain_lists(domain: str) -> str:
    if not domain:
        return "unknown"
        
    if domain in TRUSTED_DOMAINS or any(domain.endswith(tld) for tld in TRUSTED_TLDS):
        return "legitimate"
        
    if domain in SUSPICIOUS_DOMAINS:
        return "suspicious"
        
    return "unknown"

def verify_mx_records(domain: str) -> bool:
    """Returns True if the domain has valid mail servers configured."""
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return len(records) > 0
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, Exception):
        return False
    

#main function that runs + integrates the functions above
# In authenticator.py
def evaluate_authenticity(email_text: str) -> dict:
    domain = extract_domain(email_text)
    
    if not domain:
        return {"status": "suspicious", "reason": "Could not extract sender domain."}
        
    # Check our lists first (fastest)
    list_status = check_domain_lists(domain)
    if list_status == "legitimate":
        return {"status": "legitimate", "reason": f"Domain {domain} is a trusted institutional domain."}
    if list_status == "suspicious":
        return {"status": "suspicious", "reason": f"Official opportunities rarely come from personal domains like {domain}."}
        
    # If unknown, check if the domain is actually real
    if not verify_mx_records(domain):
        return {"status": "suspicious", "reason": f"Domain {domain} does not have valid mail servers."}
        
    return {"status": "unknown", "reason": f"Domain {domain} has valid mail servers but is not explicitly trusted."}