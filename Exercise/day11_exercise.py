"""A customer assistant chatbot used to reply members of a Sacco."""

import os
from dotenv import load_dotenv
import anthropic
load_dotenv()
client= anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API"))

#Layout rules that the AI will strictly follow to avoid misguiding clients
system_prompt="""You are a customer service assistant for a Matatu Sacco.
Your Rules:
-Only answer questions about balance, meeting, current membership fees
-Finance is in KES
-If question is out of scope, say:"Please call our offices on 0711 245 750 for that."
-Always be polite and professional. End with: "Asante kwa wasiliana." 
"""
question= input("What can I help you with: ")

try:
    message=client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=514,
        system=system_prompt,
        messages=[{"role":"user", "content":question}]
    )
    print(message.content[0].text)
except anthropic.APIConnectionError:
    print("No internet connection. Check your connection and try again.")
except anthropic.AuthenticationError:
    print("Api key is wrong or expired. Check your .env file.")
except anthropic.RateLimitError:
    print("Too many requests. Wait 60 seconds and try again.")

