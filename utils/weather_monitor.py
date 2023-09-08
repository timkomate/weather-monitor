import requests
import mariadb
import time
import json
import logging
import datetime


class WeatherMonitor:
    def __init__(self, secrets_path, config_path):
        self.secrets = self.load_json(secrets_path)
        self.config = self.load_json(config_path)
        self.init_logging()
        self.init_database_connection()

    @staticmethod
    def load_json(file_path):
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        return data

    def init_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def init_database_connection(self):
        try:
            self.conn = mariadb.connect(
                user=self.config["db_user"],
                password=self.secrets["db_password"],
                host=self.config["db_host"],
                port=self.config["db_port"],
                database=self.config["db_name"],
                autocommit=False,
            )
            self.cur = self.conn.cursor()
            self.logger.info("Database connection is ready")
        except mariadb.Error as e:
            self.logger.error(
                f"An error occurred while connecting to the database: {e}"
            )
            sys.exit(1)

    def fetch_weather_data(self):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.config['city']}&units=metric&APPID={self.secrets['API_KEY']}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-2xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred while fetching weather data: {e}")
            return None

    def log_weather_data(self, weather_data):
        now = datetime.datetime.utcnow()
        if weather_data:
            temp = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]
            pressure = weather_data["main"]["pressure"]
            description = weather_data["weather"][0]["description"]
            windspeed = weather_data["wind"]["speed"]
            winddir = weather_data["wind"]["deg"]
            clouds = weather_data["clouds"]["all"]
            self.logger.info(weather_data)
            if "rain" in weather_data:
                rain = weather_data["rain"]["1h"]
            else:
                rain = 0
            self.logger.info(
                f"Temperature: {temp}*C, Humidity: {humidity}%, Pressure: {pressure} hPa, Rain: {rain} mm, Windspeed: {windspeed} km/h, Wind direction: {winddir}*, Clouds: {clouds}%, Description: {description}"
            )
            query = f"INSERT INTO {self.config['db_table_name']} (date, temperature, humidity, rain, pressure, windspeed, winddir,clouds, description) VALUES ('{now}', '{temp}', '{humidity}', '{rain}', '{pressure}', '{windspeed}', '{winddir}', '{clouds}','{description}')"
            self.logger.debug(query)
            try:
                self.cur.execute(query)
                self.conn.commit()
            except mariadb.Error as e:
                self.logger.error(
                    f"An error occurred while inserting data into the database: {e}"
                )
                self.conn.rollback()

    def run(self):
        while True:
            weather_data = self.fetch_weather_data()
            if weather_data:
                self.log_weather_data(weather_data)
            time.sleep(self.config["dt"])
