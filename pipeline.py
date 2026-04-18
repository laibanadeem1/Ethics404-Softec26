import time
from extractor import extract_and_classify
from utils import split_emails

def process_all_emails(raw_text: str, student_profile: dict = None) -> list[dict]:
    emails = split_emails(raw_text)
    emails=emails[:15]
    results = []

    for i, email in enumerate(emails):
        print(f"Processing email {i+1}/{len(emails)}...")
        result = extract_and_classify(email, student_profile)
        result["email_index"] = i + 1
        results.append(result)
        
        # Wait 4 seconds between calls to avoid 429
        # 15 emails × 4s = 60s total, safe under 6000 TPM limit
        if i < len(emails) - 1:  # no need to wait after last email
            time.sleep(4)

    return results