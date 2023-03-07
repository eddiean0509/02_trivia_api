import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  CORS(app, resources={r"*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
      # response.headers.add("Access-Control-Allow-Origin", "*")
      # response.headers.add("Access-Control-Allow-Headers", "*")
      # response.headers.add("Access-Control-Allow-Methods", "*")
      # response.headers.add("Content-Type", "application/json")
      return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/categories", methods=["GET"])
  def available_categories():
      return jsonify({
          "categories": {
              category.id: category.type
              for category in Category.query
          },
      }), 200


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route("/questions", methods=["GET"])
  def list_questions():
      # args
      page = request.args.get("page", 1, type=int)
      per_page = request.args.get("per_page", 10, type=int)
      category_id = request.args.get("category_id", None, type=int)

      # question
      question_q = Question.query.order_by(Question.id.desc())

      # filter by category
      if category_id is not None:
          question_q = question_q.filter_by(category=category_id)

      # question pagination
      question_pagination = question_q.paginate(page=page, per_page=per_page)

      # categories
      categories = {c.id: c.type for c in Category.query}

      return jsonify({
          "questions": [q.format() for q in question_pagination.items],
          "total_questions": question_pagination.total,
          "categories": categories,
          "current_category": categories.get(category_id),
      }), 200


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route("/questions/<int:id>", methods=["DELETE"])
  def delete_question(id):
      question = Question.query.get_or_404(id)
      question.delete()

      return jsonify({ "id": id }), 200

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route("/questions", methods=["POST"])
  def create_question():
      data = request.get_json()
      question_args = (
          data.get("question"),
          data.get("answer"),
          data.get("category"),
          data.get("difficulty"),
      )

      if not all(question_args):
          abort(400)

      # create question
      Question(*question_args).insert()

      return jsonify({}), 200

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route("/questions/search", methods=["POST"])
  def search_questions():
      search_term = request.get_json().get("searchTerm")
      if search_term:
          questions = Question.query.filter(
              Question.question.ilike(f"%{search_term}%")
          ).all()
      else:
          questions = []

      return jsonify({
          "questions": [q.format() for q in questions],
          "total_questions": len(questions),
          "current_category": None,
      }), 200


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route("/categories/<int:id>/questions")
  def category_questions(id):
    # category with questions
    category = Category.query.options(
        SQLAlchemy().joinedload(Category.questions)
    ).get_or_404(id)

    return jsonify({
        "questions": [q.format() for q in category.questions],
        "total_questions": len(category.questions),
        "current_category": category.type,
    }), 200


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route("/quizzes", methods=["POST"])
  def quizzes():
      data = request.get_json()
      previous_questions = data.get("previous_questions")
      category_id = data.get("quiz_category", {}).get("id")

      if previous_questions is None or category_id is None:
          abort(400)

      question_q = Question.query.filter(
          Question.id.notin_(previous_questions),
      ).order_by(SQLAlchemy().func.random())

      # all category !=
      if category_id != 0:
          question_q = question_q.filter(Question.category==category_id)

      # question
      question = question_q.first()

      return jsonify({
          "question": question.format() if question else None,
      }), 200


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "message": "Resource Not Found"
      }), 404

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "message": "Bad Request"
      }), 400

  @app.errorhandler(422)
  def unprocessable_content(error):
      return jsonify({
          "message": "Unprocessable Content"
      }), 422
  
  return app

    
