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

  CORS(app, resources={r"*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add("Access-Control-Allow-Origin", "*")
      response.headers.add("Access-Control-Allow-Headers", "*")
      response.headers.add("Access-Control-Allow-Methods", "*")
      response.headers.add("Content-Type", "application/json")
      return response

  @app.route("/categories", methods=["GET"])
  def available_categories():
      return jsonify({
          "categories": {
              category.id: category.type
              for category in Category.query
          },
      }), 200


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


  @app.route("/questions/<int:id>", methods=["DELETE"])
  def delete_question(id):
      question = Question.query.get_or_404(id)
      question.delete()

      return jsonify({ "id": id }), 200

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

    
