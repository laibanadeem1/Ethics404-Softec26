import time
from extractor import extract_and_classify
from authenticator import evaluate_authenticity, extract_domain
from utils import split_emails

def process_all_emails(raw_text: str, student_profile: dict = None) -> list[dict]:
    emails = split_emails(raw_text)
    emails = emails[:15]

    # Deduplicate — remove emails with same first 100 chars
    seen = set()
    unique_emails = []
    duplicates = []

    for i, email in enumerate(emails):
        fingerprint = email.strip()[:100].lower()
        if fingerprint in seen:
            duplicates.append(i + 1)
            print(f"Email {i+1} is a duplicate — skipping")
        else:
            seen.add(fingerprint)
            unique_emails.append(email)

    results = []

    for i, email in enumerate(unique_emails):
        print(f"Processing email {i+1}/{len(unique_emails)}...")
        
        # 1. Run strict Python-based Authenticity Check
        auth_result = evaluate_authenticity(email)
        domain = extract_domain(email)
        
        # 2. Run LLM Extraction for the opportunity details
        result = extract_and_classify(email, student_profile)
        
        # 3. Merge the authentications results into the LLM output dict
        result["email_index"] = i + 1
        result["legitimacy"] = auth_result["status"]
        result["legitimacy_reason"] = auth_result["reason"]
        result["sender_domain"] = domain
        
        results.append(result)

        if i < len(unique_emails) - 1:
            time.sleep(4)

    # Add duplicates as ignored spam entries
    for dup_index in duplicates:
        results.append({
            "is_opportunity": False,
            "email_index": dup_index,
            "confidence": "high",
            "reason": "Duplicate email — already seen in this batch.",
            "legitimacy": "suspicious",
            "legitimacy_reason": "Repetitive emails are a spam indicator.",
            "red_flags": ["Duplicate email detected"],
            "sender_domain": None
        })

    # Sort by email_index so display order is clean
    results.sort(key=lambda x: x.get("email_index", 0))

    return results