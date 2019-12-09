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
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## API Reference

### Endpoints

#### GET /categories
- General:
    - Returns a dictionary of categories.
    - Request Argument: ```None```
- Sample: ```curl localhost:5000/categories```
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

#### GET /questions
- Genreal:
    - Returns a dictionary of questions, categories, total number of questions, and current categories.
    - Results are painated in groups of 2. Include a request argument to choose page number, starting from 1.
    - Request Argument: ```page```
- Sample:
    - ```curl localhost:5000/questions``` (without request argument)
    - ```curl localhost:5000/questions?page=1```(with request argument)
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": [
    "Entertainment", 
    "History", 
    "Sports", 
    "Geography", 
    "Art", 
    "Science"
  ], 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "total_questions": 19
}
```

#### DELETE /questions/{question_id}
- General:
    - Deletes the specified question based on given id. Returns the success value.
- Sample: ```curl -X DELETE localhost:5000/questions/2```
```
{
  "success": true
}
```

#### POST /questions
- General:
    - If ```searchTerm``` provided in POST request. Returns the questions which match the ```searchTerm``` value, current category and total number of questions.
    - If ```searchTerm``` not provided. Creates a new question using the the submitted question, answer, category and difficulty. Returns the success value.
- Sample:
    - ```curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "boxer"}' localhost:5000/questions```(provide searchTerm)
        ```
        {
          "current_category": [
              "History"
            ], 
          "questions": [
              {
              "answer": "Muhammad Ali", 
              "category": 4, 
              "difficulty": 1, 
              "id": 9, 
              "question": "What boxer's original name is Cassius Clay?"
              }
            ], 
          "total_questions": 1
        }
        ```
    - ```curl -X POST -H "Content-Type: application/json" -d '{"question": "Who was the first president of the USA?", "answer": "George Washington", "category": 4, "difficulty": 1}' localhost:5000/questions```
        ```
        {
            "success": true
        }

        ```

#### GET /categories/{category_id}/questions
- General:
  - Returns questions based on category, current category and total number of questions.
- Sample:```curl localhost:5000/categories/1/questions```
```
{
  "current_category": [
    "Science"
  ], 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }
  ], 
  "total_questions": 3
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