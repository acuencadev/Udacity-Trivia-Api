import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, with_credentials=True, resources={
    r'/api/*': {'origins': "*"}
  })

  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
    response.headers.add('Access-Control-Allow-Methods', "GET, POST, PATCH, DELETE, OPTIONS")
    response.headers.add('Access-Control-Allow-Credentials', "true")
    
    return response

  '''
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/api/categories', methods=['GET'])
  def get_all_categories():
    categories = Category.query.all()
    formatted_categories = { category.id : category.type for category in categories }
    
    return jsonify({
      'success': True,
      'categories': formatted_categories
    })

  '''
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/api/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
    
    categories = Category.query.all()
    formatted_categories = { category.id : category.type for category in categories }
    
    return jsonify({
      'success': True,
      'questions': formatted_questions[start:end],
      'total_questions': len(formatted_questions),
      'categories': formatted_categories,
      'current_category': 0
    })

  '''
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.get(question_id)
    
    if not question:
      abort(404)
    
    question.delete()
    
    return jsonify({
      'success': True
    })

  '''
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/api/questions', methods=['POST'])
  def create_question():
    data = request.get_json()
    
    try:
      question = data['question']
      answer = data['answer']
      difficulty = data['difficulty']
      category = data['category']
    except KeyError:
      abort(422)
    
    new_question = Question(question=question, answer=answer,
                            difficulty=difficulty, category=category)
    
    new_question.insert()
    
    return jsonify({
      'success': True
    })

  '''
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/api/questions/search', methods=['POST'])
  def search_questions():
    data = request.get_json()
    search_term = data['searchTerm']
    
    questions = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
    formatted_questions = [question.format() for question in questions]
    
    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions': len(formatted_questions),
      'current_category': 0
    })

  '''
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/api/categories/<int:category>/questions', methods=['GET'])
  def get_questions_by_category(category):
    questions = Question.query.filter(Question.category==str(category)).all()
    formatted_questions = [question.format() for question in questions]
    
    return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions': len(formatted_questions),
      'current_category': category
    })


  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/api/quizzes', methods=['POST'])
  def get_next_question():
    data = request.get_json()
    
    try:
      previous_questions = data['previous_questions']
      quiz_category = data['quiz_category']
    except KeyError:
      abort(422)

    questions_filter = Question.query
    
    if quiz_category['id'] != 0:
      questions_filter.filter_by(category=quiz_category['type'])
      
    if len(previous_questions) > 0:
      questions_filter.filter(Question.id.notin_(previous_questions))

    questions = questions_filter.all()
    random_question = random.choice(questions)
    formatted_question = random_question.format()
    
    return jsonify({
      'success': True,
      'question': formatted_question
    })

  '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def internal_error(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': "Bad request"
    }), 400
    
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': "Not found"
    }), 404
    
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': "Unprocessable"
    }), 422
    
  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': "Internal Error"
    }), 500
  
  return app

    