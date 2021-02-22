import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, db_drop_and_create_all, Movie
from auth import AuthError, requires_auth, AUTH0_DOMAIN, ALGORITHMS, API_AUDIENCE, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL

# True: development, False: production
is_dev = False


def create_app(test_config=None):
    # create and configure the app
    flask_app = Flask(__name__)
    setup_db(flask_app)
    CORS(flask_app)
    # Uncomment the following line to initialize the datbase
    # !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    # !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    # db_drop_and_create_all()

    return flask_app


app = create_app()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origions', '*')  # ?
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, POST, PATCH, DELETE, OPTIONS')
    return response


@app.route('/')
def get_greeting():
    greeting = "Hello"

    return jsonify({
        'success': True,
        'greeting': greeting
    })


@app.route("/login", methods=["GET"])
def generate_login_url():
    login_url = f'https://{AUTH0_DOMAIN}/authorize' \
        f'?audience={API_AUDIENCE}' \
        f'&response_type=token&client_id=' \
        f'{AUTH0_CLIENT_ID}&redirect_uri=' \
        f'{AUTH0_CALLBACK_URL}'

    print('login url:', login_url)

    return jsonify({
        'login_url': login_url
    })


MOVIES_PER_PAGE = 10
ACTORS_PER_PAGE = 10


def paginate(items, max_per_page):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * max_per_page
    end = start + max_per_page
    return items[start:end]


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(jwt):
    selection = Movie.query.order_by(Movie.id).all()
    current_movies = [movie.get_dict()
                      for movie in paginate(selection, MOVIES_PER_PAGE)]
    if len(current_movies) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'movies': current_movies,
        'total_movies': len(selection)
    })


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(jwt):
    body = request.get_json()
    if body is None:
        abort(400)

    try:
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        movie = Movie(
            title=new_title,
            release_date=new_release_date
        )
        movie.insert()

        selection = Movie.query.order_by(Movie.id).all()
        current_movies = [movie.get_dict()
                          for movie in paginate(selection, MOVIES_PER_PAGE)]

        return jsonify({
            'success': True,
            'created': movie.id,
            'movies': current_movies,
            'total_movies': len(Movie.query.all())
        })

    except Exception as ex:
        db.session.rollback()
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(jwt, movie_id):
    body = request.get_json()

    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        return jsonify({
            'success': False,
            'error': 'Movie id ' + str(movie_id) + ' not found to be edited.'
        }), 404

    else:
        try:
            new_title = body.get('title', None)
            new_release_date = body.get('release_date', None)

            movie.title = new_title or movie.title
            movie.release_date = json.dumps(
                new_release_date) or movie.release_date

            movie.update()

            return jsonify({
                'success': True,
                'updated_id': movie.id,
                'updated_movie': movie.get_dict()
            })

        except Exception as ex:
            db.session.rollback()
            abort(422)


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(jwt, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        return jsonify({
            'success': False,
            'error': 'Movie id ' + str(movie_id) + ' not found to be deleted.'
        }), 404

    else:
        try:
            movie.delete()

            return jsonify({
                'success': True,
                'deleted_id': movie_id
            })

        except Exception as ex:
            db.session.rollback()
            print(ex)
            abort(422)


'''
Error handler
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500


@app.errorhandler(AuthError)
def process_AuthError(error):
    response = jsonify(error.error)
    response.status_code = error.status_code

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=is_dev)
