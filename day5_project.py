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
    usd_rate = currency_rates['USD']
    cad_rate = currency_rates['CAD']
    eur_rate = currency_rates['EUR']
    tzs_rate = currency_rates['TZS']
    egp_rate = currency_rates['EGP']
    print("Exchange Rates:")
    print("USD:", usd_rate)
    print("CAD:", cad_rate)
    print("EUR:", eur_rate)
    print("TZS:", tzs_rate)
    print("EGP:", egp_rate)
else:
    print("Failed to retrieve exchange rates. Status code:", response.status_code)