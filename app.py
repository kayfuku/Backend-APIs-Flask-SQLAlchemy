import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, db_drop_and_create_all, Movie


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
    print(greeting)

    return jsonify({
        'success': True,
        'greeting': greeting
    })


PER_PAGE = 10


def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    return selection[start:end]


@app.route('/movies', methods=['GET'])
def get_movies():
    selection = Movie.query.order_by(Movie.id).all()
    current_movies = [movie.get_dict()
                      for movie in paginate(request, selection)]
    if len(current_movies) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'movies': current_movies,
        'total_movies': len(selection)
    })


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


# local
if __name__ == '__main__':
    app.run(debug=True)

# #
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)
