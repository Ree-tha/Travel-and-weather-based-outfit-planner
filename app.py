
import streamlit as st
import os
from utils.weather import get_weather_by_location
from utils.suggestion import suggest_outfit
from utils.trip_mode import plan_trip_outfits
from utils.ai_chat import get_ai_response

# Apply custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Create wardrobe folder if not exists
os.makedirs("data/wardrobe", exist_ok=True)

# Page config
st.set_page_config(page_title="AI Outfit Assistant", layout="centered")

st.title("👗 Personal AI Outfit Assistant")
st.markdown("Upload your wardrobe, choose your location and get outfit suggestions!")

# Upload clothes
uploaded_files = st.file_uploader("Upload clothes from your wardrobe (images)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
if uploaded_files:
    for file in uploaded_files:
        with open(os.path.join("data/wardrobe", file.name), "wb") as f:
            f.write(file.getbuffer())
    st.success(f"Uploaded {len(uploaded_files)} items to wardrobe.")

# Location input
location = st.text_input("Enter your location (City/State)", placeholder="e.g., Mysore")

# Occasion
occasion = st.selectbox("Select an occasion", ["None", "Casual", "Formal", "Party", "Outdoor"])

# Trip Mode
trip_mode = st.checkbox("Enable Trip Mode")

if trip_mode:
    st.markdown("### Trip Details")
    days = st.number_input("Number of Days", min_value=1, max_value=30, step=1)
    trip_locations = st.text_area("Enter places for the trip (comma-separated)", placeholder="e.g., Bangalore, Ooty, Mysore")


# ⬇️ Place below the Trip Mode section in app.py

if st.button("Get Outfit Suggestion"):
    if not location:
        st.warning("Please enter a location.")
    else:
        with st.spinner("Fetching weather and preparing suggestions..."):
            weather, error = get_weather_by_location(location)

            if error:
                st.error(f"Error: {error}")
            else:
                st.success(f"Weather in {location}: {weather['temperature']}°C, {weather['condition']}")

                suggestions = suggest_outfit(weather, occasion)

                if suggestions:
                    st.markdown("### 👕 Suggested Outfit Items:")
                    for item in suggestions:
                        st.image(f"data/wardrobe/{item}", width=200, caption=item)
                else:
                    st.warning("No suitable outfits found. Please upload more labeled clothes.")


# ⬇️ Add below the regular suggestion block
if trip_mode:
    if not trip_locations or not days:
        st.warning("Please enter trip locations and number of days.")
    else:
        trip_outfits, trip_error = plan_trip_outfits(trip_locations, days, occasion)
        if trip_error:
            st.error(trip_error)
        else:
            st.markdown("## 🧳 Trip Outfit Planner")
            for day_plan in trip_outfits:
                st.markdown(f"### Day {day_plan['day']} – {day_plan['location']}")
                if "error" in day_plan:
                    st.error(f"Could not fetch weather: {day_plan['error']}")
                else:
                    weather = day_plan["weather"]
                    st.info(f"Weather: {weather['temperature']}°C, {weather['condition']}")
                    if day_plan["suggestions"]:
                        for item in day_plan["suggestions"]:
                            st.image(f"data/wardrobe/{item}", width=200, caption=item)
                    else:
                        st.warning("No suitable outfit found for this day.")


st.markdown("---")
st.markdown("### 🤖 AI Fashion Assistant")
st.markdown("Ask me anything about outfits, travel packing, weather styling, etc.")

user_question = st.text_input("Your question", placeholder="e.g., What should I wear in Bangalore tomorrow?")

if user_question:
    with st.spinner("Thinking..."):
        ai_answer = get_ai_response(user_question)
    st.markdown("**Answer:**")
    st.success(ai_answer)
