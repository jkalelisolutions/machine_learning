from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app) #Allows all origins in development, for production use specific origins

#For production, restrict to your frontend domain, e.g., CORS(app, origins=["https://yourfrontend.com"])

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "text is required"}), 400
    text=data.get("text")
    result = summarize_text(text)
    return jsonify({"summary": result}), 200

if __name__ == '__main__':
    app.run(debug=True)