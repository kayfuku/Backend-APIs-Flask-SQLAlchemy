import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Movie, Actor, Cast
from auth import CASTING_ASSISTANT_TOKEN, EXECUTIVE_PRODUCER_TOKEN, \
    EXPIRED_TOKEN


def get_auth_header(token):
    return {'Authorization': f'Bearer {token}'}


class TestCase(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test
    """

    '''
    Test create, read, update, delete movies.
    '''

    def test_get_greeting(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['greeting'], "Hello")

    def test_generate_login_url(self):
        res = self.client().get('/login')
        self.assertEqual(res.status_code, 200)

    def test_get_movies(self):
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        res = self.client().get('/movies', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_404_get_movies(self):
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        res = self.client().get('/movies?page=1000000', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_movie(self):
        new_movie = {
            'title': 'Movie D',
            'release_date': '2021-05-25'
        }
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        res = self.client().post('/movies', json=new_movie,
                                 headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_400_create_movie(self):
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        res = self.client().post('/movies', headers=auth_header)  # no body
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_update_movies(self):
        updated_movie = {
            'release_date': '2030-05-25'
        }
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        movie = Movie.query.order_by(Movie.id).all()[0]
        res = self.client().patch(
            f'/movies/{movie.id}', json=updated_movie, headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_id'], movie.id)

    def test_404_update_invalid_movie(self):
        updated_movie = {
            'release_date': '2030-05-25'
        }
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        res = self.client().patch('/movies/1000000', json=updated_movie,
                                  headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_expired_token(self):
        auth_header = get_auth_header(EXPIRED_TOKEN)

        res = self.client().get('/movies', headers=auth_header)
        # desirialize, jsonify, and make it a dict
        # data: object of AuthError.error (dict)
        # {
        #     'code': 'token_expired',
        #     'description': 'Token expired.'
        # }
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "token_expired")

    def test_delete_movie(self):
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        movie = Movie.query.order_by(Movie.id).all()[0]
        res = self.client().delete(f'/movies/{movie.id}', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_invalid_movie(self):
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        res = self.client().delete('/movies/1000000', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Test create, read, update, delete actors.
    '''

    def test_get_actors(self):
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        res = self.client().get('/actors', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_404_get_actors(self):
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        res = self.client().get('/actors?page=1000000', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_actor(self):
        new_actor = {
            'name': 'Alice',
            'age': 25,
            'gender': 'F'
        }
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        res = self.client().post('/actors', json=new_actor,
                                 headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

    def test_400_create_actor(self):
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        res = self.client().post('/actors', headers=auth_header)  # no body
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_update_actors(self):
        updated_actor = {
            'age': 26
        }
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        actor = Actor.query.order_by(Actor.id).all()[0]
        res = self.client().patch(
            f'/actors/{actor.id}', json=updated_actor, headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_id'], actor.id)

    def test_404_update_invalid_actor(self):
        updated_actor = {
            'age': 26
        }
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        res = self.client().patch('/actors/1000000', json=updated_actor,
                                  headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        actor = Actor.query.order_by(Actor.id).all()[0]
        res = self.client().delete(f'/actors/{actor.id}', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_invalid_actor(self):
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        res = self.client().delete('/actors/1000000', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Tests for Casting Assistant role permissions
    '''

    def test_get_movies(self):
        auth_header = get_auth_header(CASTING_ASSISTANT_TOKEN)

        res = self.client().get('/movies', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_401_unauthorized_create_movie(self):
        new_movie = {
            'title': 'Movie D',
            'release_date': '2021-05-25'
        }
        auth_header = get_auth_header(CASTING_ASSISTANT_TOKEN)

        res = self.client().post('/movies', json=new_movie,
                                 headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unauthorized")

    def test_401_unauthorized_update_movies(self):
        updated_movie = {
            'release_date': '2030-05-25'
        }
        auth_header = get_auth_header(CASTING_ASSISTANT_TOKEN)

        movie = Movie.query.order_by(Movie.id).all()[0]
        res = self.client().patch(
            f'/movies/{movie.id}', json=updated_movie, headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unauthorized")

    def test_401_unauthorized_delete_movie(self):
        auth_header = get_auth_header(CASTING_ASSISTANT_TOKEN)

        movie = Movie.query.order_by(Movie.id).all()[0]
        res = self.client().delete(f'/movies/{movie.id}', headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], "unauthorized")


if __name__ == "__main__":
    unittest.main()
