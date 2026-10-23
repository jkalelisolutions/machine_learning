"""
This project fetches country info and its exchange rate against major currencies.

To Setup:
1. Run pip install requests python-dotenv
2. Create a new file .env with: EXCHANGE-RATES=Your_API_Key and RESTCOUNTRIES=Your_API_Key
3. Get free API Keys from rescountries.com and exchangerate-api.com

To Run:
python day3_exercise.py
"""

import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

def load_data():
    if not os.path.exists("data.json"):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            print("data.json file not found.")
            
            

# A def function used to fetch the specified base currency and convert it into differentcurrencies. 
def get_exchange_rates(base_currency):
    api_key = os.getenv("EXCHANGE_RATE")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    response = requests.get(url)
    return response

# A def function used to fetch countries info using restcountries api
def country_info(country_code):
    api_key = os.getenv("REST_COUNTRIES_API")
    if not api_key:
        raise RuntimeError("REST_COUNTRIES_API is not set")

    url = "https://api.restcountries.com/countries/v5"
    response = requests.get(
        url,
        params={"q": country_code},
        headers={"Authorization": api_key},
        timeout=15,
    )
    response.raise_for_status()
    return response

def run_tool():
    data = load_data()

    submit = [] 
    print("="*50)
    print("Welcome to know your country!")
    print("="*50)
    
    country_code = input("\nEnter the country code (e.g., KE for Kenya): ").strip()
    base_currency = input("Enter the base currency (e.g., KES for Kenyan Shilling): ").strip().upper()

    if not country_code:
        print("No country code entered. Exiting.")
        return
    if not base_currency:
        print("No base currency entered. Exiting.")
        return
    
    #Displaying country info based on the searched country code
    response = country_info(country_code)
    if response.status_code == 200:
        data = response.json()
        country = data["data"]["objects"][0]  # Assuming the response is a list and we want the first country
        name = country["names"]["common"]
        capital = country["capitals"][0]
        population = country["population"]
        currencies = list(country["currencies"])
        result = {"Country": name,"Capital": capital,"Population": population,"Currencies":currencies}
        print(f"\nCountry: {name}\nCapital: {capital}\nPopulation: {population}\nCurrencies: {currencies}")
        submit.append(result)

    #Converting the base currency 
    response = get_exchange_rates(base_currency)
    if response.status_code == 200:
        data = response.json()
        currency_rates = data['conversion_rates']
        kes_rate = round(currency_rates['KES'],2)
        usd_rate = round(currency_rates['USD'], 4)
        cad_rate = round(currency_rates['CAD'], 4)
        eur_rate = round(currency_rates['EUR'], 4)
        tzs_rate = round(currency_rates['TZS'], 2)
        egp_rate = round(currency_rates['EGP'], 4)
        res = {"KES": kes_rate, "USD": usd_rate, "CAD": cad_rate, "EUR": eur_rate,"TZS": tzs_rate, "EGP": egp_rate}
        submit.append(res)
        print("\nExchange Rates:")
        print(f"\nExchange Rates for {base_currency}:\nKES: {kes_rate} \nUSD: {usd_rate}\nCAD: {cad_rate}\nEUR: {eur_rate}\nTZS: {tzs_rate}\nEGP: {egp_rate}")
    else:
        print(f"Failed to fetch exchange rates. Status code: {response.status_code}")

    #Saving data to a JSON file  
    try:
        with open("data.json","w") as f:
            json.dump(submit,f,indent=4)
            print(f"Data saved succesfully.")
    except json.JSONDecodeError:
        print("Data not saved. Please try again")
    
run_tool()
