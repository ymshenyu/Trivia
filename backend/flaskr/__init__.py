import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def categories_dict():
    categories = Category.query.all()
    categories_dict = {}
    for category in categories:
        categories_dict[category.id] = category.type
    return categories_dict


def pagination_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = selection
    formatted_questions = [question.format() for question in questions]
    return formatted_questions[start:end]


def current_category(selection):
    categories = []
    for question in selection:
        category = Category.query.filter(
            Category.id == question.category).one_or_none()
        category_type = category.type
        if category_type not in categories:
            categories.append(category_type)
    return categories


def quiz_question(selection, previous_questions):
    for question in selection:
        if question.id not in previous_questions:
            formatted_question = question.format()
            break
        else:
            formatted_question = None
    return formatted_question


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/categories')
    def get_all_categories():
        try:
            return jsonify({
                'categories': categories_dict()
            })
        except Exception:
            abort(404)

    @app.route('/questions')
    def get_all_questions():
        selection = Question.query.order_by(Question.id).all()
        formatted_questions = pagination_questions(request, selection)

        if not len(formatted_questions):
            abort(404)

        return jsonify({
            'questions': formatted_questions,
            'total_questions': len(selection),
            'categories': categories_dict(),
            'current_category': current_category(selection)
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            question.delete()
            return jsonify({'success': True})
        except Exception:
            abort(404)

    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        if 'searchTerm' in data:
            # search questions based on search term
            selection = Question.query.filter(Question.question.ilike(
                f"%{data['searchTerm']}%")).order_by(Question.id).all()
            formatted_questions = pagination_questions(request, selection)

            if not len(formatted_questions):
                abort(404)

            return jsonify({
                'questions': formatted_questions,
                'total_questions': len(selection),
                'current_category': current_category(selection)
            })
        else:
            try:
                question = Question(question=data['question'],
                                    answer=data['answer'],
                                    category=data['category'],
                                    difficulty=data['difficulty'])
                question.insert()
                return jsonify({'success': True})
            except Exception:
                abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions(category_id):
        selection = Question.query.filter(
            Question.category == str(category_id)).all()
        formatted_questions = pagination_questions(request, selection)

        if not len(formatted_questions):
            abort(404)

        return jsonify({
            'questions': formatted_questions,
            'total_questions': len(selection),
            'current_category': current_category(selection)
        })

    @app.route('/quizzes', methods=['POST'])
    def quiz():
        try:
            data = request.get_json()
            previous_questions = data['previous_questions']
            force_end = False
            if data['quiz_category']['id'] == 0:
                selection = Question.query.order_by(func.random()).all()
                formatted_question = quiz_question(
                    selection, previous_questions)
            else:
                selection = (Question.query.filter(
                    Question.category == data['quiz_category']['id'])
                    .order_by(func.random()).all())
                formatted_question = quiz_question(
                    selection, previous_questions)

            if formatted_question is None:
                # end the game if it doesn't have more question
                force_end = True

            return jsonify({
                'question': formatted_question,
                'forceEnd': force_end
            })
        except Exception:
            abort(404)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'code': 404,
            'success': False,
            'message': "The requested resource doesn't exist."
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'code': 422,
            'success': False,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'code': 405,
            'success': False,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'code': 500,
            'success': False,
            'message': 'internal server error'
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'code': 400,
            'success': False,
            'message': 'bad request'
        }), 400

    return app
