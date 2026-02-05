import os
import requests
from typing import Dict, Any

class WeatherTool:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city: str) -> Dict[str, Any]:
        """
        Fetches current weather for a specified city.
        """
        if not self.api_key:
            return {"error": "OPENWEATHER_API_KEY not found."}
        
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data["name"],
                "temperature": f"{data['main']['temp']}°C",
                "condition": data["weather"][0]["description"],
                "humidity": f"{data['main']['humidity']}%"
            }
        else:
            return {"error": f"Failed to fetch weather for {city}. Status code: {response.status_code}"}

    def run(self, action: str, **kwargs) -> Any:
        if action == "get_weather":
            return self.get_weather(kwargs.get("city"))
        return {"error": "Unknown action"}
