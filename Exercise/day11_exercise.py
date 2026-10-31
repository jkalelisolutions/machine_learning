"""A customer assistant chatbot used to reply members of a Sacco.

To setup:
1. Run pip install anthropic python-dotenv
2. Create new file .env with: ANTHROPIC_API=your_api_key_here
3. Get your API key from https://platform.claude.com 

To run:
Python day11_exercise.py
"""

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

Examples:
User: "What is my balance?"
Answer: Your balance is KES 50,000 shillings.

User: "When is the next meeting?"
Answer: The next meeting is on 02-11-2026 on a Monday. It will start at 2:00pm in the evening.

User: "What are the current membership fees?"
Answer: The current membership fees is KES 1000 shillings
"""
question= input("What can I help you with: ")

try:
    message=client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=514,
        system=system_prompt,
        messages=[{"role":"user", "content":question}]
    )
    print(message.content[0])
except anthropic.APIConnectionError:
    print("No internet connection. Check your connection and try again.")
except anthropic.AuthenticationError:
    print("Api key is wrong or expired. Check your .env file.")
except anthropic.RateLimitError:
    print("Too many requests. Wait 60 seconds and try again.")

