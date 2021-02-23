# Rest API Study

## Overview  
  
The purpose of this project is to learn about how to build database-backed APIs and web applications, including REST APIs, schema design, database migrations, Object-Relational Mapping (ORM), API testing, authentication and authorization with Json Web Token (JWT) and asymmetric encryption through Auth0, and server deployment on Heroku.  

## Application Stack  
This appication only has a backend code. [Python 3](https://www.python.org/downloads/) is required.  

- **Framework**: [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- **Deployment**: [Heroku](https://www.heroku.com/){:target="_blank" rel="noopener"}


#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

Key Dependencies:  

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

#### Database Setup  

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
createdb trivia
psql trivia < trivia.psql
```

Also, set the database name to ```trivia```, on line 6 in models.py.  

#### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 



## Tests  

In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

The database name is already set to ```trivia_test``` on line 17 in test_flaskr.py. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

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

### Endpoints  
#### GET /categories
- General:
    - Returns a list of categories, and success value. 
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl "http://127.0.0.1:5000/categories"`

``` {
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "success": true
}
```

#### GET /questions?page=<page_number>
- General:
    - Returns a list of questions, success value, total number of the questions, current category, and all categories. 
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl "http://127.0.0.1:5000/questions?page=1"`

```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "current_category": [], 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },  
    
    ...,  
    
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 22
}
```

#### DELETE /questions/<question_id>
- General:  
    - Deletes the qustion of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and question list based on current page number to update the frontend. 
    - Request argument: question id to be deleted
- Sample: `curl -X DELETE "http://127.0.0.1:5000/questions/1"`

```
{
  "deleted": 26, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
        
    ...,  
  
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 21
}
```

#### POST /questions
- General:
    - Creates a new question using the submitted statement, answer, difficulty and category. Returns the id of the created question, success value, total questions, and question list based on current page number to update the frontend. 
- Sample: `curl -X POST "http://127.0.0.1:5000/questions" -H "Content-Type: application/json" -d '{"question":"q3", "answer":"a3", "difficulty":"1", "category":"1"}'`

```
{
  "created": 28, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
        
    ...,  
  
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 22
}
```  

#### GET /categories/<category_id>/questions  
- General:
    - Returns a list of questions in the given category, success value, total number of questions, and current category. 
    - Request argument: category id to be chosen
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl "http://127.0.0.1:5000/categories/1/questions"`

```
{
  "current_category": {
    "id": 1, 
    "type": "Science"
  }, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    
    ...,  
    
    {
      "answer": "a3", 
      "category": 1, 
      "difficulty": 1, 
      "id": 28, 
      "question": "q3"
    }
  ], 
  "success": true, 
  "total_questions": 5
}
```

#### POST /quizzes
- General:
    - Takes quiz category and previous questions parameters and returns a random question within the given category, if provided, and that is not one of the previous questions.  

- Sample: `curl -X POST "http://127.0.0.1:5000/quizzes" -H "Content-Type: application/json" -d '{"quiz_category":{"id": 1, "type": "Science"}, "previous_questions": []}'`

```
{
  "question": {
    "answer": "a1", 
    "category": 1, 
    "difficulty": 1, 
    "id": 24, 
    "question": "q1"
  }, 
  "success": true
}
```
  

## Authors
kei (kayfuku) + Udacity

## Acknowledgements 
The awesome team at Udacity and peer students!  




