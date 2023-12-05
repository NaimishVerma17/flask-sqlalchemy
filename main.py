from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from flask_marshmallow import Marshmallow
from marshmallow_enum import EnumField
import enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/car_rentals'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class GearEnum(enum.Enum):
    manual = 'manual'
    automatic = 'automatic'


class TypeEnum(enum.Enum):
    diesel = 'diesel'
    petrol = 'petrol'


class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)
    image = db.Column(db.String(255))
    color = db.Column(db.String(255))
    brand = db.Column(db.String(255))
    type = db.Column(Enum(TypeEnum))
    gear = db.Column(Enum(GearEnum))
    price = db.Column(db.Double())

    def __init__(self, name, image, color, type, gear, brand, price):
        self.name = name
        self.image = image
        self.color = color
        self.type = type
        self.gear = gear
        self.brand = brand
        self.price = price


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    from_date = db.Column(db.DateTime())
    to_date = db.Column(db.DateTime())
    car_id = db.Column(db.Integer(), db.ForeignKey(Car.id), primary_key=True)
    car = db.relationship('Car', foreign_keys='Order.car_id')

    def __init__(self, name, email, phone_number, from_date, to_date, car_id):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.from_date = from_date
        self.to_date = to_date
        self.car_id = car_id


class CarSchema(ma.Schema):
    type = EnumField(TypeEnum, by_value=True)
    gear = EnumField(GearEnum, by_value=True)

    class Meta:
        fields = ('id', 'name', 'color', 'image', 'brand', 'price', 'gear', 'type')


car_schema = CarSchema()
cars_schema = CarSchema(many=True)

with app.app_context():
    db.create_all()


@app.route('/orders', methods=['Post'])
def create_task():
    try:
        name = request.json['name']
        email = request.json['email']
        phone_number = request.json['phone_number']
        from_date = request.json['from_date']
        to_date = request.json['to_date']
        car_id = request.json['car_id']

        order = Order(name, email, phone_number, from_date, to_date, car_id)

        db.session.add(order)
        db.session.commit()

        return {"success": True}
    except Exception as ex:
        print(ex)
        return {"success": False}


@app.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    result = cars_schema.dump(cars)
    return jsonify(result)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to car rental API'})


if __name__ == "__main__":
    app.run(debug=True)
