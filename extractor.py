import json
from gemini import safe_generate

def extract_and_classify(email_text: str) -> dict:
    prompt = f"""
You are an AI assistant for university students in Pakistan.

First decide if this email contains a real opportunity.
Real opportunities: internship, scholarship, fellowship, competition,
hackathon, admission, research position, exchange program.
NOT opportunities: newsletters, marketing, general announcements, spam.

If it IS an opportunity, extract all fields.
If it is NOT, just return is_opportunity as false.

Reply with ONLY valid JSON, no explanation, no markdown:
{{
  "is_opportunity": true or false,
  "confidence": "high" | "medium" | "low",
  "reason": "one sentence",
  "title": "opportunity name or null",
  "organization": "who is offering it or null",
  "type": "internship | scholarship | fellowship | competition | admission | research | other | null",
  "deadline": "YYYY-MM-DD or null",
  "deadline_raw": "exact deadline text or null",
  "eligibility": "who can apply or null",
  "cgpa_required": "minimum CGPA as number or null",
  "degree_required": "e.g. BS CS or null",
  "semester_required": "e.g. 6th semester or null",
  "documents": ["list", "of", "documents"] or [],
  "skills_required": ["list", "of", "skills"] or [],
  "stipend_or_funding": "amount or null",
  "location": "city/country/remote or null",
  "link": "URL or null",
  "contact": "email or number or null",
  "next_steps": "what student should do to apply or null"
}}

Email:
{email_text}
"""
    raw = safe_generate(prompt)
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "is_opportunity": False,
            "confidence": "low",
            "reason": "Failed to parse response.",
        }