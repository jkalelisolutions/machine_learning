#app.py -- your first Flask app
from flask import Flask, jsonify, request

app=Flask(__name__)

@app.route('/')
def home():
    return "Kamau Stores API is running"


inventory={
    "maize flour": {"price": 100, "stock": 50},
    "rice": {"price": 120, "stock": 30},
    "cooking oil": {"price": 150, "stock": 20},
}

@app.route("/api/products")
def get_products():
    return jsonify(inventory), 200

@app.route("/api/products/<product_name>")
def get_product(product_name):
    if product_name in inventory:
        data = inventory[product_name]
        data["name"] = product_name
        return jsonify(data), 200
    return jsonify({"error": f"Product '{product_name}' not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)