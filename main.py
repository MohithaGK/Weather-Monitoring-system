import requests
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

API_KEY = '7f4f55d94e46c910283a59c457b59a6e'  # Replace with your OpenWeatherMap API Key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Use 'metric' for Celsius, 'imperial' for Fahrenheit
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None


def parse_weather_data(data):
    if data:
        temp = data['main']['temp']  # Current temperature
        feels_like = data['main']['feels_like']  # Perceived temperature
        humidity = data['main']['humidity']  # Humidity
        wind_speed = data['wind']['speed']  # Wind speed
        weather_condition = data['weather'][0]['main']
        timestamp = data['dt']
        return temp, feels_like, humidity, wind_speed, weather_condition, timestamp
    return None


def store_weather_data(city, temp, feels_like, humidity, wind_speed, condition, timestamp):
    # Check if file exists, if not create with headers
    file_exists = os.path.isfile('weather_data.csv')

    with open('weather_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write header if file does not exist
            writer.writerow(['City', 'Temp', 'Feels_Like', 'Humidity', 'Wind_Speed', 'Condition', 'Timestamp'])
        # Write weather data to file
        writer.writerow([city, temp, feels_like, humidity, wind_speed, condition, datetime.fromtimestamp(timestamp)])


def calculate_daily_summary(file='weather_data.csv'):
    if not os.path.exists(file):
        print("No weather data available.")
        return None

    df = pd.read_csv(file)

    # Ensure the Timestamp is parsed correctly
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = df['Timestamp'].dt.date

    daily_summary = df.groupby('Date').agg({
        'Temp': ['mean', 'max', 'min'],
        'Humidity': ['mean', 'max', 'min'],
        'Wind_Speed': ['mean', 'max', 'min'],
        'Condition': lambda x: x.mode()[0]  # Dominant weather condition
    })
    return daily_summary


def check_threshold(city, temp, threshold=35, count=2):
    # Initialize temp_history dictionary if it doesn't exist
    if not hasattr(check_threshold, 'temp_history'):
        check_threshold.temp_history = {}

    # Initialize the city's temperature history list if it doesn't exist
    if city not in check_threshold.temp_history:
        check_threshold.temp_history[city] = []

    temp_history = check_threshold.temp_history[city]
    temp_history.append(temp)

    # Print the city and its temperature history for debugging
    print(f"Checking threshold for {city} - Temp History: {temp_history}")

    # Keep track of last 'count' temperatures
    if len(temp_history) > count:
        temp_history.pop(0)

    # Check threshold
    if len(temp_history) == count and all(t > threshold for t in temp_history):
        print(f"Alert triggered for {city}!")
        return f"Alert! Temperature in {city} exceeded {threshold}°C for {count} consecutive updates."

    # Print for debugging when the threshold is not breached
    print(f"No alert for {city}. Latest temp: {temp}")
    return None


def plot_temperature(cities):
    temps = []
    for city in cities:
        weather_data = get_weather_data(city)
        if weather_data:
            parsed_data = parse_weather_data(weather_data)
            temps.append(parsed_data[0])  # Append only the temperature
        else:
            temps.append(None)  # Append None if data not available

    # Filter out None values for plotting
    filtered_cities = [city for city, temp in zip(cities, temps) if temp is not None]
    filtered_temps = [temp for temp in temps if temp is not None]

    if not filtered_temps:  # If all temperatures are None
        print("No valid temperature data available for plotting.")
        return

    # Create bar plot for temperatures
    bars = plt.bar(filtered_cities, filtered_temps, color='blue', alpha=0.7)

    # Adding temperature labels on each bar
    for bar, temp in zip(bars, filtered_temps):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{temp:.2f}°C', ha='center', va='bottom')

    plt.xlabel('Cities')
    plt.ylabel('Temperature (°C)')
    plt.title('Current Temperatures in Cities')
    plt.xticks(rotation=45)
    plt.ylim(0, max(filtered_temps) + 5)  # Set y-axis limit

    # Adding a legend for the color
    plt.legend(['Temperature (°C)'], loc='upper left')

    plt.show()

def main():
    cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
    data_collection_duration = 60  # Collect data for 1 minute
    end_time = time.time() + data_collection_duration

    while time.time() < end_time:
        for city in cities:
            weather_data = get_weather_data(city)
            if weather_data:
                parsed_data = parse_weather_data(weather_data)
                store_weather_data(city, *parsed_data)
                alert = check_threshold(city, parsed_data[0], threshold=25)
                if alert:
                    print(alert)
        time.sleep(10)  # Reduce interval to 10 seconds for quicker testing

    # After the data collection period, calculate and visualize the daily summary
    daily_summary = calculate_daily_summary()
    print(daily_summary)
    plot_temperature(cities)

if __name__ == "__main__":
    main()
