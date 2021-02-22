import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Movie


CASTING_ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhIM1liU1Q3Qkt6aXF1NnF2X3pIXyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtaWFtLWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwYTY4Njg0NDFmZDYwMDcwODFjZDMxIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTM4Njg3MjMsImV4cCI6MTYxMzk1NTEyMywiYXpwIjoic1NHZVNFaWFxMTNISUdHSXg2UE5uNENqTkRNb0dDbGYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.TKd4M_8K-DgcKP_RRd3-R06A0vXFUYARLA22zxRoYCgTSTXE40NY483I-BICDVSeJabH_-wamtrGY2xO4ivsiyCm3kepYE6THqb69si3MXNrxIOHRfvcwj3YXIuWP7QCopthTcWIMJdY7Uc49wAl-OqEq_VmVef29sA6cXQMKQ71sp5cmRqm0S8Qvmz7nCmRKlOgU0O1IqjnSw3LZmiEtYYO9HD9fXF6ppTlDIPA_fNs0ImY202k_VXFiBI5gq5BRuM1k87Teub4cPZijY0oD3m34gRaVv7X_ccmwLuzsE6zOQeXzl2r5q0KWJTtfT2TOwgE-FK3D1WGzPHZcoqMfA'

EXECUTIVE_PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhIM1liU1Q3Qkt6aXF1NnF2X3pIXyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtaWFtLWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwMGY2YjIxNTIyMTgwMDZhM2M3NmU5IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTM5NTU1OTQsImV4cCI6MTYxNDA0MTk5NCwiYXpwIjoic1NHZVNFaWFxMTNISUdHSXg2UE5uNENqTkRNb0dDbGYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.RnWM5mptfbfGgoUVwlYNoYIAX891PDbTZ-RNxlwmHqBJZNUhmUWtWxw3T71C8KgBChqzkDHxXYEZ9ki1zb7-FEIypOQfO3y9YiofWZu7YC1JsBbbccxvYm-e0nuvjEGfzvUCPT2YG-eXtAhDtz1v7E56uxjEwhyPUHFuzAa4-XTdkzXIwGmoAklSHotPfPTR55z-cG8JrQMYWgHAQEGmOkc0fqQVgZhsREAwIQYfSh9ZY0dGkPwKkT7yO9fvb3uvgH6DG23sHEkynlnh6GjvJ7rfzAcixlI54khmJN4Jiv1ncKtDHDkvh4ktddMMZBGinYQhFTFn2tae8fpz09cqCw'

EXPIRED_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlhIM1liU1Q3Qkt6aXF1NnF2X3pIXyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtaWFtLWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAwMGY2YjIxNTIyMTgwMDZhM2M3NmU5IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2MTM4MDU4NzQsImV4cCI6MTYxMzgxMzA3NCwiYXpwIjoic1NHZVNFaWFxMTNISUdHSXg2UE5uNENqTkRNb0dDbGYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.GMhyhppfQeo8I47Y3oKaIIWpOHFA51xIMwjdF_D-EIFi40yxbzWKawfZJbpbLoSNA3ar3DM9SRh33AwNOvDXLrDmqEjo7nfmvxmUoWAHAV8pTDwjGo50oo-Xtd0br6pwMjU2A7PWqhRLBJt1k7jLnc9B_7cNzUu3zGkhzGoqOQ3XEMhHKKbU-5CGXvbftDVcZBYRJfQe_SIP9_0iRJS6S5g8KxesXWEVvLlIcvd3MRbJC3uk64m9UvW5cGVd9Piu-zfBR4cgsa3Wk0pxUAQvR_z1X3lFRbq-5ulqZDDkVAsu5L5GoEGFiwd5T_jcrEcilm3v5mKtpsVCai_DkbSwFw'


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

        res = self.client().patch('/movies/1000000', json=updated_movie, headers=auth_header)
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


if __name__ == "__main__":
    unittest.main()
