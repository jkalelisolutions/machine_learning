import requests
url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)
print("Status code:", response.status_code)
print(response.json())