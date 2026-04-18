from extractor import extract_and_classify
from utils import split_emails

def process_all_emails(raw_text: str) -> list[dict]:
    emails = split_emails(raw_text)
    results = []

    for i, email in enumerate(emails):
        result = extract_and_classify(email)
        result["email_index"] = i + 1
        results.append(result)

    return results