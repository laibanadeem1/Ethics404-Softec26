import re

def split_emails(raw_text: str) -> list[str]:
    """
    Split emails by --- separator first.
    If no --- found, split only on 'From:' at the start of a line.
    """

    # Primary: split by --- separator
    if "---" in raw_text:
        parts = [p.strip() for p in raw_text.split("---") if p.strip()]
        return parts

    # Fallback: split only when 'From:' appears at start of a new line
    # This won't split on Subject/Dear/Date inside an email
    parts = re.split(r'\n(?=From\s*:)', raw_text, flags=re.IGNORECASE)
    parts = [p.strip() for p in parts if p.strip()]

    if not parts:
        return [raw_text.strip()]

    return parts