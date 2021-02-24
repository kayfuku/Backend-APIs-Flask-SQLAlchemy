# Backend APIs example using Flask, SQLAlchemy 
  
## Overview  
The purpose of this project is to learn about how to build database-backed APIs and web applications, including REST APIs, schema design, database migrations, Object-Relational Mapping (ORM), API testing, authentication and authorization with Json Web Token (JWT) and asymmetric encryption through Auth0, and server deployment on Heroku.  
  
  
## Application Stack  
Flask is a simple but versatile web application framework, which is a good starting point for learning backend APIs. This appication only has a backend code. [Python 3](https://www.python.org/downloads/) is required.  

- **Framework**: [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- **Deployment**: [Heroku](https://www.heroku.com/)
  
  
## Run server locally  

1. **Install Dependencies**  
    ```
    pip3 install -r requirements.txt
    ```
  
2. **Create Local Database**  
    Create a local database and set the database URI to the environment variable `DATABASE_URL` in `setup.sh`.
  
3. **Export Environment Variables**  
    ```
    source setup.sh
    ```
  
4. **Run Database Migrations**  
    ```
    python manage.py db init  # only needed once at the beginning
    python manage.py db migrate
    python manage.py db upgrade
    ```
  
5. **Run the Flask Application locally**  
    On Linux (macOS)  
    ```
    export FLASK_APP=app.py
    ```  
    On Windows
    ```
    set FLASK_APP=app.py
    ```  
    then, 
    ```
    flask run --reload
    ```
  
  
## Roles and Permissions  
The application has two roles:  
  
1. **Casting Assistant**
    - Can view all movies and actors in the database

2. **Executive Producer**
    - Has all the permissions of Casting Assistant
    - Can create a new movie and a new actor
    - Can update a movie and an actor
    - Can delete a movie and an actor
  
  
## Testing server locally  
```test_app.py``` has test cases for expected success and error behavior for each endpoint using the unittest library.  

1. **Export Environment Variables**  
    ```
    source setup.sh
    ```  
  
2. **Run the test**  
    ```
    python3 test_app.py
    ```  
  
  
## Testing server on Heroku  
**[Postman](https://www.postman.com/)** is used for testing. The application server has been up and running on Heroku and the tokens have already been set in the postman collection and will expire at around 2/23 9:10 pm (PST).  
  
API endpoint root URL: `https://full-stack-web-app-4.herokuapp.com/`
  
1. Import [the file](udacity-fsnd-capstone.postman_collection.json) into Postman to run the tests.

2. Adjust the values of the host name and the tokens for your own. (Already set)

3. Run the collection.  
  
  
## API Reference  
  
### Getting Started
- The app is hosted at `https://full-stack-web-app-4.herokuapp.com/`. 
- Authentication and authorizatioon: This application requires a Casting Assistant or Executive Producer role described above.  

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 401: Unauthorized

### Endpoints  
#### GET /movies?page=<page_number>
- General:
    - Returns a list of movies, success value, and the total number of movies. 
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl "http://127.0.0.1:8080/movies?page=1"`

``` 
{
    "movies": [
        {
            "id": 25,
            "release_date": "05/25/2030",
            "title": "Movie D"
        },
        {
            "id": 27,
            "release_date": "05/25/2021",
            "title": "Movie D"
        },
        
        ...
        
        {
            "id": 29,
            "release_date": "05/25/2021",
            "title": "Movie D"
        }
    ],
    "success": true,
    "total_movies": 4
}
```

#### GET /actors?page=<page_number>
- General:
    - Returns a list of actors, success value, and the total number of actors. 
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl "http://127.0.0.1:8080/actors?page=1"`

```
{
    "actors": [
        {
            "age": 26,
            "gender": "F",
            "id": 11,
            "name": "Alice"
        },
        {
            "age": 25,
            "gender": "F",
            "id": 12,
            "name": "Alice"
        }
    ],
    "success": true,
    "total_actors": 2
}
```

#### POST /movies
- General:
    - Creates a new movie using the submitted title and release date. Returns the id of the created movie, success value, total number of movies, and movie list based on current page number. 
- Sample: `curl -X POST "http://127.0.0.1:8080/movies" -H "Content-Type: application/json" -d '{"title":"Movie D", "release_date":"2021-05-25"}'`

```
{
    "created": 30,
    "movies": [
        {
            "id": 25,
            "release_date": "05/25/2030",
            "title": "Movie D"
        },
        {
            "id": 27,
            "release_date": "05/25/2021",
            "title": "Movie D"
        },
        
        ...
        
        {
            "id": 30,
            "release_date": "05/25/2021",
            "title": "Movie D"
        }
    ],
    "success": true,
    "total_movies": 5
}
```  

#### PATCH /movies/<movie_id>
- General:  
    - Updates the movie of the given ID if it exists. Returns the id of the updated movie, success value, total number of movies, and movie list based on the current page number.  
    - Request argument: movie id to be updated
- Sample: `curl -X PATCH "http://127.0.0.1:8080/movies/25" -H "Content-Type: application/json" -d '{"release_date":"2004-05-25"}'`

```  
{
    "success": true,
    "updated_id": 25,
    "updated_movie": {
        "id": 25,
        "release_date": "05/25/2004",
        "title": "Movie D"
    }
}
```  

#### DELETE /movies/<movie_id>
- General:  
    - Deletes the movie of the given ID if it exists. Returns the id of the deleted movie and success value.  
    - Request argument: movie id to be deleted
- Sample: `curl -X DELETE "http://127.0.0.1:8080/movies/27"`

```
{
    "deleted_id": 27,
    "success": true
}
```    
  
  
## Authors
kei (kayfuku) + Udacity

## Acknowledgements 
The awesome team at Udacity and peer students!  




