def split_emails(raw_text: str) -> list[str]:
    """Split pasted emails by --- divider, clean empties."""
    emails = raw_text.split("---")
    return [e.strip() for e in emails if e.strip()]