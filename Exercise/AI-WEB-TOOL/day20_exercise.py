import anthropic
import os
from dotenv import load_dotenv
import json
from flask import Flask, jsonify, render_template,request
from flask_cors import CORS
from datetime import datetime

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API"))
app = Flask(__name__)
CORS(app)
@app.route("/")
def index():
    return render_template("index.html")


def complaint_responder(question):
    system_prompt = """"You are a message Complaint Response Tool.
    Your task is to provide professional and empathetic responses to customer complaints.
    rules:
    - Provide a brief, professional and empathetic response to the complaint.
    - Highlight the key issues raised in the complaint.
    - If complaint is out of your scope, respond with: "Please contact 07 23 724 540 for more enquiries. Thank you."
    - If complaint is huge enough for you not being able to handle it. Push the complaint to email: jksolutions47@gmail.com or send it to 0757822470. You will then respond: "Your complaint has been forwaded and you will be contacted shortly. Asante kwa kuwasiliana."
    - Save the messages to JSON file for future references
    - Always end with: "Asante sana kwa kuwasiliana na wewe."
    
    """
    try:
        messages= []
        
        message = question
            
        messages.append({"role":"user", "content":message})
        response=client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=512,
                system=system_prompt,
                messages=[{"role":"user","content":message}]
            )

        reply = response.content[0]
        messages.append({"role":"assistant", "content":reply})
        if len(messages)>10:
                 messages=messages[-10:]
        log = {
                 "date":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 "messges":messages
            }

        with open("Static/assistant.json", "w") as f:
                    json.dump(log,f,indent=4)
                    return {f"Data saved succesfully."}
    except anthropic.APIConnectionError:
            return jsonify({"No internet connection. Check your connection and try again."})
    except anthropic.AuthenticationError:
             return jsonify({"Api key is wrong or expired. Check your .env file."})
    except anthropic.RateLimitError:
            return jsonify({"Too many requests. Wait 60 seconds and try again."})
    return jsonify({"Message saved succesfully"})


@app.route("/api/complaint", methods=["POST"])
def complaint():
       data= request.get_json()
       question= data["question"]
       result= complaint_responder(question)
       return jsonify(result)


if __name__ == '__main__':
       app.run(debug=True)
           
