from flask import Flask, request, jsonify
from config import db, app
from models import Car, cars_schema, Order, orders_schema

with app.app_context():
    db.create_all()


@app.route('/orders', methods=['Post'])
def create_order():
    try:
        name = request.json['name']
        email = request.json['email']
        phone_number = request.json['phone_number']
        from_date = request.json['from_date']
        to_date = request.json['to_date']
        car_id = request.json['car_id']
        car = Car.query.get(car_id)
        if car.stock == 0:
            return {"success": False, "message": "Out of stock."}, 400
        order = Order(name, email, phone_number, from_date, to_date, car_id)
        car.stock = car.stock - 1
        db.session.add(order)
        db.session.commit()

        return {"success": True}, 201
    except Exception as ex:
        return {"success": False, "message": "Unable to create order. Something went wrong!"}, 500


@app.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    result = cars_schema.dump(cars)
    return jsonify(result), 200


@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    result = orders_schema.dump(orders)
    return jsonify(result), 200


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to car rental API'})


if __name__ == "__main__":
    app.run(debug=True)
