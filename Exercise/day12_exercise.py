import anthropic
import os
import json
from dotenv import load_dotenv
load_dotenv()
client=anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

system_prompt="""An AI property agent assistant, based in Nairobi
Your rules:
- Be brief and professional when answering messages
-You only focus on listed properties in Nairobi
-Your answers should be based on this scope: property_type, bedrooms, budget_KES, rental or resale.
- Questions that falls out of the scope, your response is: "Please call our office 0723744820 for that. Thank you.
-Be polite and alsways end with: "Asante kwa kuwasiliana."

Example:
Question: "I am looking for 3-bedroom house in Kileleshwa, budget around KES 80,0000 per month."
Answer: "Yes, we have a listed 3-bedroom apartment based in Kileleshwa."

After giving your answer you list it based on the data retrieved in JSON file.
The format is: {"property_type":"apartment", "bedrooms":3, "budget_kes":80000, "status":"rental" or "resale"}
No explanation. No markdown. Just the JSON.
"""
messages=[]
try:
    while True:
        question=input("Ask me about houses: ")
        if question.lower()=="exit":
            break
        messages.append({"role":"user","content":question})
        response=client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=512,
            system=system_prompt,
            messages=messages
        )
        reply= response.content[0]
        messages.append({"role":"assistant","content":reply})
        print(f"Assistant: {reply}")
except anthropic.AuthenticationError:
    print("API Key is wrong or expired. Check you .env file.")
except anthropic.APIConnectionError:
    print("No internet connection. Check your connection and try again.")
except anthropic.RateLimitError:
    print("Too many request. Wait 60 seconds and try again.")
