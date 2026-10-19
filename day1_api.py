import requests
import os
from dotenv import load_dotenv
load_dotenv()

url = "https://api.restcountries.com/countries/v5?q=kenya&pretty=3"
headers = {"Authorization": f"Bearer {os.getenv('AUTHORIZATION')}"}

response = requests.get(url, headers=headers, timeout=15)
print("Status code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    countries = data["data"]["objects"][0]  # Assuming the response is a list and we want the first country
    name = countries["names"]["common"]
    capital = countries["capitals"][0]
    population = countries["population"]
    currencies = list(countries["currencies"])
    print(f"Country: {name}")
    print(f"Capital: {capital}")
    print(f"Population: {population}")
    print(f"Currencies: {currencies}")
else:
    print("Failed to retrieve data:", response.text)