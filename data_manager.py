"""Module to manage data operations for Users and Movies."""
from models import Movie, User, db

class DataManager():
    """Class to manage CRUD options for Users and Movies in the database.
    """
    def get_users(self):
        """Get all users from the database."""
        users = User.query.all()
        return users


    def get_user(self, user_id: int):
        """Get a user by their ID."""
        user = db.session.get(User, user_id)
        return user


    def add_user(self, name: str):
        """Add a new user to the database."""
        new_user = User(user_name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user


    def get_movies(self, user_id: int):
        """Get all movies for a specific user by their user ID."""
        movies = Movie.query.filter_by(user_id=user_id).all()
        return movies


    def get_movie_by_id(self, movie_id: int):
        """Get a movie by their movie ID."""
        movie = db.session.get(Movie, movie_id)
        return movie


    def add_movie(self, movie: Movie):
        """Add a new movie to the database."""
        if not isinstance(movie, Movie):
            raise ValueError('The provided movie is not a valid Movie instance.')
        db.session.add(movie)
        db.session.commit()
        return f'Movie {movie.movie_title} successfully added to your library!'


    def update_movie(self, movie_id, new_title):
        """Update an existing movie's title."""
        movie = db.session.get(Movie, movie_id)
        if movie:
            movie.movie_title = new_title
            db.session.commit()
            return f'Movie with ID {movie_id} successfully updated to {new_title}!'
        return None

    def delete_movie(self, movie_id):
        """Delete a movie from the database by it's ID."""
        movie = db.session.get(Movie, movie_id)
        if movie:
            title = movie.movie_title
            db.session.delete(movie)
            db.session.commit()
            return f'Movie {title} successfully deleted from your library!'
        return f'Movie with ID {movie_id} not found.'
