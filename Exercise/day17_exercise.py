from datetime import datetime
from flask import Flask, jsonify, request,render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

stock={
    "shed_1":{"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "count": 100},
    "shed_2":{"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "count": 200},
    "shed_3":{"date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "count": 150},
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/eggs", methods=["POST"])
def add_eggs():
    data = request.get_json()
    if not data or "shed" not in data or "count" not in data:
        return jsonify({"error": "shed and count are required"}), 400
    new_eggs={
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "count": data["count"]
    }
    shed = data["shed"]
    if shed in stock:
        stock[shed] = new_eggs
    
    return jsonify({"message": "Eggs added successfully"}), 201

@app.route("/api/eggs/<shed>", methods=["GET"])
def get_eggs(shed):
    if shed in stock:
        return jsonify(stock[shed]), 200
    return jsonify({"error": f"Shed '{shed}' not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)