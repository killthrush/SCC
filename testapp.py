"""
Module that hosts a Flask API for Questions.
"""

from flask import Flask
from flask import Response
from flask import request
from flask import abort
import questions as q
import testapphelper as h

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
def get_some_questions(id_numbers):
    """
    Returns questions matching the given IDs in JSON format (the default), or in csv format.
        Allowed parameters:
            * fmt: set to 'csv' to return the questions in pipe-delimited format
            * start: set to the ordinal number of the first question to return.
                Must appear with num.
            * num: set to the total number of questions to return.  Must appear with start.
            * qf: set to a string; if the question text contains this string, it will be returned.
                Conjunctive with 'af' and 'df' filters.
            * af: set to a string; if the answer text contains this string, it will be returned.
                Conjunctive with 'qf' and 'df' filters.
            * df: set to a string; if the text of any of the distractors contains this string,
                it will be returned.  Conjunctive with 'af' and 'qf' filters.
            * sk: set to one of the following to set the sorting key for questions:
                * 'i': sort by id_number (the default)
                * 'q': sort by question text
                * 'a': sort by answer text
                * 'd': sort by the number of distractors
            * sd: set to one of the following to set the sorting direction for questions:
                * 'a': sort ascending (the default)
                * 'd': sort descending
        Returns status 200 along with the formatted question data on success.
        Returns status 400 if the ID list is malformed or if pagination arguments (start, num)
            are supplied but are invalid.
        Returns status 500 on application error.
    """
    invalid_pagination = (h.has_pagination_args(request) and not h.pagination_args_are_valid(request))
    if not h.is_valid_id_list(id_numbers) or invalid_pagination:
        abort(400)

    questions = invoke_get_with_filters(repository, request.args, id_numbers)
    return h.format_question_response(questions, request.args)


@app.route('/questions/', methods=['GET'])
def get_all_questions():
    """
    Returns all available questions in JSON format (the default), or in csv format.
        Allowed parameters:
            * fmt: set to 'csv' to return the questions in pipe-delimited format
            * start: set to the ordinal number of the first question to return.
                Must appear with num.
            * num: set to the total number of questions to return.  Must appear with start.
            * qf: set to a string; if the question text contains this string, it will be returned.
                Conjunctive with 'af' and 'df' filters.
            * af: set to a string; if the answer text contains this string, it will be returned.
                Conjunctive with 'qf' and 'df' filters.
            * df: set to a string; if the text of any of the distractors contains this string,
                it will be returned.  Conjunctive with 'af' and 'qf' filters.
            * sk: set to one of the following to set the sorting key for questions:
                * 'i': sort by id_number (the default)
                * 'q': sort by question text
                * 'a': sort by answer text
                * 'd': sort by the number of distractors
            * sd: set to one of the following to set the sorting direction for questions:
                * 'a': sort ascending (the default)
                * 'd': sort descending
        Returns status 200 along with the formatted question data on success.
        Returns status 400 if pagination arguments (start, num) are supplied but are invalid.
        Returns status 500 on application error.
    """
    if h.has_pagination_args(request) and not h.pagination_args_are_valid(request):
        abort(400)

    questions = invoke_get_with_filters(repository, request.args)
    return h.format_question_response(questions, request.args)


@app.route('/questions/', methods=['POST'])
def create_questions():
    """
    Allows creation of one or more new questions, given a JSON payload.
    Returns the new questions (with IDs) on success.
        Returns status 201 along with the JSON for the new questions on success.
        Returns status 400 if the JSON payload is malformed.
        Returns status 500 on application error.
    """
    question = q.Question()
    if not question.try_set_from_json(request.json):
        abort(400)
    new_question = repository.create(question)
    return Response(new_question.to_json(), mimetype='application/json')


@app.route('/questions/<id_number>/', methods=['PUT'])
def edit_question(id_number):
    """
    Changes the data for a question given an ID and a JSON payload.  Returns the edited
    question on success.
        Returns status 200 along with the JSON for the updated question on success.
        Returns status 404 if the requested question does not exist.
        Returns status 400 if the supplied ID was not a number, the JSON payload is malformed,
            or the ID in the payload does not match the URL.
        Returns status 500 on application error.
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
        Returns status 204 (no content) on success.
        Returns status 404 if the requested question does not exist.
        Returns status 400 if the supplied ID was not a number.
        Returns status 500 on application error.
    """
    if not h.is_valid_int(id_number):
        abort(400)
    question = repository.get_by_id(id_number)
    if question == None:
        abort(404)
    repository.remove(question)
    return '', 204


def invoke_get_with_filters(repo, args, id_numbers=None):
    """
    Given a question repository and a validated request context,
    loads questions given various parameters.
    The parameters can be arbitrarily mixed and matched by the caller.
    """

    # ID filters
    id_list = None
    if isinstance(id_numbers, str):
        id_list = id_numbers.split(',')

    # Pagination filters
    start = None
    num = None
    if h.has_pagination_args(request):
        start = int(args.get('start'))
        num = int(args.get('num'))

    # Question value filters
    question_filter = args.get('qf')
    answer_filter = args.get('af')
    distractor_filter = args.get('df')

    # Sorting
    sort_key = args.get('sk')
    if not isinstance(sort_key, str):
        sort_key = 'i'
    sort_direction = args.get('sd')
    if not isinstance(sort_direction, str):
        sort_direction = 'a'

    questions = repo.get_with_filters(id_list=id_list,
                                      start_record=start,
                                      num_records=num,
                                      question_filter=question_filter,
                                      answer_filter=answer_filter,
                                      distractor_filter=distractor_filter,
                                      sort_key=sort_key,
                                      sort_descending=(sort_direction.lower() == 'd'))
    return questions


if __name__ == '__main__':
    initialize()
    app.run()
