# Weather-Monitoring-system
 Developed a real-time data processing system to monitor weather conditions and provide  summarized insights using rollups and aggregates. The system will utilize data from the  OpenWeatherMap API
# Table of Contents
Features

Installation

Technologies Used

Architecture

Dependencies

Design Choices

Process

# Features
1.Real-time weather monitoring for major cities in India.
2.Daily weather summaries with aggregates like average temperature, humidity, etc.
3.Alert system for exceeding temperature thresholds.
4.Data visualization using Matplotlib.

# Installation
1.Prerequisites
2.Python 3.x: Ensure you have Python 3 installed on your system. You can download it from python.org.
3.OpenWeatherMap API Key: Sign up at OpenWeatherMap and obtain your free API key

# Technologies Used
Python
Requests (for API calls)
Pandas (for data manipulation)
Matplotlib (for visualization)

# Architecture
The Weather Monitoring Application retrieves real-time weather data from the OpenWeatherMap API, processes and parses the information (temperature, humidity, wind speed), and stores it in a CSV file. It calculates daily summaries, including average and maximum temperatures, and checks against user-defined thresholds to trigger alerts. Visualization is done using Matplotlib, displaying current temperatures in a bar chart format. The console serves as the user interface, providing real-time updates and alerts. The modular design allows for easy enhancements and integration of additional weather parameters in the future.

# Design Choices
1.Data Retrieval: The application uses the OpenWeatherMap API for fetching real-time weather data.
2.Data Processing: Weather data is processed and stored in a CSV file for further analysis. The application computes daily summaries including average, maximum, and minimum temperatures.
3.Visualizations: Matplotlib is used for generating bar charts to visualize current temperatures.
Threshold Alerting: A simple threshold mechanism is implemented to alert users when temperatures exceed specified limits.

# Dependencies
1.requests: For making HTTP requests to the OpenWeatherMap API.

2.pandas: For data manipulation and analysis, especially for calculating daily summaries.

3.matplotlib: For data visualization.

# Process

1. Setup API Connection: Sign up for the OpenWeatherMap API to obtain an API key for accessing weather data.
2. Define Weather Data Retrieval: Implement a function to make API calls for specified cities and retrieve real-time weather data in metric units.
3. Parse Weather Data: Extract relevant information (temperature, humidity, wind speed, and weather condition) from the API response.
4. Store Data: Write the parsed weather data into a CSV file, creating a header if the file doesn't exist, and append new data for each retrieval.
5. Check Temperature Thresholds: Maintain a history of temperature readings for each city and check if the latest readings breach user-defined thresholds to trigger alerts.
6. Calculate Daily Summaries: At regular intervals, aggregate the stored data to compute daily summaries, including average, maximum, and minimum temperatures, and determine the dominant weather condition.
7. Visualize Data: Use Matplotlib to create bar charts that visualize current temperatures for each city, displaying values above each bar for clarity.
8. Run the System: Implement a main function that continuously collects weather data for a specified duration, calling the retrieval and processing functions at set intervals.
9. Display Results: After the data collection period, print daily summaries and display the temperature visualization to the user.




