from utils.weather_monitor import WeatherMonitor

if __name__ == "__main__":
    monitor = WeatherMonitor("./secrets.json", "./config.json")
    monitor.run()
