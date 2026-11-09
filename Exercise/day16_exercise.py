from flask import Flask,jsonify

app=Flask(__name__)

@app.route("/")
def home():
    return "Eldoret hardware shop API is running..."


Inventory= {"Jackson Kaleli": 30000,
            "Damien Mwabungo": 50000,
            "Pili Asha": 20000,
            "Elijah Mwendwa": 60000,
            "Norah Mbaika": 70000}

@app.route("/api/balance")
def check_balance():
    
    return jsonify(Inventory), 200 

@app.route("/api/balance/<customer>")
def get_balance(customer):
    for key,value in Inventory.items():
        if key == customer:
            return jsonify({key:value}), 200
    return jsonify({"error": f"Customer '{customer}' not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
