import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the correct model and API version (v1)
model = genai.GenerativeModel(model_name="gemini-pro")

def get_ai_response(user_message):
    try:
        response = model.generate_content(user_message)
        return response.text.strip()
    except Exception as e:
        return f"AI Error: {str(e)}"
