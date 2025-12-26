import requests
from config import openWeatherAPIKey

LAT = 51.7612
LON = -1.2466

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def fetch_weather():
    params = {
        "lat": LAT,
        "lon": LON,
        "units": "metric",
        "appid": openWeatherAPIKey
    }

    current = requests.get(CURRENT_URL, params=params, timeout=10)
    current.raise_for_status()

    forecast = requests.get(FORECAST_URL, params=params, timeout=10)
    forecast.raise_for_status()

    return {
        "current": current.json(),
        "forecast": forecast.json()
    }
