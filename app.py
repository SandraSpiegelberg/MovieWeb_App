"""create the Flask app instance"""
import os
from flask import Flask, redirect, render_template, request, url_for
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


def get_movie_info_api(user_id, title):
    """Gets the OMDb information and return it as a Movie object."""
    movies_url = f'{API_URL}apikey={API_KEY}&t={title}'
    res = requests.get(movies_url, timeout=None)
    movie_data = res.json()
    if res.status_code == 200:
        if movie_data['Response'] == 'False':
            msg = f"For movie {title}: "
            msg += movie_data['Error']
            return msg
        movie_title = movie_data['Title']
        movie_year = movie_data['Year']
        movie_director = movie_data['Director']
        movie_poster_url = movie_data['Poster']
        movie = Movie(movie_title, movie_director, movie_year, user_id, movie_poster_url)
        return movie
    else:
        try:
            return movie_data['Error']
        except requests.exceptions.RequestException as req_err:
            return f"Error: {res.status_code}, {req_err}"


@app.route('/', methods=['GET'])
def home():
    """The home page of your application. Show a list of all registered users and 
    a form for adding new users."""
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """When the user submits the “add user” form, a POST request is made.
    The server receives the new user info, adds it to the database,
    then redirects back to home page"""
    new_user = request.form.get('name')
    data_manager.add_user(new_user)
    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    """When you click on a user name, the app retrieves that user’s list 
    of favorite movies and displays it."""
    user = data_manager.get_user(user_id)
    movies = data_manager.get_movies(user_id)
    msg= request.args.get('message')
    return render_template('user.html', user_id=user_id, movies=movies, user=user, message=msg)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_new_movie(user_id):
    """Adds a new movie to a user's (ID) list of favorite movies. 
    also fetch the OMDb info in the DataManager class."""
    #user = User.query.get(user_id)
    title = request.form.get('title')
    new_movie = get_movie_info_api(user_id, title)
    if isinstance(new_movie, Movie):
        data_manager.add_movie(new_movie)
        return redirect(url_for('user_movies', user_id=user_id))
    return redirect(url_for('user_movies', user_id=user_id, message=new_movie))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Modify the title of a specific movie in a user’s list, 
    without depending on OMDb for corrections."""
    old_movie = data_manager.get_movie_by_id(user_id, movie_id)
    old_title = old_movie.movie_title
    new_title = request.form.get('movie-title')
    data_manager.update_movie(movie_id, new_title)
    msg = f"Movie with ID {movie_id} successfully updated! {old_title} was updated to {new_title}."
    return redirect(url_for('user_movies', user_id=user_id, message=msg))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Remove a specific movie from a user’s favorite movie list."""
    movie = data_manager.get_movie_by_id(user_id, movie_id)
    data_manager.delete_movie(movie_id)
    msg = f"Movie {movie.movie_title} sucessfully deleted."
    return redirect(url_for('user_movies', user_id=user_id, message=msg))


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors by rendering a custom template."""
    return render_template('404.html', error=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors by rendering a custom template."""
    return render_template('5oo.html', error=e), 500


@app.errorhandler(Exception)
def unhandled_exception(e):
    """Handle any unhandled exceptions by logging the error and 
    rendering a custom template."""
    app.logger.error('Unhandled Exception: %s', e)
    return render_template('500.html', error=str(e)), 500


if __name__ == "__main__":
    #create the database, only run once
    # with app.app_context():
    #    db.create_all()

    app.run(host="0.0.0.0", port=5002, debug=True)
