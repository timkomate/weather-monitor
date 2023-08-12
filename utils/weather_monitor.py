import requests
import time
import json
import logging


class WeatherMonitor:
    def __init__(self, secrets_path, config_path):
        self.secrets = self.load_json(secrets_path)
        self.config = self.load_json(config_path)
        self.init_logging()

    @staticmethod
    def load_json(file_path):
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        return data

    def init_logging(self):
        logging.basicConfig(
                level = logging.INFO,
                format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def fetch_weather_data(self):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.config['city']}&units=metric&APPID={self.secrets['API_KEY']}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-2xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred while fetching weather data: {e}")
            return None

    def display_weather_info(self, weather_data):
        if weather_data:
            temp = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]
            pressure = weather_data["main"]["pressure"]
            self.logger.info(
                f"Temperature: {temp}°C, Humidity: {humidity}%, Pressure: {pressure} hPa"
            )

    def run(self):
        while True:
            weather_data = self.fetch_weather_data()
            if weather_data:
                self.display_weather_info(weather_data)
            time.sleep(self.config["dt"])


if __name__ == "__main__":
    monitor = WeatherMonitor("./secrets.json", "./config.json")
    monitor.run()
