import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Movie


CASTING_ASSISTANT_TOKEN = ''

EXECUTIVE_PRODUCER_TOKEN = ''


def get_auth_header(token):
    return {'Authorization': f'Bearer {token}'}


class TestCase(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgres://{}/{}".format(
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
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_404_get_movies(self):
        res = self.client().get('/movies?page=1000000')
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

        res = self.client().post('/movies', json=new_movie, headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

        # Delete the row just created.
        created_id = data['created']
        Movie.query.filter(Movie.id == created_id).one_or_none().delete()

    def test_400_create_movie(self):
        res = self.client().post('/movies')  # no body
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


if __name__ == "__main__":
    unittest.main()
