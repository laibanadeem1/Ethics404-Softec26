import re

def split_emails(raw_text: str) -> list[str]:
    """
    Auto-detect email boundaries using common email header patterns.
    Splits when a new email header pattern appears after some content.
    Falls back to --- splitting, then treats as single email.
    """

    # These patterns signal the start of a new email
    boundary_pattern = re.compile(
        r'(?=\n[ \t]*(?:From|Subject|Date|Dear|To)\s*[:\,])',
        re.IGNORECASE
    )

    parts = boundary_pattern.split(raw_text)
    parts = [p.strip() for p in parts if p.strip()]

    # fallback 1: try --- splitting
    if len(parts) <= 1:
        parts = [p.strip() for p in raw_text.split("---") if p.strip()]

    # fallback 2: treat whole thing as one email
    if not parts:
        parts = [raw_text.strip()]

    return parts