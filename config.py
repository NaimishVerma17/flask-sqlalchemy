from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Initialise the flask app
app = Flask(__name__)

# CORS(Cross-Origin-Resource-Sharing) config for the app
CORS(app)

# Assign database configuration to the flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/car_rentals'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the database instance using SQLAlchemy class
db = SQLAlchemy(app)

# Create the marshmallow instance. It is used for serializing and deserializing the request-response objects
ma = Marshmallow(app)

