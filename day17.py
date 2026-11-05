from flask import Flask, request, jsonify
app = Flask(__name__)

orders = [
    {"id":1, "customer":"Hassan Traders", "product":"maize flour", "qty":50, "status":"pending"},
    {"id":2, "customer":"Otieno Wholesale", "product":"rice", "qty":30, "status":"delivered"}
]

@app.route("/api/orders", methods=["GET"])
def get_orders():
    return jsonify(orders), 200

@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    if not data or "customer" not in data or "product" not in data:
        return jsonify({"error": "customer and product are required"}), 400

    new_order={
        "id": len(orders) +1,
        "customer": data["customer"],
        "product": data["product"],
        "qty": data.get("qty", 0),
        "status": "pending"
    }
    orders.append(new_order)
    return jsonify(new_order), 201