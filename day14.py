import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

client= anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API"))

tools=[{
    "name":"get_stock_level",
    "description":"Get the current stock quantity for a product at Kamau Stores",
    "input_schema":{
        "type":"object",
        "properties":{
            "product_name":{
                "type":"string",
                "description":"The name of the product to check"
            }
        },
        "required":["product_name"]
    }
}]

#Simulate a database lookup (in a production system, this queries SQlite or an API)
inventory={
    "maize flour":120,
    "wheat flour":85,
    "rice":200,
    "sugar":0,
    "cooking oil":45
}
question=input("Ask me anything: ")
def get_stock_level(product_name):
    product=product_name.lower()
    if product in inventory:
        qty=inventory[product]
        if qty == 0:
            return f"{product_name} is currently out of stock."
        return f"{product_name}:{qty} bags in stock."
    return f"product '{product_name}' not fount in the system."

try:
    response= client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        tools=tools,
        messages=[{"role":"user", "content":question}]
    )
    if response.stop_reason == "tool_use":
        tool_use= response.content[1]#the tool call back

        fn_name=tool_use.name
        fn_input=tool_use.input

        result=get_stock_level(fn_input["product_name"])
        print(f"Function called {fn_name}({fn_input})")
        print(f"Result:{result}")
except anthropic.APIConnectionError:
    print("No internet connection. Check your connection and try again.")
except anthropic.AuthenticationError:
    print("Api key is wrong or expired. Check your .env file.")
except anthropic.RateLimitError:
    print("Too many requests. Wait 60 seconds and try again.")