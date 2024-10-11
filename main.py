# pip install openmeteo-requests
# pip install requests-cache retry-requests numpy pandas

import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 36.6519,
	"longitude": 50.749,
	"current": ["temperature_2m", "rain", "showers", "weather_code"],
	"minutely_15": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "rain", "freezing_level_height", "weather_code"],
	"hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "snow_depth", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_80m", "wind_speed_120m", "wind_speed_180m", "wind_direction_10m", "wind_direction_80m", "wind_direction_120m", "wind_direction_180m", "wind_gusts_10m", "temperature_80m", "temperature_120m", "temperature_180m", "soil_temperature_0cm", "soil_temperature_6cm", "soil_temperature_18cm", "soil_temperature_54cm", "soil_moisture_0_to_1cm", "soil_moisture_1_to_3cm", "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm", "soil_moisture_27_to_81cm", "uv_index", "uv_index_clear_sky", "is_day", "sunshine_duration", "freezing_level_height", "boundary_layer_height"],
	"daily": ["sunrise", "sunset"],
	"timezone": "auto",
	"forecast_days": 16
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_rain = current.Variables(1).Value()
current_showers = current.Variables(2).Value()
current_weather_code = current.Variables(3).Value()

print(f"Current time {current.Time()}")
print(f"Current temperature_2m {current_temperature_2m}")
print(f"Current rain {current_rain}")
print(f"Current showers {current_showers}")
print(f"Current weather_code {current_weather_code}")

# Process minutely_15 data. The order of variables needs to be the same as requested.
minutely_15 = response.Minutely15()
minutely_15_temperature_2m = minutely_15.Variables(0).ValuesAsNumpy()
minutely_15_relative_humidity_2m = minutely_15.Variables(1).ValuesAsNumpy()
minutely_15_apparent_temperature = minutely_15.Variables(2).ValuesAsNumpy()
minutely_15_rain = minutely_15.Variables(3).ValuesAsNumpy()
minutely_15_freezing_level_height = minutely_15.Variables(4).ValuesAsNumpy()
minutely_15_weather_code = minutely_15.Variables(5).ValuesAsNumpy()

minutely_15_data = {"date": pd.date_range(
	start = pd.to_datetime(minutely_15.Time(), unit = "s", utc = True),
	end = pd.to_datetime(minutely_15.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = minutely_15.Interval()),
	inclusive = "left"
)}
minutely_15_data["temperature_2m"] = minutely_15_temperature_2m
minutely_15_data["relative_humidity_2m"] = minutely_15_relative_humidity_2m
minutely_15_data["apparent_temperature"] = minutely_15_apparent_temperature
minutely_15_data["rain"] = minutely_15_rain
minutely_15_data["freezing_level_height"] = minutely_15_freezing_level_height
minutely_15_data["weather_code"] = minutely_15_weather_code

minutely_15_dataframe = pd.DataFrame(data = minutely_15_data)
print(minutely_15_dataframe)

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(3).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()
hourly_rain = hourly.Variables(5).ValuesAsNumpy()
hourly_showers = hourly.Variables(6).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(7).ValuesAsNumpy()
hourly_snow_depth = hourly.Variables(8).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(9).ValuesAsNumpy()
hourly_cloud_cover_low = hourly.Variables(10).ValuesAsNumpy()
hourly_cloud_cover_mid = hourly.Variables(11).ValuesAsNumpy()
hourly_cloud_cover_high = hourly.Variables(12).ValuesAsNumpy()
hourly_visibility = hourly.Variables(13).ValuesAsNumpy()
hourly_et0_fao_evapotranspiration = hourly.Variables(14).ValuesAsNumpy()
hourly_vapour_pressure_deficit = hourly.Variables(15).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(16).ValuesAsNumpy()
hourly_wind_speed_80m = hourly.Variables(17).ValuesAsNumpy()
hourly_wind_speed_120m = hourly.Variables(18).ValuesAsNumpy()
hourly_wind_speed_180m = hourly.Variables(19).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(20).ValuesAsNumpy()
hourly_wind_direction_80m = hourly.Variables(21).ValuesAsNumpy()
hourly_wind_direction_120m = hourly.Variables(22).ValuesAsNumpy()
hourly_wind_direction_180m = hourly.Variables(23).ValuesAsNumpy()
hourly_wind_gusts_10m = hourly.Variables(24).ValuesAsNumpy()
hourly_temperature_80m = hourly.Variables(25).ValuesAsNumpy()
hourly_temperature_120m = hourly.Variables(26).ValuesAsNumpy()
hourly_temperature_180m = hourly.Variables(27).ValuesAsNumpy()
hourly_soil_temperature_0cm = hourly.Variables(28).ValuesAsNumpy()
hourly_soil_temperature_6cm = hourly.Variables(29).ValuesAsNumpy()
hourly_soil_temperature_18cm = hourly.Variables(30).ValuesAsNumpy()
hourly_soil_temperature_54cm = hourly.Variables(31).ValuesAsNumpy()
hourly_soil_moisture_0_to_1cm = hourly.Variables(32).ValuesAsNumpy()
hourly_soil_moisture_1_to_3cm = hourly.Variables(33).ValuesAsNumpy()
hourly_soil_moisture_3_to_9cm = hourly.Variables(34).ValuesAsNumpy()
hourly_soil_moisture_9_to_27cm = hourly.Variables(35).ValuesAsNumpy()
hourly_soil_moisture_27_to_81cm = hourly.Variables(36).ValuesAsNumpy()
hourly_uv_index = hourly.Variables(37).ValuesAsNumpy()
hourly_uv_index_clear_sky = hourly.Variables(38).ValuesAsNumpy()
hourly_is_day = hourly.Variables(39).ValuesAsNumpy()
hourly_sunshine_duration = hourly.Variables(40).ValuesAsNumpy()
hourly_freezing_level_height = hourly.Variables(41).ValuesAsNumpy()
hourly_boundary_layer_height = hourly.Variables(42).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["apparent_temperature"] = hourly_apparent_temperature
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["precipitation"] = hourly_precipitation
hourly_data["rain"] = hourly_rain
hourly_data["showers"] = hourly_showers
hourly_data["snowfall"] = hourly_snowfall
hourly_data["snow_depth"] = hourly_snow_depth
hourly_data["cloud_cover"] = hourly_cloud_cover
hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
hourly_data["visibility"] = hourly_visibility
hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration
hourly_data["vapour_pressure_deficit"] = hourly_vapour_pressure_deficit
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
hourly_data["wind_speed_120m"] = hourly_wind_speed_120m
hourly_data["wind_speed_180m"] = hourly_wind_speed_180m
hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
hourly_data["wind_direction_80m"] = hourly_wind_direction_80m
hourly_data["wind_direction_120m"] = hourly_wind_direction_120m
hourly_data["wind_direction_180m"] = hourly_wind_direction_180m
hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
hourly_data["temperature_80m"] = hourly_temperature_80m
hourly_data["temperature_120m"] = hourly_temperature_120m
hourly_data["temperature_180m"] = hourly_temperature_180m
hourly_data["soil_temperature_0cm"] = hourly_soil_temperature_0cm
hourly_data["soil_temperature_6cm"] = hourly_soil_temperature_6cm
hourly_data["soil_temperature_18cm"] = hourly_soil_temperature_18cm
hourly_data["soil_temperature_54cm"] = hourly_soil_temperature_54cm
hourly_data["soil_moisture_0_to_1cm"] = hourly_soil_moisture_0_to_1cm
hourly_data["soil_moisture_1_to_3cm"] = hourly_soil_moisture_1_to_3cm
hourly_data["soil_moisture_3_to_9cm"] = hourly_soil_moisture_3_to_9cm
hourly_data["soil_moisture_9_to_27cm"] = hourly_soil_moisture_9_to_27cm
hourly_data["soil_moisture_27_to_81cm"] = hourly_soil_moisture_27_to_81cm
hourly_data["uv_index"] = hourly_uv_index
hourly_data["uv_index_clear_sky"] = hourly_uv_index_clear_sky
hourly_data["is_day"] = hourly_is_day
hourly_data["sunshine_duration"] = hourly_sunshine_duration
hourly_data["freezing_level_height"] = hourly_freezing_level_height
hourly_data["boundary_layer_height"] = hourly_boundary_layer_height

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_sunrise = daily.Variables(0).ValuesAsNumpy()
daily_sunset = daily.Variables(1).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}
daily_data["sunrise"] = daily_sunrise
daily_data["sunset"] = daily_sunset

daily_dataframe = pd.DataFrame(data = daily_data)
print(daily_dataframe)
