import anthropic
import os
import json
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

client= anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API"))

#Rules that the AI will strictly follow to avoid misguiding clients
system_prompt="""You are a customer service assistant for a Matatu Sacco.
Your Rules:
-Only answer questions about balance, meeting, current membership fees
-Finance is in KES
-If question is out of scope, say:"Please call our offices on 0711 245 750 for that."
-Always be polite and professional. End with: "Asante kwa wasiliana.

Examples:
User: "What is my balance?"
Answer: Your balance is KES 50,000 shillings.

User: "When is the next meeting?"
Answer: The next meeting is on 02-11-2026 on a Monday. It will start at 2:00pm in the evening.

User: "What are the current membership fees?"
Answer: The current membership fees is KES 1000 shillings.
"""
messages=[]
try:
    while True:
        question=input("What can I help you with: ")
        if question.lower()=="exit":
            break
        messages.append({"role":"user","content":question})
        response=client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=514,
            system=system_prompt,
            messages=[{"role":"user", "content":question}]
        )
        reply=response.content[0]
        messages.append({"role":"assistant","content":reply})
        print(f"Assistant: {reply}")
        if len(messages)>10:
            messages=messages[-10:]
        log={
            "date":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "messages":messages
        }

        with open("day13.json", "w") as f:
            json.dump(log,f,indent=2)
except anthropic.APIConnectionError:
    print("No internet connection. Check your connection and try again.")
except anthropic.AuthenticationError:
    print("Api key is wrong or expired. Check your .env file.")
except anthropic.RateLimitError:
    print("Too many requests. Wait 60 seconds and try again.")