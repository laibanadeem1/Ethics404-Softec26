import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("key"))

def safe_generate(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f'{{"is_opportunity": false, "confidence": "low", "reason": "API error: {str(e)}"}}'