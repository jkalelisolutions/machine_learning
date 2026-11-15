import requests
from bs4 import BeautifulSoup
import csv
import time

def fetch_page(url, retries=3):
     for attempt in range(retries):
          try:
              response= requests.get(url, timeout=10)
              response.raise_for_status()
              return response
          except requests.RequestException as e:
               print(f"Attempt {attempt+1} failed: {e}")
               time.sleep(2)
          return None 

url = "https://books.toscrape.com/"
response= fetch_page(url)



soup = BeautifulSoup(response.text,"html.parser")
     
print("Status:", response.status_code)
print("Page size:", len(response.text), "characters\n")

#find all book articles on the page
books = soup.find_all("article", class_="product_pod")
print(f"\nFound{len(books)} based on this page.")

for book in books[:5]: #first 5 only
    title = book.find("h3").find("a")["title"]
    price= book.find("p", class_="price_color").text
    print(f"{title}:{price}")

books_data=[]
for book in books:
     title = book.find("h3").find("a")["title"]
     price= book.find("p", class_="price_color").text
     rating = book.find("p", class_="star-rating")["class"][1]
     books_data.append({"title":title,"price":price,"rating":rating})

with open("day22.csv", "w", newline="", encoding="utf-8") as f:
     writer= csv.DictWriter(f, fieldnames=["title", "price", "rating"])
     writer.writeheader()
     writer.writerows(books_data)
     print(f"Saved {len(books_data)} books to day22.csv")