import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import database_exists, create_database

# HELPER IMPORT FOR TEST
# import datetime


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#    ___       _        _                     ___           __ _
#   |   \ __ _| |_ __ _| |__  __ _ ___ ___   / __|___ _ _  / _(_)__ _
#   | |) / _` |  _/ _` | '_ \/ _` (_-</ -_) | (__/ _ \ ' \|  _| / _` |
#   |___/\__,_|\__\__,_|_.__/\__,_/__/\___|  \___\___/_||_|_| |_\__, |
#                                                               |___/

'''
Database configuration. Set up enviroment variables in the terminal:

DB_USER = "postgres"
DB_PASSWORD = "postgres"

'''

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
database_host = "localhost:5432"
database_name = "casting_agency"

database_path = "postgresql://{}:{}@{}/{}".format(
    DB_USER,
    DB_PASSWORD,
    database_host,
    database_name
    )

db = SQLAlchemy()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#    ___       _        _                    ___      _
#   |   \ __ _| |_ __ _| |__  __ _ ___ ___  / __| ___| |_ _  _ _ __
#   | |) / _` |  _/ _` | '_ \/ _` (_-</ -_) \__ \/ -_)  _| || | '_ \
#   |___/\__,_|\__\__,_|_.__/\__,_/__/\___| |___/\___|\__|\_,_| .__/
#                                                             |_|

'''
Setup database. This binds the databese with app server.
It checks if the database exists and creates it if it doesn't
'''


def setup_db(app):
    if not database_exists(database_path):
        create_database(database_path)

    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()

    # TEST IF IT WORKS TO THIS POINT:
    # movie = Movie(
    #     title = 'Testing',
    #     release_date = datetime.date(2010, 5, 1)
    # )
    # movie.insert()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#    __  __         _     _
#   |  \/  |___  __| |___| |___
#   | |\/| / _ \/ _` / -_) (_-<
#   |_|  |_\___/\__,_\___|_/__/
#

'''
Movies with attributes title and release date with functions to:
insert (new movie to database), format (to return formatted object)
'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

'''
Actors with attributes name, age and gender with functions:
insert (new actor to database), format (to return formatted object)
'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(100), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
