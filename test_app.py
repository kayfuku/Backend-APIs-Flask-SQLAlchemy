import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Movie


CASTING_ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhIM1liU1Q3Qkt6aXF1NnF2X3pIXyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtaWFtLWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwYTY4Njg0NDFmZDYwMDcwODFjZDMxIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTM4MDU1MjAsImV4cCI6MTYxMzgxMjcyMCwiYXpwIjoic1NHZVNFaWFxMTNISUdHSXg2UE5uNENqTkRNb0dDbGYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.i72_E6WzhbWEj6A3jxDb0iM0X8-ndV03hVD3xT8YevW3aWFDYnLVqOthPBqna0Zdzl_QaqKAtGQ7Eehk3ff0DkCNkWV4_hbESSJ8CNMDelgTGEtYFsdNKx6YSeEsnxVwPHFyTMslZ_X8QBtvyg6Ie-8xhd2d38tWAtZezcxZu4XE3zblGF2Fs8lMkipVxwkEGrgfcyUM_7dn0ajgj6fyeVjCY58T-Iv_he0YrAbTr-9onTKDfoy_8Y8LNAkaCauqFnOynysSl9c8wra_8M_eUZQZFURMJk3RGWwCvpGxgK4wyyZKMousmQ84h6rQJBdVjfhsDospRF6poHWB-w5ifA'

EXECUTIVE_PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhIM1liU1Q3Qkt6aXF1NnF2X3pIXyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtaWFtLWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwMGY2YjIxNTIyMTgwMDZhM2M3NmU5IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTM4MDU4NzQsImV4cCI6MTYxMzgxMzA3NCwiYXpwIjoic1NHZVNFaWFxMTNISUdHSXg2UE5uNENqTkRNb0dDbGYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.GMhyhppfQeo8I47Y3oKaIIWpOHFA51xIMwjdF_D-EIFi40yxbzWKawfZJbpbLoSNA3ar3DM9SRh33AwNOvDXLrDmqEjo7nfmvxmUoWAHAV8pTDwjGo50oo-Xtd0br6pwMjU2A7PWqhRLBJt1k7jLnc9B_7cNzUu3zGkhzGoqOQ3XEMhHKKbU-5CGXvbftDVcZBYRJfQe_SIP9_0iRJS6S5g8KxesXWEVvLlIcvd3MRbJC3uk64m9UvW5cGVd9Piu-zfBR4cgsa3Wk0pxUAQvR_z1X3lFRbq-5ulqZDDkVAsu5L5GoEGFiwd5T_jcrEcilm3v5mKtpsVCai_DkbSwFw'


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

        res = self.client().post('/movies', json=new_movie, headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

        # Delete the row just created.
        created_id = data['created']
        Movie.query.filter(Movie.id == created_id).one_or_none().delete()

    def test_400_create_movie(self):
        auth_header = get_auth_header(EXECUTIVE_PRODUCER_TOKEN)

        res = self.client().post('/movies', headers=auth_header)  # no body
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


if __name__ == "__main__":
    unittest.main()
