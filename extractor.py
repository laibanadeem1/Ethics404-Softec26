import json
from groq_client import safe_generate

def extract_and_classify(email_text: str, student_profile: dict = None) -> dict:
    
    profile_section = ""
    if student_profile and student_profile.get('cv_text'):
        profile_section = f"""
    Student Resume (use this to assess fit and personalize ranking):
    {student_profile['cv_text'][:1500]}
    """
    prompt = f"""You are an AI assistant for university students in Pakistan.
{profile_section}
Analyze the email below and reply with ONLY a valid JSON object. No markdown, no explanation, no text before or after the JSON.

If the email contains a real opportunity (internship, scholarship, fellowship, competition, hackathon, admission, research, exchange program), extract all details.
If it is NOT an opportunity (newsletter, marketing, spam, general announcement), set is_opportunity to false.

Return exactly this JSON structure:
{{
  "is_opportunity": true,
  "confidence": "high",
  "reason": "one sentence",
  "title": "opportunity name or null",
  "organization": "who is offering it or null",
  "type": "internship or scholarship or fellowship or competition or admission or research or other",
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
    
    # Print for debugging
    print("=== RAW RESPONSE ===")
    print(raw)
    print("====================")
    
    # Clean up response
    raw = raw.strip()
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()
    
    # Extract JSON if there's text around it
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
            "reason": "Failed to parse response.",
        }