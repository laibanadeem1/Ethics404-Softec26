import json
from gemini import safe_generate

def classify_email(email_text: str) -> dict:
    prompt = f"""
You are an email classifier for university students in Pakistan.

Decide if this email contains a real opportunity.
Real opportunities include: internship, scholarship, fellowship,
competition, hackathon, admission, research position, exchange program.

NOT opportunities: newsletters, event invites, marketing, 
notices, general announcements, spam.

Reply with ONLY valid JSON, no explanation, no markdown:
{{
  "is_opportunity": true or false,
  "type": "internship" | "scholarship" | "fellowship" | "competition" | "admission" | "research" | "other" | null,
  "confidence": "high" | "medium" | "low",
  "reason": "one sentence explaining your decision"
}}

Email:
{email_text}
"""
    raw = safe_generate(prompt)

    # strip markdown if gemini wraps it
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "is_opportunity": False,
            "type": None,
            "confidence": "low",
            "reason": "Failed to parse classifier response."
        }