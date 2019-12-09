import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertLessEqual(len(data['questions']), 10)
        self.assertTrue(data)

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)
        self.assertTrue(data['success'])

    def test_create_question(self):
        res = self.client().post('/questions', json={'question': 'Who was the first president of the USA?',
                                                     'answer': 'George Washington',
                                                     'category': 4,
                                                     'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)
        self.assertTrue(data['success'])
    
    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': 'boxer'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)
        self.assertLessEqual(len(data['questions']), 10)
        self.assertIn('boxer', data['questions'][0]['question'])

    def test_get_questions_based_on_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data)
        self.assertLessEqual(len(data['questions']), 10)

    def test_404_if_questions_does_not_exist(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "The requested resource doesn't exist.")

    def test_405_if_methods_not_allowed(self):
        res = self.client().get('questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'method not allowed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
