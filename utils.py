import re

def split_emails(raw_text: str) -> list[str]:
    if "---" in raw_text:
        parts = [p.strip() for p in raw_text.split("---") if p.strip()]
        return parts

    parts = re.split(r'\n(?=From\s*:)', raw_text, flags=re.IGNORECASE)
    parts = [p.strip() for p in parts if p.strip()]

    if not parts:
        return [raw_text.strip()]

    return parts