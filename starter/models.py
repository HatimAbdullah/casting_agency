
import os
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import json, sys

database_name = "alphadb"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

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
    db.create_all()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

actor_movie = db.Table('actor_movie',
    Column('id', db.Integer, primary_key=True),
    Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
)

class Actor(db.Model):
    __tablename__ = 'actor'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    place_of_birth = Column(String)
    contact = Column(String)
    image_link = Column(String)
    has_bio = Column(Boolean, default=True)
    bio = Column(String)
    movies = relationship('Movie', secondary=actor_movie, back_populates='cast', lazy='joined')

    def __init__(self, name, gender, age, place_of_birth, contact, image_link, has_bio, bio):
        self.name = name
        self.gender = gender
        self.age = age
        self.place_of_birth = place_of_birth
        self.contact = contact
        self.image_link = image_link
        self.has_bio = has_bio
        self.bio = bio
        

    def insert(self):
      try:
        db.session.add(self)
        db.session.commit()
      except: 
        db.session.rollback()
        print(sys.exc_info())
  
    def update(self):
      try:
        db.session.commit()
      except: 
        db.session.rollback()
        print(sys.exc_info())

    def delete(self):
      try:
        db.session.delete(self)
        db.session.commit()
      except: 
        db.session.rollback()
        print(sys.exc_info())

    def format(self):
        return {
            'name': self.name,
            'id': self.id,
            'gender': self.gender,
            'age': self.age,
            'movies': [movie.format_with_no_cast() for movie in self.movies]
        }

    def format_no_movies(self):
    	 return {
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
        }
    	 


class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    release_date = Column(String)
    image_link = Column(String)
    film_summary = Column(String)
    cast = relationship('Actor', secondary=actor_movie, back_populates='movies', cascade='save-update, merge', lazy='dynamic')

    def __init__(self, name, release_date, image_link, film_summary):
        self.name = name
        self.release_date = release_date
        self.image_link = image_link
        self.film_summary = film_summary

    def insert(self):
      try:
        db.session.add(self)
        db.session.commit()
      except: 
        db.session.rollback()
        print(sys.exc_info())
  
    def update(self):
      try:
        db.session.commit()
      except: 
        db.session.rollback()
        print(sys.exc_info())

    def delete(self):
      try:
        db.session.delete(self)
        db.session.commit()
      except: 
        db.session.rollback()
        print(sys.exc_info())


    def format(self):
        return {
            'name': self.name,
            'id': self.id,
            'release_date': self.release_date,
            'cast': [actor.format_no_movies() for actor in self.cast],
        }

    def format_with_no_cast(self):
        return {
            'name': self.name,
            'release_date': self.release_date,
        }