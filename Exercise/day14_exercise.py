import anthropic
import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API"))

#Setting up weather API key 
def get_weather():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Kericho&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

def run_chatbot():
     Question=input("What can I help you with today: ").strip()
     system_prompt="""You are a tea estate field supervisor assistant. You will provide information about the weather in Kericho, Kenya.
   Your rules: 
  - You will call get_weather() tool when the question involves conditions and harvesting. Only focus on the weather in Kericho, Kenya.
  - You will use the weather result to give practical recomendation in plain language.
  - Only answer questions about the weather in Kericho, Kenya.
  - If a question is outside your scope, say: "Please call our office on 0712 345 678 for that.
  - Always be polite and professional. End with "Asante kwa Kuwasiliana.

  Examples:
  User: "Is today a good day for harvesting?"
  Answer:"Yes, today is a good day for harvesting. There is no rain in the next 6 hours, temperature betweeen 15-25 degrees Celcius, and low humidity. You can proceed with harvesting."

  User: "Is today a good day for harvesting?"
  Answer: "No, today is a bad day for harvesting. There is an active rain and temperature is above 28 degree Celcius. "
  """

     try: 
        data = get_weather()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        messages= client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=512,
                system=system_prompt,
                messages=[{"role":"user", "content":f"User question: '{Question}'. Current weather data in Kericho: Temp {temp}°C, Condition: {description}, Humidity: {humidity}%."}]
               )
        print("===Assistant Response===")
        print(messages.content[0])
            
        
     except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")

     except anthropic.APIConnectionError:
            print("No internet connection. Check your connection and try again.")
     except anthropic.AuthenticationError:
         print("Api key is wrong or expired. Check your .env file.")
     except anthropic.RateLimitError:
            print("Too many requests. Wait 60 seconds and try again.")
         
if __name__ == "__main__":
    run_chatbot()