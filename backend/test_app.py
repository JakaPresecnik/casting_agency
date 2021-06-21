import os
import unittest
import json
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import database_exists, create_database
from werkzeug.datastructures import Authorization

from app import create_app
from models import *

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZrSzl5dTNpM09SNlRkSzdwR0NobCJ9.eyJpc3MiOiJodHRwczovL2Rldi1iZm4tOHIxdC5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDg0ODA5MDY1Mzk5NzAxMTUzNTUiLCJhdWQiOlsiY2FzdGluZ19hZ2VuY3kiLCJodHRwczovL2Rldi1iZm4tOHIxdC5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjI0MTczNTgyLCJleHAiOjE2MjQyNTk5ODIsImF6cCI6IjV0SERzRkJtazFCQ1VydlN2SlM0REFtSFlMb3ljaDFFIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.ek5Zt458zwwxGh3Fd78Ulra9NXx4rktSIDvlRcXnDSfULn5FmAepTPUrmceiL0V7PKioO228fCXAX-ygUuppQ_gWYyQsKUfr0wdEGS8OjFGPHLqgzrfwvUD6xFg9rX73IMOqIkcXJMZgPPC75Nc8l5zEpMVjTeSazUCYznFXeeyFZkTSa1GqjI4u2LGFG6Q6JAIePihw0EY4TMbXUtFOnhoKL5UB43U65GRXfRVw1bBX1P1d2PUsLbD3vU5lbsClcJBZ5WZ0WjuNd7ZmAmGOmz5vo8NX9iUoFc8nSLxBtZj4lQp_594k6IxdT9pHp2dUklxic_UMewM2iUzRCCgXGQ'
JWT = 'bearer ' + token
second_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZrSzl5dTNpM09SNlRkSzdwR0NobCJ9.eyJpc3MiOiJodHRwczovL2Rldi1iZm4tOHIxdC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ZTZiY2QwZjcyYjQwMDY3YjNjM2U2IiwiYXVkIjpbImNhc3RpbmdfYWdlbmN5IiwiaHR0cHM6Ly9kZXYtYmZuLThyMXQuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYyNDE3MzI1OSwiZXhwIjoxNjI0MjU5NjU5LCJhenAiOiI1dEhEc0ZCbWsxQkNVcnZTdkpTNERBbUhZTG95Y2gxRSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.ieEKPPciq1By4s6uieekhIpIsx-NFRXW2NIE0SOF0ri6P_9u5NUt_9PNQC2rAlaSDPxmgLJmXuzrpopbKpMRSujMTcfPIusu7fcsVOTApriScwEeXBynmOgn7BB9sl2SbZGkU_Cd7exHGzOUH_JVDGxWi-TeVzM8clGhjqk0bcrvUssH4ziZCdApyfMr7tjcnlEZkrvDXZvj5HrjaCdaYxHYh0-uFIv9omJaSodbniHiLy8PpYv0QD_PsRkI1Bi6HEPpPoh1z8kZsXOovh5E2wjMJegUqV837QMozVlop9K8M1R542ilF9pib_aGxqp6wCUq-KFkVrb4cI-m2Gf4dw'
second_JWT = 'bearer ' + second_token


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
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': JWT
            }
        self.second_headers = {
            'Content-Type': 'application/json',
            'Authorization': second_JWT
        }

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
        res = self.client().get('/actors', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
    
    def test_assistant_get_actors(self):
        res = self.client().get('/actors', headers=self.second_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_get_actors_beyond_valid_page(self):
        res = self.client().get(
            '/actors?page=999',
            headers=self.headers
            )
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
        res = self.client().get('/movies', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_get_movies_beyond_valid_page(self):
        res = self.client().get(
            '/movies?page=999',
            headers=self.headers
            )
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
        res = self.client().delete('/actors/1', headers=self.headers)
        data = json.loads(res.data)

        actor = Actor.query.filter_by(id=1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)

    def test_404_delete_actor_not_exist(self):
        res = self.client().delete('/actors/1000', headers=self.headers)
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
        res = self.client().delete('/movies/1', headers=self.headers)
        data = json.loads(res.data)

        movie = Movie.query.filter_by(id=1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie, None)

    def test_404_delete_movie_not_exist(self):
        res = self.client().delete('/actors/1000', headers=self.headers)
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
        res = self.client().post(
            '/actors',
            json=test_actor,
            headers=self.headers
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_actor']['name'], test_actor['name'])

    def test_assistant_post_actor(self):
        test_actor = {
            "name": "Mr. Assistant Test",
            "age": "25",
            "gender": "Unknown"
        }
        res = self.client().post(
            '/actors',
            json=test_actor,
            headers=self.second_headers
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)

    def test_422_post_actor_no_body(self):
        res = self.client().post(
            '/actors',
            json={},
            headers=self.headers
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_400_post_actor_actor_data_not_included(self):
        res = self.client().post(
            '/actors',
            json={'wrong': 'data'},
            headers=self.headers
            )
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
        res = self.client().post(
            '/actors',
            json=test_actor,
            headers=self.headers
            )
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
        res = self.client().post(
            '/movies',
            json=test_movie,
            headers=self.headers
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_movie']['title'], test_movie['title'])

    def test_422_post_movie_no_body(self):
        res = self.client().post('/movies', json={}, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_400_post_movie_movie_data_not_included(self):
        res = self.client().post(
            '/movies',
            json={'wrong': 'data'},
            headers=self.headers
            )
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
        res = self.client().patch(
            '/actors/2',
            json={'age': '40'},
            headers=self.headers
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_actor']['age'], 40)

    def test_404_patch_actors_not_exist(self):
        res = self.client().patch(
            '/actors/1000',
            json={'age': '41'},
            headers=self.headers
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_422_post_actors_no_body(self):
        res = self.client().patch('/actors/2', json={}, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_400_patch_actor_actor_data_not_included(self):
        res = self.client().patch(
            '/actors/2',
            json={'wrong': 'data'},
            headers=self.headers
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_409_post_actor_actor_already_enlisted(self):
        res = self.client().patch(
            '/actors/2',
            json={"name": "Actor 2"},
            headers=self.headers
            )
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
        res = self.client().patch(
            '/movies/2',
            json={'title': 'New Title'},
            headers=self.headers
            )
        data = json.loads(res.data)

        movie = Movie.query.filter_by(id=2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_movie']['title'], 'New Title')

    def test_422_patch_movies_no_body(self):
        res = self.client().patch(
            '/movies/2',
            json={},
            headers=self.headers
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_404_patch_movie_not_exist(self):
        res = self.client().patch(
            '/movies/1000',
            json={'title': 'Not Ex'},
            headers=self.headers
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_400_patch_movie_movie_data_not_included(self):
        res = self.client().patch(
            '/movies/2',
            json={'wrong': 'data'},
            headers=self.headers
            )
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
