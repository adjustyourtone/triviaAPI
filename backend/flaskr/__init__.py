import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_ques(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return 'Welcome to the Trivia API'

  #   '''
  # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs - Done
  # '''

  #   '''
  # @TODO: Use the after_request decorator to set Access-Control-Allow
  # ''' - Done

  #   '''
  # @TODO:
  # Create an endpoint to handle GET requests
  # for all available categories. - Done
  # '''
    @app.route('/categories')
    def get_categories():
        # query the DB for all categories
        categories = Category.query.all()
        # format categories
        formated_categories = [category.format() for category in categories]

        # return in JSON w/success and formated list
        return jsonify({
            'success': True,
            'categories': formated_categories
        })

  #   '''
  # @TODO:
  # Create an endpoint to handle GET requests for questions,
  # including pagination (every 10 questions).
  # This endpoint should return a list of questions,
  # number of total questions, current category, categories.

  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions.
  # ''' - Done
    @app.route('/questions')
    def retrieve_questions():
        selection = Question.query.all()
        current_questions = paginate_ques(request, selection)

        categories = Category.query.all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {category.id: category.type for category in categories},
            'current_category': None
        })
  #   '''
  # @TODO:
  # Create an endpoint to DELETE question using a question ID.

  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page.
  # ''' - Done
    @app.route('/questions/<int:questions_id>', methods=['DELETE'])
    def delete_question(questions_id):
        # run a try/except with query/by question_id. Use ORM to delete
        try:
            question = Question.query.get(questions_id)

            if question is None:
                abort(404)

            # just call delete. After delete app calls getQuestions() automatically.
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)

  #   '''
  # @TODO:
  # Create an endpoint to POST a new question,
  # which will require the question and answer text,
  # category, and difficulty score.

  # TEST: When you submit a question on the "Add" tab,
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.
  # ''' - done
    # question form returns json of: question, answer, difficulty, category
    @app.route('/questions', methods=["POST"])
    def create_question():
        try:
            body = request.get_json()

            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_question_category = body.get('category', None)
            new_question_difficulty = body.get('difficulty', None)

            question = Question(question=new_question, answer=new_answer,
                                category=new_question_category, difficulty=new_question_difficulty)
            question.insert()
            return jsonify({
                "success": True
            })
        except:
            abort(404)
  #   '''
  # @TODO:
  # Create a POST endpoint to get questions based on a search term.
  # It should return any questions for whom the search term
  # is a substring of the question.

  # TEST: Search by any phrase. The questions list will update to include
  # only question that include that string within their question.
  # Try using the word "title" to start.
  # ''' - done

    @app.route('/search/questions', methods=["POST"])
    def search_question():
        try:
            content = request.get_json()

            searchTerm = content.get('searchTerm', '')

            if (searchTerm is None or searchTerm == ''):
                abort(400)

            search = "%{}%".format(searchTerm)

            questions = Question.query.all()

            questions_found = Question.query.filter(
                Question.question.ilike(search))

            questions_found_format = [question.format()
                                      for question in questions_found]

            return jsonify({
                "success": True,
                "total_questions": len(questions),
                "questions": questions_found_format,
                "current_category": None
            })
        except:
            abort(400)
    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/categories/<int:category_id>/questions')
    def list_by_category(category_id):
        try:
            questions = Question.query.filter_by(
                category=str(category_id)).all()
            formatted_questions = [question.format() for question in questions]
            total_questions = len(formatted_questions)
            return jsonify({
                'questions': formatted_questions,
                'total_questions': total_questions,
            })
        except:
            abort(400)

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

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
