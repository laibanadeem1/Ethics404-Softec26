import re
import time
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.0-flash-lite")

#models = genai.list_models()

#for m in models:
    #print(m.name, m.supported_generation_methods)

def safe_generate(prompt: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            return model.generate_content(prompt).text.strip()
        except ResourceExhausted as e:
            # extract exact wait time from the error message
            match = re.search(r'retry_delay\s*\{\s*seconds:\s*(\d+)', str(e))
            wait = int(match.group(1)) + 5 if match else 40

            if attempt < retries - 1:
                st.warning(f"⏳ Rate limit hit — retrying in {wait} seconds... (attempt {attempt + 1}/{retries})")
                time.sleep(wait)
            else:
                st.error("❌ Quota fully exhausted. Please get a new API key or wait until tomorrow.")
                st.stop()