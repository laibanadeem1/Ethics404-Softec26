import json
from groq_client import safe_generate

def extract_and_classify(email_text: str, student_profile: dict = None) -> dict:

    profile_section = ""
    if student_profile and student_profile.get('cv_text'):
        profile_section = f"""
Student Resume (use this to assess fit):
{student_profile['cv_text'][:500]}
"""

    prompt = f"""You are an AI assistant for university students in Pakistan.
{profile_section}

Analyze the email below and extract the opportunity details.

## TASK — OPPORTUNITY DETECTION & EXTRACTION
Decide if this email contains a real opportunity:
- Real: internship, scholarship, fellowship, competition, hackathon, admission, research, exchange program
- NOT real: newsletters, marketing, spam, shipment, OTP, promotions, general announcements

Reply with ONLY a valid JSON object, no markdown, no explanation:
{{
  "is_opportunity": true or false,
  "confidence": "high" or "medium" or "low",
  "reason": "one sentence explaining decision",
  "red_flags": ["list any red flags found in the text"] or [],
  "title": "opportunity name or null",
  "organization": "who is offering it or null",
  "type": "internship or scholarship or fellowship or competition or admission or research or other or null",
  "deadline": "YYYY-MM-DD or null",
  "deadline_raw": "exact deadline text or null",
  "eligibility": "who can apply or null",
  "cgpa_required": "minimum CGPA as number or null",
  "degree_required": "e.g. BS CS or null",
  "semester_required": "e.g. 6th semester or null",
  "documents": [],
  "skills_required": [],
  "stipend_or_funding": "amount or null",
  "location": "city/country/remote or null",
  "link": "URL or null",
  "contact": "email or number or null",
  "next_steps": "what student should do to apply or null"
}}

EMAIL TO ANALYZE:
{email_text}"""

    raw = safe_generate(prompt)

    print("=== RAW RESPONSE ===")
    print(raw)
    print("====================")

    raw = raw.strip()
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    if not raw.startswith("{"):
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            raw = raw[start:end]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print("STILL FAILED TO PARSE:", raw)
        return {
            "is_opportunity": False,
            "confidence": "low",
            "reason": "Failed to parse response."
        }