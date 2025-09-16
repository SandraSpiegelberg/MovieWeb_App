"""create the Flask app instance"""
import os
from flask import Flask, request
from dotenv import load_dotenv
import requests

from data_manager import DataManager
from models import Movie, db


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
#output of SQL commands in terminal
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)  # Link the database and the app.

data_manager = DataManager() # Create an object of your DataManager class


@app.route('/', methods=['GET'])
def home():
    """The home page of your application. Show a list of all registered users and 
    a form for adding new users."""
    return "Welcome to MoviWeb App!"


@app.route('/users')
def list_users():
    """Page that lists all users"""
    users = data_manager.get_users()
    return str(users)  # Temporarily returning users as a string


@app.route('/users', methods=['POST'])
def create_user():
    """When the user submits the “add user” form, a POST request is made.
    The server receives the new user info, adds it to the database,
    then redirects back to home page"""
    new_user = request.form.get('name')
    data_manager.add_user(new_user)
    return f'New user {new_user} is created.'


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    """When you click on a user name, the app retrieves that user’s list 
    of favorite movies and displays it."""
    #user = data_manager.get_user(user_id)
    movies = data_manager.get_movies(user_id)
    return movies



@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_new_movie(user_id):
    """Adds a new movie to a user's (ID) list of favorite movies. 
    also fetch the OMDb info in the DataManager class."""
    #user = User.query.get(user_id)
    title = request.form.get('title')
    movies_url = f'{API_URL}apikey={API_KEY}&t={title}'
    res = requests.get(movies_url, timeout=None)
    movie_data = res.json()
    if res.status_code == 200:
        if movie_data['Response'] == 'False':
            return movie_data['Error']
        else:
            movie_title = movie_data['Title']
            movie_year = movie_data['Year']
            movie_director = movie_data['Director']
            movie_poster_url = movie_data['Poster']
            new_movie = Movie(movie_title, movie_director, movie_year, user_id, movie_poster_url)
            msg = data_manager.add_movie(new_movie)
            return msg
    else:
        try:
            return movie_data['Error']
        except requests.exceptions.RequestException as req_err:
            return f"Error: {res.status_code}, {req_err}"


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Modify the title of a specific movie in a user’s list, 
    without depending on OMDb for corrections."""
    old_movie = data_manager.get_movie_by_id(user_id, movie_id)
    new_title = request.form.get('title')
    data_manager.update_movie(movie_id, new_title)
    msg = f"{old_movie} was updated to {new_title}."
    return msg


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Remove a specific movie from a user’s favorite movie list."""
    movie = data_manager.get_movie_by_id(user_id, movie_id)
    data_manager.delete_movie(movie_id)
    msg = f"Movie {movie.movie_title} sucessfully deleted."
    return msg


if __name__ == "__main__":
    #create the database, only run once
    # with app.app_context():
    #    db.create_all()

    app.run(host="0.0.0.0", port=5002, debug=True)
