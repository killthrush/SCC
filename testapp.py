"""
Module that hosts a Flask API for Questions.
"""

from flask import Flask
from flask import Response
from flask import request
from flask import abort
import questions as q
import testapphelper as h
import access_control as ac

app = Flask(__name__)

# Keep questions in memory. This doesn't look thread-safe...
repository = q.SimpleQuestionRepository()

def initialize():
    """
    Runs code when the test application starts.
    """
    app.debug = True # allow stack traces for development
    repository.load_state_from_file('./question_state.csv')


@app.route('/questions/<id_numbers>/', methods=['GET'])
@ac.crossdomain(origin='*')
def get_some_questions(id_numbers):
    """
    Returns questions matching the given IDs in JSON format (the default), or in csv format.
    """
    invalid_pagination = (h.has_pagination_args(request.args) and not h.pagination_args_are_valid(request.args))
    if not h.is_valid_id_list(id_numbers) or invalid_pagination:
        abort(400)

    questions = h.invoke_get_with_filters(repository, request.args, id_numbers)
    return h.format_question_response(questions, request.args)


@app.route('/questions/', methods=['GET'])
def get_all_questions():
    """
    Returns all available questions in JSON format (the default), or in csv format.
    """
    if h.has_pagination_args(request.args) and not h.pagination_args_are_valid(request.args):
        abort(400)

    questions = h.invoke_get_with_filters(repository, request.args)
    return h.format_question_response(questions, request.args)


@app.route('/questions/', methods=['POST'])
def create_question():
    """
    Allows creation of a new question, given a JSON payload.
    Returns the new questions (with IDs) on success.
    """
    question = q.Question()
    if not question.try_set_from_json(request.json):
        abort(400)
    new_question = repository.create(question)
    return Response(new_question.to_json(), mimetype='application/json'), 201


@app.route('/questions/<id_number>/', methods=['PUT'])
def edit_question(id_number):
    """
    Changes the data for a question given an ID and a JSON payload.  Returns the edited
    question on success.
    """
    if not h.is_valid_int(id_number):
        abort(400)
    question = repository.get_by_id(id_number)
    if question == None:
        abort(404)
    if 'id_number' in request.json and request.json['id_number'] != int(id_number):
        abort(400)
    if not question.try_set_from_json(request.json):
        abort(400)
    return_question = repository.change(question)
    return Response(return_question.to_json(), mimetype='application/json')


@app.route('/questions/<id_number>/', methods=['DELETE'])
def remove_question(id_number):
    """
    Removes the given question from the repository.
    """
    if not h.is_valid_int(id_number):
        abort(400)
    question = repository.get_by_id(id_number)
    if question == None:
        abort(404)
    repository.remove(question)
    return '', 204



if __name__ == '__main__':
    initialize()
    app.run()
