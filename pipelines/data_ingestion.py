import requests
import os
import pandas as pd
from prefect import flow, task
#from prefect.tasks import task_input_hash
#from datetime import timedelta
from pathlib import Path
from prefect_aws import AwsCredentials, S3Bucket


# API endpoints and keys 
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
AIR_QUALITY_API_URL = "http://api.openweathermap.org/data/2.5/air_pollution"


# List of cities to analyze

CITIES = [

    {"name": "Douala", "lat": 4.0483, "lon": 9.7043}, 
    {"name": "Yaoundé", "lat": 3.8667, "lon": 11.5167}, 
    {"name": "Bafoussam", "lat": 5.4737, "lon": 10.4179}, 
    {"name": "Bamenda", "lat": 5.9527, "lon": 10.1582}, 
    {"name": "Maroua", "lat": 10.591, "lon": 14.3159}, 
    {"name": "Ngaoundéré", "lat": 7.3167, "lon": 13.5833}, 
    {"name": "Buea", "lat": 4.1527, "lon": 9.241}, 
    {"name": "Ebolowa", "lat": 2.9, "lon": 11.15}, 
    {"name": "Garoua", "lat": 9.3, "lon": 13.4}, 
    {"name": "Bertoua", "lat": 4.5833, "lon": 13.6833}, 

]


@task(#cache_key_fn=task_input_hash,
       #cache_expiration=timedelta(hours=1)
       )
def extract_weather_data(city): 

    """Extract weather data from OpenWeatherMap API"""

    params = {
        "lat": city["lat"], 
        "lon": city["lon"], 
        "appid": WEATHER_API_KEY, 
        "units": "metric"
    }

    response = requests.get(WEATHER_API_URL, params=params)

    if response.status_code == 200: 

        data = response.json()
    
        weather_data = {
            "city" : city["name"], 
            "temperature": data["main"]["temp"], 
            "feels_like": data["main"]["feels_like"], 
            "temp_min": data["main"]["temp_min"], 
            "temp_max": data["main"]["temp_max"], 
            "pressure": data["main"]["pressure"], 
            "humidity": data["main"]["humidity"], 
            "wind_speed": data["wind"]["speed"]
    }
        
        return weather_data
    else: 
        print(f"Failed to fetch data: {response.status_code}, {response.text}")
        return None
    

weather_data = extract_weather_data(CITIES[8])

if weather_data: 
    print(extract_weather_data(CITIES[8]))

@task(#cache_key_fn=task_input_hash, 
      #cache_expiration=timedelta(hours=1)
      )
def extract_air_quality_data(city): 
    """ Extract air quality data from OpenWeatherMap API."""
    params = {
        "lat": city["lat"], 
        "lon": city["lon"], 
        "appid": WEATHER_API_KEY
    }

    response = requests.get(AIR_QUALITY_API_URL, params=params)

    if response.status_code == 200: 

        data = response.json()

        air_quality_data = {
            "city": city["name"], 
            "aqi": data["list"][0]["main"]["aqi"], 
            "co": data["list"][0]["components"]["co"], 
            "no2": data["list"][0]["components"]["no2"], 
            "o3": data["list"][0]["components"]["o3"], 
            "pm2_5": data["list"][0]["components"]["pm2_5"]
        }

        return air_quality_data
    
    else: 
        print(f"Failed to fetch data: {response.status_code}, {response.text}")


air_quality_data = extract_air_quality_data(CITIES[8])

if air_quality_data: 
    print(extract_air_quality_data(CITIES[8]))



@task   
def transform_data(weather_data, air_quality_data): 
    """ Transform and combine weather and air quality data."""

    weather_df = pd.DataFrame(weather_data)
    air_quality_df = pd.DataFrame(air_quality_data)

    combined_df = pd.merge(weather_df, air_quality_df, on = "city")

    #Add air quality category based on AQI

    combined_df["air_quality_category"] = pd.cut(
        combined_df["aqi"], 
        bins=[-1, 50, 100, 150, 200, 300, 500], 
        labels = ["Good", "Moderate", "Unhealthy for Sensitive Groups", "Unhealthy", "Very Unhealthy", "Hazardous"]
    )

    combined_df.to_csv('../data/combined_df.csv', index = False)

    return combined_df

@task
def save_to_s3(): 
    """ Save the final data into an S3 bucket"""

    # AWS credential...
    file_path = Path("../data/combined_df.csv")
    aws_credentials_block = AwsCredentials.load("my-aws-creds")
    s3_bucket = S3Bucket(
        bucket_name="zeguild-bucket",
        credentials=aws_credentials_block
    )
    s3_bucket_path = s3_bucket.upload_from_path(file_path)

    return s3_bucket_path




@flow(name="City Weather and Air Quality ETL")
def city_weather_air_quality_etl(): 
    weather_data = []
    air_quality_data = []

    for city in CITIES: 
        weather_data.append(extract_weather_data(city))
        air_quality_data.append(extract_air_quality_data(city))

    combined_data = transform_data(weather_data, air_quality_data)
    save_to_s3()

    return combined_data



if __name__ == "__main__": 
    city_weather_air_quality_etl()