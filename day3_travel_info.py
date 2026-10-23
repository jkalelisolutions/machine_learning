import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def get_country_info(country_code):
   api = os.getenv("AUTHORIZATION")
   if not api:
       raise RuntimeError("Failing to get RESTCOUNTRIES API. Please check and try again...")
   url = f"https://api.restcountries.com/countries/v5"
   response = requests.get(
       url,
       params={"q":country_code},
       headers={"Authorization":api},
       timeout=15
   )
   return response
def run_tool():
    print("Travel Weather Tool")
    print("-------------------")
    city = input("Enter a city name: ").strip()

    if not city:
        print("No city entered. Exiting.")
        return

    print(f"\nFetching data for {city}...")

    weather_data = get_weather(city)

    if not weather_data:
        print(f"Could not find weather data for '{city}'. Check the city name and try again.")
        return

    country_code = weather_data["sys"]["country"]
    country_data = get_country_info(country_code).json()

    print(f"\n=== {city.title()}, {country_code} ===")
    print(f"Temperature : {weather_data['main']['temp']}C")
    print(f"Condition   : {weather_data['weather'][0]['description'].title()}")
    print(f"Humidity    : {weather_data['main']['humidity']}%")
    print(f"Wind        : {weather_data['wind']['speed']} m/s")

    if country_data:
        country = country_data["data"]["objects"][0]
        population = country["population"]
        region = country["region"]
        currencies = list(country["currencies"])
        print(f"\n=== Country Info ===")
        print(f"Region      : {region}")
        print(f"Population  : {population:,}")
        print(f"Currency    : {currencies}")


run_tool()