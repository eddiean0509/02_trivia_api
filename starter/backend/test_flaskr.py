import os
import unittest
import json
from flask import Response
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

DATABASE_NAME = "trivia_test"
DATABASE_PATH = "postgresql://postgres:postgres@127.0.0.1:5432/trivia_test"


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # load test data
        os.system(f'psql "{DATABASE_PATH}" {DATABASE_NAME} -c "DROP TABLE questions, categories;"')
        os.system(f'psql "{DATABASE_PATH}" {DATABASE_NAME} < ./trivia.psql')

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DATABASE_NAME
        self.database_path = DATABASE_PATH
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

    def test_available_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', data)

    def test_list_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('questions', data)


    def test_delete_question(self):
        question = Question.query.first()
        response = self.client().delete(f'/questions/{question.id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

    def test_create_question(self):
        new_question = {
            'question': 'What is the capital of Italy?',
            'answer': 'Rome',
            'category': 3,
            'difficulty': 2
        }
        response = self.client().post('/questions', json=new_question)
        #data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

        questions = Question.query.filter(Question.question == new_question['question']).all()
        self.assertGreater(len(questions), 0)

    def test_search_questions(self):
        search_term = 'title'
        response = self.client().post('/questions/search', json={'searchTerm': search_term})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data['questions'], list)

        for question in data['questions']:
            self.assertIn(search_term.lower(), question['question'].lower())

    def test_category_questions(self):
        category_id = 1
        response = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data['questions'], list)
        self.assertGreater(len(data['questions']), 0)

        for question in data['questions']:
            self.assertEqual(question['category'], category_id)

    def test_quizzes(self):
        previous_questions = [1, 2]
        quiz_data = {
            'quiz_category': {'type': 'click', 'id': 0},
            'previous_questions': previous_questions
        }
        response = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data['question'])
        self.assertNotIn(data['question']['id'], previous_questions)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

