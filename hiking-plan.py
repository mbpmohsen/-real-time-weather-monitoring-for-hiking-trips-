import json
import pandas as pd
import requests
import concurrent.futures
import matplotlib.pyplot as plt
from tqdm import tqdm

with open('./adjusted_gpx_to_json.json', 'r') as file:
    route_data = json.load(file)

segments = route_data['tracks'][0]['segments'][0]

total_items = len(segments)

route_df = pd.DataFrame(segments)


def get_weather(lat, lon, timestamp):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "minutely_15": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "rain", "freezing_level_height", "weather_code"],
        "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "snow_depth", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", "wind_speed_10m", "wind_speed_80m", "wind_speed_120m", "wind_speed_180m", "wind_direction_10m", "wind_direction_80m", "wind_direction_120m", "wind_direction_180m", "wind_gusts_10m"],
        "daily": ["sunrise", "sunset"],
        "start": timestamp,
        "end": timestamp,
        "timezone": "auto"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        print(f"Error Fetching Data for {lat}, {lon}: {e}")
    return None


def fetch_weather_data_parallel(index, row):
    lat = row['latitude']
    lon = row['longitude']
    timestamp = row['time']  # Assuming your timestamp format is compatible with Open Meteo API
    return get_weather(lat, lon, timestamp)


weather_data = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers based on your system
    futures = [executor.submit(fetch_weather_data_parallel, index, row) for index, row in route_df.iterrows()]

    for future in tqdm(concurrent.futures.as_completed(futures), total=total_items, desc="Fetching Weather Data"):
        result = future.result()
        if result:
            weather_data.append(result)

output_file = 'parallel_route_weather_data.json'
with open(output_file, 'w') as f:
    json.dump(weather_data, f)

print(f"Weather data saved to {output_file}")

with open('parallel_route_weather_data.json', 'r') as f:
    weather_data = json.load(f)

time_list = []
temperature_list = []
rain_list = []
wind_speed_list = []
sunrise_list = []
sunset_list = []

for entry in weather_data:
    if 'hourly' in entry and 'time' in entry['hourly']:
        times = entry['hourly']['time']  # List of times

        temperatures = entry['hourly'].get('temperature_2m', [None] * len(times))  # List of temperatures

        rain = entry['hourly'].get('precipitation', [None] * len(times))  # List of rain data

        wind_speed = entry['hourly'].get('wind_speed_10m', [None] * len(times))  # List of wind speeds

        time_list.extend(times)
        temperature_list.extend(temperatures)
        rain_list.extend(rain)
        wind_speed_list.extend(wind_speed)

    if 'daily' in entry:
        sunrise = entry['daily'].get('sunrise', [None] * len(times))
        sunset = entry['daily'].get('sunset', [None] * len(times))

        sunrise_list.extend([sunrise[0]] * len(times))
        sunset_list.extend([sunset[0]] * len(times))

df = pd.DataFrame({
    'time': pd.to_datetime(time_list),
    'temperature_2m': temperature_list,
    'rain': rain_list,
    'wind_speed_10m': wind_speed_list,
    'sunrise': sunrise_list if sunrise_list else None,
    'sunset': sunset_list if sunset_list else None
})

df.sort_values(by='time', inplace=True)

# --- Plot Temperature ---
plt.figure(figsize=(10, 6))
plt.plot(df['time'], df['temperature_2m'], label='Temperature (°C)', color='tab:red')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.title('Temperature along the hiking route')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Plot Rain ---
plt.figure(figsize=(10, 6))
plt.plot(df['time'], df['rain'], label='Rain (mm)', color='tab:blue')
plt.xlabel('Time')
plt.ylabel('Rain (mm)')
plt.title('Rain along the hiking route')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Plot Wind Speed ---
plt.figure(figsize=(10, 6))
plt.plot(df['time'], df['wind_speed_10m'], label='Wind Speed (m/s)', color='tab:green')
plt.xlabel('Time')
plt.ylabel('Wind Speed (m/s)')
plt.title('Wind Speed along the hiking route')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Plot Sunrise and Sunset (if available) ---
plt.figure(figsize=(10, 6))
plt.plot(df['time'], df['sunrise'], label='Sunrise', color='tab:orange')
plt.plot(df['time'], df['sunset'], label='Sunset', color='tab:purple')
plt.xlabel('Time')
plt.ylabel('Time')
plt.title('Sunrise and Sunset times along the hiking route')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
