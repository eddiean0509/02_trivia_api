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
        # response = self.client().get('/categories')
        # self.assertEqual(response.status_code, 200)

        # data = json.loads(response.data)
        # self.assertEqual(len(data["categories"]), 6)
        # self.assertEqual(data["categories"]["4"], "History")
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['categories']), 0)

        for category in data['categories']:
            self.assertIsNotNone(category['id'])
            self.assertIsNotNone(category['type'])

    def test_list_questions(self):
        # response = self.client().get('/questions')
        # self.assertEqual(response.status_code, 200)

        # data = json.loads(response.data)
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['questions']), 0)

        for question in data['questions']:
            self.assertIsNotNone(question['id'])
            self.assertIsNotNone(question['question'])
            self.assertIsNotNone(question['answer'])
            self.assertIsNotNone(question['difficulty'])
            self.assertIsNotNone(question['category'])

    def test_delete_question(self):
        question_id = 1  # 삭제할 질문의 ID
        response = self.client().delete(f'/questions/{question_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNone(Question.query.get(question_id))

    def test_create_question(self):
        new_question = {
            'question': 'What is the capital city of France?',
            'answer': 'Paris',
            'difficulty': 2,
            'category': 3
        }
        initial_question_count = len(Question.query.all())  # 테스트 실행 전 질문 수

        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        final_question_count = len(Question.query.all())  # 테스트 실행 후 질문 수
        added_question = Question.query.get(data['question_id'])  # 추가된 질문

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question_id'])
        self.assertEqual(final_question_count, initial_question_count + 1)
        self.assertIsNotNone(added_question)
        self.assertEqual(added_question.question, new_question['question'])
        self.assertEqual(added_question.answer, new_question['answer'])
        self.assertEqual(added_question.difficulty, new_question['difficulty'])
        self.assertEqual(added_question.category, new_question['category'])

    def test_search_questions(self):
        search_term = 'title'  # 검색어
        response = self.client().post('/questions/search', json={'searchTerm': search_term})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['questions']), 0)

        for question in data['questions']:
            self.assertIn(search_term.lower(), question['question'].lower())

    def test_category_questions(self):
        category_id = 1  # 카테고리 ID
        response = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['questions']), 0)

        for question in data['questions']:
            self.assertEqual(question['category'], category_id)

    def test_quizzes(self):
        quiz_category = {'id': 1, 'type': 'Science'}  # 퀴즈 카테고리
        previous_questions = []  # 이전에 출제된 질문 ID 목록

        response = self.client().post('/quizzes', json={'quiz_category': quiz_category, 'previous_questions': previous_questions})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])
        self.assertNotIn(data['question']['id'], previous_questions)
        self.assertEqual(data['question']['category'], quiz_category['id'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

