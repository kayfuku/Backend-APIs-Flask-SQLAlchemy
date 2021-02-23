import os
from sqlalchemy import Column, String, Integer, DateTime, \
    ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Movie
Have title and release date
'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)
    casts = db.relationship('Cast', backref=db.backref('movie', lazy=True),
                            cascade="all, delete-orphan")

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return '<Movie %r>' % self

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("%m/%d/%Y")
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    casts = db.relationship('Cast', backref=db.backref('actor', lazy=True),
                            cascade="all, delete-orphan")

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return '<Actor %r>' % self

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


class Cast(db.Model):
    '''Join table (Associated/Intermediary table) between Movie and Actor'''

    __tablename__ = 'casts'

    id = db.Column(Integer, primary_key=True)
    movie_id = db.Column(Integer, ForeignKey(Movie.id), nullable=False)
    actor_id = db.Column(Integer, ForeignKey(Actor.id), nullable=False)

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def __repr__(self):
        return '<Cast %r>' % self

    def get_dict(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id,
        }
