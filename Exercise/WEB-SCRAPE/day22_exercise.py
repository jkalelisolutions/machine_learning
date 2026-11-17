import requests
from bs4 import BeautifulSoup
import csv
import time

def fetch_url(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Attempt {attempt+1} failed {e}")
            time.sleep(2)
        return None

url = "https://quotes.toscrape.com/"
response= fetch_url(url)

if response is None:
    print("Could not fetch the page")
else:
    soup= BeautifulSoup(response.text, "html.parser")
    print("Status:" ,response.status_code)
    print("Scraped:", len(response.text), "characters")

    quotes = soup.find_all("div", class_="quote")
    print(f"Found {len(quotes)} on this page")

    scrape= []
    for quote in quotes:
         text= quote.find("span", class_="text").text
         author= quote.find("span").find("small")
         link= quote.find("a")
         scrape.append({"Text":text,"Author":author,"Link":link})

         print(f"{text}:{author}\n {link}")

    with open("quotes.csv", "w") as f:
      writer= csv.DictWriter(f,fieldnames=['Text', 'Author', 'Link'])
      writer.writeheader()
      writer.writerows(scrape)

      print(f"Saved {len(scrape)} quotes to quotes.csv")

    