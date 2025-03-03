import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Weather Prediction App",
    page_icon="🌤️",
    layout="wide"
)

# Custom CSS for styling

st.markdown("""
    <style>
        /* Main App Styling */
        .stApp {
            background: linear-gradient(135deg, #1e3799, #0984e3);
            color: white;
        }
        
        /* Title and Headers */
        .main-title {
            text-align: center;
            font-size: 5px;
            padding: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            margin-bottom: 10px;
        }
        
        .sub-title {
            text-align: center;
            font-size: 1.5em;
            margin-bottom: 10px;
            color: rgba(255,255,255,0.9);
        }
        
        /* Search Box Styling */
        .search-container {
            background: rgba(255,255,255,0.1);
            padding: 2px;
            border-radius: 2px;
            backdrop-filter: black;
        }
        
        /* Weather Cards */
        .metric-card {
            background: rgba(255, 255, 255, 0.15);
            padding: 6px;
            border-radius: 0px;
            margin: 10px 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.2);
        }
        
        .metric-card h4 {
            font-size: 15px;
            color: rgba(255,255,255,0.9);
            margin-bottom: 15px;
            text-align:start;
        }
        
        .metric-card h2 {
            font-size: 2em;
            text-align: center;
            margin: 10px 0;
        }
        
        /* Button Styling */
        .stButton>button {
            background: linear-gradient(45deg, #00a8ff, #0097e6);
            color: white;
            border-radius: 10px;
            padding: 15px 30px;
            font-weight: bold;
            border: none;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        
        /* Input Field */
        .stTextInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.1);
            color: black;
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 5px;
            font-size: 1.1em;
        }
        
        /* Section Headers */
        .section-header {
            font-size: 1.8em;
            margin: 30px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255,255,255,0.1);
            text-align: center;
        }
        
        /* Sun Schedule */
        .sun-schedule {
            background: rgba(255,255,255,0.15);
            padding: 10px;
            border-radius: 15px;
            text-align: center;
            margin: 10px 0;
            backdrop-filter: blur(10px);
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 20px;
            margin-top: 50px;
            font-size: 0.9em;
            color: rgba(255,255,255,0.7);
            border-top: 1px solid rgba(255,255,255,0.1);
        }
        
        /* Weather Icon */
        .weather-icon {
            font-size: 4em;
            text-align: center;
            margin: 10px 0;
        }
        
        /* Temperature Display */
        .temperature-display {
            background: rgba(255,255,255,0.15);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            margin: 20px 0;
            backdrop-filter: blur(10px);
        }
        
        /* Alerts */
        .stAlert {
            background: rgba(255,255,255,0.15);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
    </style>
""", unsafe_allow_html=True)

# API Configuration
API_Key = "9dacc81457893340685c97091dc16f73"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    try:
        params = {
            "q": city,
            "appid": API_Key,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

def get_weather_icon(icon_code):
    weather_icons = {
        "01d": "☀️", "01n": "🌙", "02d": "⛅", "02n": "☁️",
        "03d": "☁️", "03n": "☁️", "04d": "☁️", "04n": "☁️",
        "09d": "🌧️", "09n": "🌧️", "10d": "🌦️", "10n": "🌧️",
        "11d": "⛈️", "11n": "⛈️", "13d": "🌨️", "13n": "🌨️",
        "50d": "🌫️", "50n": "🌫️"
    }
    return weather_icons.get(icon_code, "❓")

# Header
st.title("🌍 Weather Prediction App")
st.markdown("### Real-time Weather Information")

# City input
col1, col2 = st.columns([2, 1])
with col1:
    city = st.text_input("Enter City Name:", "Karachi")
with col2:
    if st.button("Get Weather", use_container_width=True):
        if city:
            weather_data = get_weather(city)
            
            if weather_data:
                # Current weather display
                st.markdown("## Current Weather")
                
                # Main weather info
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"### {get_weather_icon(weather_data['weather'][0]['icon'])} {weather_data['name']}, {weather_data['sys']['country']}")
                    st.markdown(f"#### {weather_data['weather'][0]['description'].title()}")
                
                with col2:
                    st.metric(
                        "Temperature",
                        f"{weather_data['main']['temp']}°C",
                        f"Feels like: {weather_data['main']['feels_like']}°C"
                    )
                
                with col3:
                    st.metric(
                        "Min/Max Temperature",
                        f"{weather_data['main']['temp_min']}°C / {weather_data['main']['temp_max']}°C"
                    )
                
                # Detailed weather info
                st.markdown("### Detailed Information")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown("""
                    <div class="metric-card text-center ">
                        <h4>Humidity</h4>
                        <h2>💧 {}%</h2>
                    </div>
                    """.format(weather_data['main']['humidity']), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="metric-card">
                        <h4 class =" text-small size:16px">Wind Speed</h4>
                        <h2>🌪️ {} m/s</h2>
                    </div>
                    """.format(weather_data['wind']['speed']), unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class="metric-card">
                        <h4>Pressure</h4>
                        <h2>📊 {} hPa</h2>
                    </div>
                    """.format(weather_data['main']['pressure']), unsafe_allow_html=True)
                
                with col4:
                    st.markdown("""
                    <div class="metric-card">
                        <h4>Visibility</h4>
                        <h2>👁️ {} km</h2>
                    </div>
                    """.format(round(weather_data['visibility']/1000, 1)), unsafe_allow_html=True)
                
                # Sunrise and Sunset
                st.markdown("### Sun Schedule")
                col1, col2 = st.columns(2)
                
                with col1:
                    sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M')
                    st.markdown(f"🌅 Sunrise: {sunrise}")
                
                with col2:
                    sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')
                    st.markdown(f"🌇 Sunset: {sunset}")
                
            else:
                st.error("Error fetching weather data. Please check the city name and try again.")
        else:
            st.warning("Please enter a city name.")

# Footer
st.markdown("---")
st.markdown("Data provided by OpenWeatherMap API | Last updated: " + 
           datetime.now().strftime("%Y-%m-%d %H:%M:%S"))