import requests
from dotenv import load_dotenv
import os
load_dotenv()
API = os.getenv('EXCHANGE_RATE')
url = f"https://v6.exchangerate-api.com/v6/{API}/latest/KES"
response = requests.get(url)
print("Status code:", response.status_code)
if response.status_code == 200:
    data = response.json()
    currency_rates = data['conversion_rates']
    usd_rate = round(currency_rates['USD'], 4)
    cad_rate = round(currency_rates['CAD'], 4)
    eur_rate = round(currency_rates['EUR'], 4)
    tzs_rate = round(currency_rates['TZS'], 2)
    egp_rate = round(currency_rates['EGP'], 4)
    print("Exchange Rates:")
    print("USD:", usd_rate)
    print("CAD:", cad_rate)
    print("EUR:", eur_rate)
    print("TZS:", tzs_rate)
    print("EGP:", egp_rate)
else:
    print("Failed to retrieve exchange rates. Status code:", response.status_code)