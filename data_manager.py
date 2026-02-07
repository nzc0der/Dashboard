import requests
import random
import pandas as pd
from datetime import datetime

class DataManager:
    def __init__(self):
        # We can simulate stock data for the graph
        self.crypto_data = {
            'Bitcoin': [random.randint(40000, 45000) for _ in range(30)],
            'Ethereum': [random.randint(2800, 3200) for _ in range(30)],
            'Dates': pd.date_range(end=datetime.today(), periods=30).tolist()
        }

    def get_weather(self, lat=40.7128, long=-74.0060):
        """Fetches weather from Open-Meteo API (No Key Required)"""
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true"
            response = requests.get(url)
            data = response.json()
            return data['current_weather']
        except Exception as e:
            return {"temperature": "--", "windspeed": "--", "weathercode": 0}

    def get_quote(self):
        """Fetches a random inspirational quote"""
        try:
            # Using a free quote API
            response = requests.get("https://zenquotes.io/api/random")
            data = response.json()[0]
            return f"\"{data['q']}\" - {data['a']}"
        except:
            return "\"Code is poetry.\" - Unknown"

    def get_system_status(self):
        """Simulates fetching CPU/RAM usage"""
        return {
            'cpu': random.randint(10, 45),
            'ram': random.randint(30, 60),
            'network': random.randint(100, 900)
        }