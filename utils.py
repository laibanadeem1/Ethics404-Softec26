import re


def clean_email(text: str) -> str:
    """Clean raw email text before sending to model."""

    # Remove excessive whitespace and blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove email tracking pixels and base64 blobs
    text = re.sub(r'[A-Za-z0-9+/]{100,}={0,2}', '[image removed]', text)

    # Remove HTML tags if any leaked through
    text = re.sub(r'<[^>]+>', '', text)

    # Remove URLs but keep domain for legitimacy check
    # Replace full URLs with just the domain
    text = re.sub(r'https?://([a-zA-Z0-9.-]+)[^\s]*', r'[link: \1]', text)

    # Remove repeated dashes/equals used as dividers
    text = re.sub(r'[-=*_]{5,}', '', text)

    # Remove forwarded email headers noise
    text = re.sub(r'[-]+\s*Forwarded message\s*[-]+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'On .+ wrote:', '', text)

    # Remove excessive punctuation
    text = re.sub(r'[!]{2,}', '!', text)
    text = re.sub(r'[?]{2,}', '?', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text

def split_emails(raw_text: str) -> list[str]:
    """
    Split emails by --- separator first.
    If no --- found, split only on 'From:' at the start of a line.
    """

    # Primary: split by --- separator
    if "---" in raw_text:
        parts = [p.strip() for p in raw_text.split("---") if p.strip()]
        return [clean_email(p) for p in parts]

    # Fallback: split only when 'From:' appears at start of a new line
    parts = re.split(r'\n(?=From\s*:)', raw_text, flags=re.IGNORECASE)
    parts = [p.strip() for p in parts if p.strip()]

    if not parts:
        return [clean_email(raw_text.strip())]

    return [clean_email(p) for p in parts]
