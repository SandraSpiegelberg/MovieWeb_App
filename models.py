"""create the SQLAlchemy db instance
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


user_movie = db.Table(
    'user_movie',
    db.Column('user_id', db.Integer, db.ForeignKey('Users.user_id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('Movies.movie_id'), primary_key=True)
)


class User(db.Model):
    """Class for objects who represents an user in the db libary.
    """
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False, unique=True)

    movie = db.relationship('Movie', secondary=user_movie, backref='user')


    def __init__(self, user_name, user_id=None):
        self.user_name = user_name
        self.user_id = user_id


    def __repr__(self):
        return f'User(user_id = {self.user_id}, user_name = {self.user_name})'


    def __str__(self):
        return f'User {self.user_name} with id {self.user_id}'


class Movie(db.Model):
    """Class for objects who represents a movie in the db libary.
    """
    __tablename__ = 'Movies'

    __table_args__ = (
        db.UniqueConstraint('movie_title','director', 'year', name='unique_movie'),
    )

    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_title = db.Column(db.String(200), nullable=False)
    movie_director = db.Column(db.String(100), nullable=False)
    movie_year = db.Column(db.Integer, nullable=False)
    movie_poster_url = db.Column(db.String(300), nullable=True)
    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)


    def __init__(self, title, director, year, user_id, poster_url, movie_id=None):
        self.movie_id = movie_id
        self.movie_title = title
        self.movie_director = director
        self.movie_year = year
        self.movie_poster_url = poster_url
        self.user_id = user_id


    def __repr__(self):
        return f'''Movie(movie_id = {self.movie_id}, movie_title = {self.movie_title},
            director = {self.director}, year = {self.year}, poster_url = {self.poster_url},
            user_id = {self.user_id})'''


    def __str__(self):
        return f'''Movie {self.movie_title} directed by {self.director}
            in {self.year} with id {self.movie_id}'''
