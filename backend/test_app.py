import os
import unittest
import json
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import database_exists, create_database

from app import create_app
from models import *


class CastingAgencyTestCase(unittest.TestCase):

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #    _____       _     ___      _
    #   |_   _|__ __| |_  / __| ___| |_ _  _ _ __
    #     | |/ -_|_-<  _| \__ \/ -_)  _| || | '_ \
    #     |_|\___/__/\__| |___/\___|\__|\_,_| .__/
    #                                       |_|

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')
        self.db_host = 'localhost:5432'
        self.db_name = 'casting_agency_test'
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.DB_USER,
            self.DB_PASSWORD,
            self.db_host,
            self.db_name
        )

        setup_db(self.app, self.database_path)

        # Initiate the database if not existant
        if not database_exists(self.database_path):
            create_database(self.database_path)

        # Bind the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
            self.actor = Actor(
                name='Initial Actor',
                age=32,
                gender='Test'
            )
            self.movie = Movie(
                title="Initial Movie",
                release_date=datetime.date(2010, 5, 1)
            )
            self.actor.insert()
            self.movie.insert()

            self.actor = Actor(
                name='Actor 2',
                age=32,
                gender='Test'
            )
            self.movie = Movie(
                title="Initial Movie 2",
                release_date=datetime.date(2010, 5, 1)
            )
            self.actor.insert()
            self.movie.insert()

    def tearDown(self):
        pass


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#    _____       _
#   |_   _|__ __| |_ ___
#     | |/ -_|_-<  _(_-<
#     |_|\___/__/\__/__/
#

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#              __             __                 __          __
#    ___ ____ / /_  ___ _____/ /____  _______   / /____ ___ / /____
#   / _ `/ -_) __/ / _ `/ __/ __/ _ \/ __(_-<  / __/ -_|_-</ __(_-<
#   \_, /\__/\__/  \_,_/\__/\__/\___/_/ /___/  \__/\__/___/\__/___/
#  /___/

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_get_actors_beyond_valid_page(self):
        res = self.client().get('/actors?page=999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#              __                   _           __          __
#    ___ ____ / /_  __ _  ___ _  __(_)__ ___   / /____ ___ / /____
#   / _ `/ -_) __/ /  ' \/ _ \ |/ / / -_|_-<  / __/ -_|_-</ __(_-<
#   \_, /\__/\__/ /_/_/_/\___/___/_/\__/___/  \__/\__/___/\__/___/
#  /___/

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_get_movies_beyond_valid_page(self):
        res = self.client().get('/movies?page=999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#       __    __    __                 __                 __          __
#   ___/ /__ / /__ / /____   ___ _____/ /____  _______   / /____ ___ / /____
#  / _  / -_) / -_) __/ -_) / _ `/ __/ __/ _ \/ __(_-<  / __/ -_|_-</ __(_-<
#  \_,_/\__/_/\__/\__/\__/  \_,_/\__/\__/\___/_/ /___/  \__/\__/___/\__/___/
#

    def test_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        actor = Actor.query.filter_by(id=1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)

    def test_404_delete_actor_not_exist(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#       __    __    __                       _           __          __
#   ___/ /__ / /__ / /____   __ _  ___ _  __(_)__ ___   / /____ ___ / /____
#  / _  / -_) / -_) __/ -_) /  ' \/ _ \ |/ / / -_|_-<  / __/ -_|_-</ __(_-<
#  \_,_/\__/_/\__/\__/\__/ /_/_/_/\___/___/_/\__/___/  \__/\__/___/\__/___/
#

    def test_delete_movies(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        movie = Movie.query.filter_by(id=1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie, None)

    def test_404_delete_movie_not_exist(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                    __             __                 __          __
#     ___  ___  ___ / /_  ___ _____/ /____  _______   / /____ ___ / /____
#    / _ \/ _ \(_-</ __/ / _ `/ __/ __/ _ \/ __(_-<  / __/ -_|_-</ __(_-<
#   / .__/\___/___/\__/  \_,_/\__/\__/\___/_/ /___/  \__/\__/___/\__/___/
#  /_/

    def test_post_actor(self):
        test_actor = {
            "name": "Mr. Test",
            "age": "25",
            "gender": "Unknown"
        }
        res = self.client().post('/actors', json=test_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_actor']['name'], test_actor['name'])

    def test_422_post_actor_no_body(self):
        res = self.client().post('/actors', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_400_post_actor_actor_data_not_included(self):
        res = self.client().post('/actors', json={'wrong': 'data'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_409_post_actor_actor_already_enlisted(self):
        test_actor = {
             "name": "Initial Actor",
             "age": "25",
             "gender": "Unknown"
         }
        res = self.client().post('/actors', json=test_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 409)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                    __                   _           __          __
#     ___  ___  ___ / /_  __ _  ___ _  __(_)__ ___   / /____ ___ / /____
#    / _ \/ _ \(_-</ __/ /  ' \/ _ \ |/ / / -_|_-<  / __/ -_|_-</ __(_-<
#   / .__/\___/___/\__/ /_/_/_/\___/___/_/\__/___/  \__/\__/___/\__/___/
#  /_/

    def test_post_movies(self):
        test_movie = {
            "title": "Tester",
            "release_date":  "2022-02-02",
        }
        res = self.client().post('/movies', json=test_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_movie']['title'], test_movie['title'])

    def test_422_post_movie_no_body(self):
        res = self.client().post('/movies', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_400_post_movie_movie_data_not_included(self):
        res = self.client().post('/movies', json={'wrong': 'data'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                __      __              __                 __          __
#     ___  ___ _/ /_____/ /    ___ _____/ /____  _______   / /____ ___ / /____
#    / _ \/ _ `/ __/ __/ _ \  / _ `/ __/ __/ _ \/ __(_-<  / __/ -_|_-</ __(_-<
#   / .__/\_,_/\__/\__/_//_/  \_,_/\__/\__/\___/_/ /___/  \__/\__/___/\__/___/
#  /_/

    def test_patch_actors(self):
        res = self.client().patch('/actors/2', json={'age': '40'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_actor']['age'], 40)

    def test_404_patch_actors_not_exist(self):
        res = self.client().patch('/actors/1000', json={'age': '41'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_422_post_actors_no_body(self):
        res = self.client().patch('/actors/2', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_400_patch_actor_actor_data_not_included(self):
        res = self.client().patch('/actors/2', json={'wrong': 'data'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_409_post_actor_actor_already_enlisted(self):
        res = self.client().patch('/actors/2', json={"name": "Actor 2"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 409)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                __      __                    _           __          __
#     ___  ___ _/ /_____/ /    __ _  ___ _  __(_)__ ___   / /____ ___ / /____
#    / _ \/ _ `/ __/ __/ _ \  /  ' \/ _ \ |/ / / -_|_-<  / __/ -_|_-</ __(_-<
#   / .__/\_,_/\__/\__/_//_/ /_/_/_/\___/___/_/\__/___/  \__/\__/___/\__/___/
#  /_/

    def test_patch_movies(self):
        res = self.client().patch('/movies/2', json={'title': 'New Title'})
        data = json.loads(res.data)

        movie = Movie.query.filter_by(id=2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_movie']['title'], 'New Title')

    def test_422_patch_movies_no_body(self):
        res = self.client().patch('/movies/2', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_404_patch_movie_not_exist(self):
        res = self.client().patch('/movies/1000', json={'title': 'Not Ex'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_400_patch_movie_movie_data_not_included(self):
        res = self.client().patch('/movies/2', json={'wrong': 'data'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#    ___                 _         _____       _
#   | __|_ _____ __ _  _| |_ ___  |_   _|__ __| |_
#   | _|\ \ / -_) _| || |  _/ -_)   | |/ -_|_-<  _|
#   |___/_\_\___\__|\_,_|\__\___|   |_|\___/__/\__|
#

if __name__ == "__main__":
    unittest.main()
