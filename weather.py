

# utils/weather.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather_by_location(location):
    if not API_KEY:
        return None, "Weather API key missing."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return None, data.get("message", "Failed to fetch weather")

        temp = data["main"]["temp"]
        condition = data["weather"][0]["main"]  # e.g., Rain, Clear, Snow
        return {"temperature": temp, "condition": condition}, None

    except Exception as e:
        return None, str(e)
