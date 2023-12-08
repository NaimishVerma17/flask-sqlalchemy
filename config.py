import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Initialise the flask app
app = Flask(__name__)

# CORS(Cross-Origin-Resource-Sharing) config for the app
CORS(app)

# Fetch db config from environment variables
MYSQL_HOST = os.environ.get('AZURE_MYSQL_HOST') or 'localhost'
MYSQL_NAME = os.environ.get('AZURE_MYSQL_NAME') or 'car_rentals'
MYSQL_USER = os.environ.get('AZURE_MYSQL_USER') or 'root'
MYSQL_PASSWORD = os.environ.get('AZURE_MYSQL_PASSWORD') or 'password'

# Assign database configuration to the flask app
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://%s:%s@%s/%s" % (
    MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_NAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the database instance using SQLAlchemy class
db = SQLAlchemy(app)

# Create the marshmallow instance. It is used for serializing and deserializing the request-response objects
ma = Marshmallow(app)
