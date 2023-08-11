# Weather Monitor

The **Weather Monitor** is a Python script that fetches and displays weather information using the OpenWeatherMap API. This script allows you to keep track of temperature, humidity, and pressure for a specified city at regular intervals.

## Features

- Fetches weather data from the OpenWeatherMap API.
- Displays temperature, humidity, and pressure for a specified city.
- Configurable refresh interval for data retrieval.
- Handles API errors and exceptions gracefully.

## Prerequisites

- Python: Make sure you have Python installed on your system. You can download and install Python from the official [Python website](https://www.python.org/downloads/).

## Usage

1. Clone the repository or download the script directly.

2. Obtain an API Key:
   - To use the OpenWeatherMap API, you need to obtain an API key. You can sign up and get your API key from the [OpenWeatherMap website](https://home.openweathermap.org/users/sign_up).

3. Configuration:
   - Create a file named `secrets.json` in the same directory as the script. This file should contain your API key in the following format:

```
{
  "API_KEY": "your_api_key_here"
}
```

4. Create a file named config.json in the same directory to configure the script behavior. The file should have the following structure:
```
{
    "city": "your_city_name",
    "dt": refresh_interval_in_seconds
}
```
Replace `your_city_name` with the name of the city for which you want to monitor the weather, and set `refresh_interval_in_seconds` to the desired interval at which you want the script to fetch and display weather data.

## Execution:

- Open a terminal or command prompt.
- Navigate to the directory containing the script.
- Run the script using the following command:
`python weather_monitor.py`

## How It Works
The script defines a WeatherMonitor class that encapsulates the functionality.
JSON files (`secrets.json` and `config.json`) are loaded using the `load_json` method.
The `fetch_weather_data` method sends a request to the OpenWeatherMap API and handles exceptions.
The `display_weather_info` method extracts temperature, humidity, and pressure and prints the information.
The run method continuously fetches and displays weather data with the specified refresh interval.
The main block initializes the WeatherMonitor instance and starts the monitoring loop.

