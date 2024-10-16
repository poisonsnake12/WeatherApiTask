import datetime as dt
import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "ff7baa6fa20bb28fdfb60f35cf15b121"

#defining function to convert kelvin to celcius and fahrenheit
def kelvin_to_celsius_farehnheit(kelvin):
    celsius = kelvin -273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit

#creating list of Cities from user input
cities = []
for i in range(5):
    city = input(f"Enter name of city {i+1}:")
    cities.append(city)

#intialising variables to keep track of average and coldest temperature
total_temp_celcius = 0 #used for average temp calculation
coldest_city = None
coldest_temp = float('inf')

#looping through array to fetch data for each city
for CITY in cities:

    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY #building url string with query for specific city

    response = requests.get(url).json() 

    #check if request was successful
    if response.get('cod') != 200:
            print(f"Could not retrieve data for {CITY}. Error: {response.get('message')}")
            continue

    #extracting weather data
    temp_kelvin = response['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_farehnheit(temp_kelvin)
    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_farehnheit(feels_like_kelvin)
    wind_speed = response['wind']['speed']
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']
    sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone']) #adjusting for timezone difference
    sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone']) #adjusting for timezone difference
    
    #adding up total temp for average
    total_temp_celcius += temp_celsius

    #checking for coldest city
    if temp_celsius < coldest_temp:
        coldest_temp = temp_celsius
        coldest_city = CITY

    #printing weather data
    print(f"Temperature in {CITY}: {temp_celsius:.2f}°C or {temp_fahrenheit:.2f}°F")
    print(f"Temperature in {CITY} feels like: {feels_like_celsius:.2f}°C or {feels_like_fahrenheit:.2f}°F")
    print(f"Humidity in {CITY}: {humidity}%")
    print(f"Wind speed in {CITY}: {wind_speed}m/s")
    print(f"General weather in {CITY}: {description}")
    print(f"Sun rises in {CITY} at {sunrise_time} local time")
    print(f"Sun sets in {CITY} at {sunset_time} local time\n")

average_temp_celsius = total_temp_celcius / 5
print(f"\nAverage temperature between the five cities is {average_temp_celsius:.2f}°C")
print(f"The coldest city of the five is {coldest_city} with a temperature of {coldest_temp:.2f}°C") 
# print(response)
