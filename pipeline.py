import time
from extractor import extract_and_classify
from utils import split_emails,clean_email

def process_all_emails(raw_text: str, student_profile: dict = None) -> list[dict]:
    if student_profile and student_profile.get('cv_text'):
        student_profile['cv_text'] = clean_email(student_profile['cv_text'])
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
        result = extract_and_classify(email, student_profile)
        result["email_index"] = i + 1
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
            "red_flags": ["Duplicate email detected"]
        })

    # Sort by email_index so display order is clean
    results.sort(key=lambda x: x.get("email_index", 0))

    return results