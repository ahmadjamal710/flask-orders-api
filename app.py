from flask import Flask, request, jsonify

app = Flask(__name__)

orders = [
    {"id": 1, "customer": "Ahmad", "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
    {"id": 2, "customer": "Ayman", "item": "Mouse", "quantity": 2, "price": 19.99, "status": "pending"}
]
next_id = 3

def find_order(order_id):
    return next((o for o in orders if o["id"] == order_id), None)

@app.route('/')
def home():
    return {"msg": "Orders API ready!"}

@app.route('/orders', methods=['GET', 'POST'])
def handle_orders():
    global next_id
    if request.method == 'GET':
        return jsonify(orders)
    data = request.get_json()
    if not all(k in data for k in ['customer', 'item', 'quantity', 'price']):
        return {"error": "Missing fields"}, 400
    order = {**data, "id": next_id, "status": "pending"}
    orders.append(order)
    next_id += 1
    return jsonify(order), 201

@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_order(order_id):
    order = find_order(order_id)
    if not order:
        return {"error": "Not found"}, 404
    if request.method == 'GET':
        return jsonify(order)
    if request.method == 'PUT':
        data = request.get_json()
        order.update(data)
        return jsonify(order)
    if request.method == 'DELETE':
        orders.remove(order)
        return {"msg": "Deleted"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)

