from base import db
from sqlalchemy.dialects.mysql import JSON

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    movies = db.Column(JSON, nullable=False)
    games = db.Column(JSON, nullable=False)

    def __init__(self, name, age, movies, games):
        self.name = name
        self.age = age
        self.movies = movies
        self.games = games

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "movies": self.movies,
            "games": self.games
        }
