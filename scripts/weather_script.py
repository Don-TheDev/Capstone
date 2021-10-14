import json
import requests

city_name = "Salt Lake City"
api_key = "e2a7eb8fb47f6546ba6b8d79c8e4d9cd"

api_call = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
response = requests.get(api_call)
response_json = response.json()
description = response_json["weather"][0]["description"]
temp = response_json["main"]["temp"]
temp_min = response_json["main"]["temp_min"]
temp_max = response_json["main"]["temp_max"]
humidity = response_json["main"]["humidity"]
wind_speed = response_json["wind"]["speed"]

print (description)
