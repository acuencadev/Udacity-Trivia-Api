# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
export DB_USERNAME=DB USER GOES HERE
export DB_PASSWORD=DB PASSWORD GOES HERE
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

Setting the `DB_USERNAME` and `DB_PASSWORD` to valid Postgres credentials allow the app to connect to the Database server.

## Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "Bad request"
}
```

## Endpoints

- GET '/api/categories'
- GET '/api/categories/<int:category>/questions'
- POST '/api/questions'
- POST '/api/questions/search'
- POST '/api/quizzes'
- DELETE '/api/questions/<int:question_id>'

**GET /api/categories**

- General:
  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  - Request Arguments: None
  - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
- Sample: `curl http://localhost:5000/api/categories`

```
{
    "success": True,
    "categories": {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    }
}
```

**GET /api/categories/id/questions**

- General:
  - Fetches a list of questions
  - Request Arguments: category id
  - Returns: An object with a success boolean, list of questions, total number of questions, and the current category. 
- Sample: `curl http://localhost:5000/api/categories/2/questions`

```
{
    "success": True,
    "questions": [
        {
            "id": 1,
            "question": "La Giaconda is better known as what?",
            "answer": "Mona Lisa",
            "difficulty": 3,
            "category": 2

        },
        ...
    ],
    "total_questions": 3,
    "current_category": 1
}
```

**POST /api/questions**

- General:
  - Creates a new question
  - Request Arguments: An JSON object containing the question, the answer, the difficulty and the category.
  - Returns: Whether or not the question was created.
- Sample: `curl http://localhost:5000/api/questions -X POST -H "Content-Type: application/json" -d '{"question": "Who am I?", "answer": "You are you", "difficulty": 5, "category": 1}'`

```
{
    "success": True
}
```

**POST /api/questions/search**

- General:
  - Search the database and look for questions that match the search term.
  - Request Arguments: Search term to look for.
  - Returns: List of qualifying questions.
- Sample: `curl http://localhost:5000/api/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "What"}'`

```
{
    "success": True,
    "questions": [
        {
            "id": 1,
            "question": "La Giaconda is better known as what?",
            "answer": "Mona Lisa",
            "difficulty": 3,
            "category": 2

        },
        ...
    ],
    "total_questions": 10,
    "current_category": 1
}
```

**POST /api/quiz**

- General:
  - Return a random question from the Database. It excludes previous questions and limit the search to the matching category.
  - Request Arguments: Quiz category and list of previous questions' ids.
  - Returns: Random question.
- Sample: `curl http://localhost:5000/api/quiz -X POST -H "Content-Type: application/json" -d '{"quiz_category": 1, "previous_questions": [1, 2, 3]}'`

```
{
    "success": True,
    "question": {
        "id": 1,
        "question": "La Giaconda is better known as what?",
        "answer": "Mona Lisa",
        "difficulty": 3,
        "category": 2
    }
}
```

**DELETE /api/questions/id**

- General:
  - Delete a question from the database.
  - Request Arguments: None.
  - Returns: Whether or not the question was deleted.
- Sample: `curl http://localhost:5000/api/questions/1 -X DELETE`

```
{
    "success": True
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```