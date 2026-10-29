import anthropic
import os
from dotenv import load_dotenv

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

system_prompt="""You are a customer service assistant for Kamau Stores, a wholesale distributor in Nairobi.
Your rules:
- Only answer questions about orders, pricing, and delivery.
- All prices are in KES. Never mention USD.
- Delivery covers Nairobi, Mombasa, Kisumu, and Nakuru only
- If a question is outside your scope, say: "Please call our office on 0712 345 678 for that."
- Always be polite and professional. End with "Asante kwa Kuwasiliana."



Extract the order details from the customer message.
Return ONLY valid JSON in this format:
{"product": "...", "quantity": ..., "urgency":"normal" or "urgent"}
No explanation. No markdown. Just the JSON.

"""

message= client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=512,
    system=system_prompt,
    messages=[{"role":"user","content":"Do you deliver to Eldoret?"}]
)

print(message.content[0].text)