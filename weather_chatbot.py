import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Weather Pro Chatbot 🌦️", page_icon="🤖")

st.title("🤖 Weather Pro Chatbot")
st.markdown("Real-time weather + 5 day forecast 😎🌍")

# ---------------- SESSION STATE ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- WEATHER CODE MAP ----------------
def get_weather_icon(code):
    if code == 0:
        return "☀️ Clear Sky"
    elif code in [1, 2, 3]:
        return "🌤️ Partly Cloudy"
    elif code in [45, 48]:
        return "🌫️ Fog"
    elif code in [51, 53, 55]:
        return "🌦️ Drizzle"
    elif code in [61, 63, 65]:
        return "🌧️ Rain"
    elif code in [71, 73, 75]:
        return "❄️ Snow"
    elif code in [95]:
        return "⛈️ Thunderstorm"
    else:
        return "🌍 Unknown"

# ---------------- INPUT ----------------
user_input = st.chat_input("Type city name...")

# ---------------- LOGIC ----------------
if user_input:
    city = user_input.lower()
    st.session_state.chat.append(("user", user_input))

    if city == "bye":
        reply = "Bye bhai 😴"
        st.session_state.chat.append(("bot", reply))

    else:
        try:
            # STEP 1: Geocoding
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
            geo_res = requests.get(geo_url)
            geo_data = geo_res.json()

            if "results" not in geo_data:
                reply = "Bhai city sahi lih 😅 mala sapadla nahi"

            else:
                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]

                # STEP 2: Weather + Forecast
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto"
                weather_res = requests.get(weather_url)

                if weather_res.status_code != 200:
                    reply = "API error bhai 😅"

                else:
                    data = weather_res.json()

                    current = data["current_weather"]
                    daily = data["daily"]

                    temp = current["temperature"]
                    wind = current["windspeed"]
                    code = current["weathercode"]

                    icon = get_weather_icon(code)

                    reply = f"""
### 🌦️ {city.title()} Weather

{icon}

🌡️ Temperature: {temp}°C  
💨 Wind: {wind} km/h  

---

### 📅 5 Day Forecast:
"""

                    # Forecast loop
                    for i in range(5):
                        day_max = daily["temperature_2m_max"][i]
                        day_min = daily["temperature_2m_min"][i]
                        day_code = daily["weathercode"][i]

                        day_icon = get_weather_icon(day_code)

                        reply += f"\nDay {i+1}: {day_icon} | {day_min}°C - {day_max}°C"

        except:
            reply = "Something went wrong 😅"

        st.session_state.chat.append(("bot", reply))

# ---------------- DISPLAY ----------------
for sender, msg in st.session_state.chat:
    with st.chat_message("user" if sender == "user" else "assistant"):
        st.markdown(msg)