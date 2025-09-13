"""create the Flask app instance"""
import os
from flask import Flask
from data_manager import DataManager
from models import Movie, User, db
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('API_KEY')

API_URL = "http://www.omdbapi.com/?"

app = Flask(__name__)

#random key only for development
app.secret_key = os.urandom(24)

#set the database URI using an absolute path, after initialized Flask app
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app.

data_manager = DataManager() # Create an object of your DataManager class
