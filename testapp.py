from flask import Flask
from flask import Response
from flask import request
from flask import abort
import questions as q
import testapphelper as h

app = Flask(__name__)

# TODO:
# 5) code TODOs
# 6) clean up, linting
# 7) deployment, readme
# 8) save state
# 9) attempt some tests
# 10) test driver (angular?)

# Keep questions in memory. This doesn't look thread-safe...
repository = q.SimpleQuestionRepository()

def initialize(app):
    app.debug = True # allow stack traces for development
    repository.loadStateFromFile('./question_state.csv')


@app.route('/questions/<ids>/', methods=['GET'])
def getSomeQuestions(ids):
    """
    Returns questions matching the given IDs in JSON format (the default), or in csv format.
        Allowed parameters:
            * fmt: set to 'csv' to return the questions in pipe-delimited format
            * start: set to the ordinal number of the first question to return.  Must appear with num.
            * num: set to the total number of questions to return.  Must appear with start.
            * qf: set to a string; if the question text contains this string, it will be returned.  Conjunctive with 'af' and 'df' filters.
            * af: set to a string; if the answer text contains this string, it will be returned.  Conjunctive with 'qf' and 'df' filters.
            * df: set to a string; if the text of any of the distractors contains this string, it will be returned.  Conjunctive with 'af' and 'qf' filters.
            * sk: set to one of the following to set the sorting key for questions: 
                * 'i': sort by id (the default)
                * 'q': sort by question text
                * 'a': sort by answer text
                * 'd': sort by the number of distractors
            * sd: set to one of the following to set the sorting direction for questions: 
                * 'a': sort ascending (the default)
                * 'd': sort descending              
        Returns status 200 along with the formatted question data on success.
        Returns status 400 if the ID list is malformed or if pagination arguments (start, num) are supplied but are invalid.
        Returns status 500 on application error.
    """    
    if not h.isValidIdList(ids) or (h.hasPaginationArgs(request) and not h.paginationArgsAreValid(request)):
        abort(400)
    
    questions = invokeGetWithFilters(repository, request, ids)
    return h.formatQuestionResponse(questions, request)

 
@app.route('/questions/', methods=['GET'])
def getAllQuestions():
    """
    Returns all available questions in JSON format (the default), or in csv format.
        Allowed parameters:
            * fmt: set to 'csv' to return the questions in pipe-delimited format
            * start: set to the ordinal number of the first question to return.  Must appear with num.
            * num: set to the total number of questions to return.  Must appear with start.
            * qf: set to a string; if the question text contains this string, it will be returned.  Conjunctive with 'af' and 'df' filters.
            * af: set to a string; if the answer text contains this string, it will be returned.  Conjunctive with 'qf' and 'df' filters.
            * df: set to a string; if the text of any of the distractors contains this string, it will be returned.  Conjunctive with 'af' and 'qf' filters.
            * sk: set to one of the following to set the sorting key for questions: 
                * 'i': sort by id (the default)
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
    if (h.hasPaginationArgs(request) and not h.paginationArgsAreValid(request)):
        abort(400)

    questions = invokeGetWithFilters(repository, request)
    return h.formatQuestionResponse(questions, request)


@app.route('/questions/', methods=['POST'])
def createQuestions():
    """
    Allows creation of one or more new questions, given a JSON payload.  Returns the new questions (with IDs) on success.
        Returns status 201 along with the JSON for the new questions on success.
        Returns status 400 if the JSON payload is malformed.
        Returns status 500 on application error.
    """
    question = q.Question()
    if not h.isValidInt(id):
        abort(400)
    if not question.trySetFromJson(request.json):
        abort(400)
    newQuestion = repository.create(question)
    return Response(newQuestion.toJson(), mimetype='application/json')


@app.route('/questions/<id>/', methods=['PUT'])
def editQuestion(id):
    """
    Changes the data for a question given an ID and a JSON payload.  Returns the edited question on success.
        Returns status 200 along with the JSON for the updated question on success.
        Returns status 404 if the requested question does not exist.
        Returns status 400 if the supplied ID was not a number, the JSON payload is malformed, or the ID in the payload does not match the URL.
        Returns status 500 on application error.
    """
    if not h.isValidInt(id):
        abort(400)
    question = repository.getById(id)
    if question == None:
        abort(404)
    if 'id' in request.json and request.json['id'] != int(id):
        abort(400)
    if not question.trySetFromJson(request.json):
        abort(400)
    returnQuestion = repository.change(question)
    return Response(returnQuestion.toJson(), mimetype='application/json')


@app.route('/questions/<id>/', methods=['DELETE'])
def removeQuestion(id):
    """
    Removes the given question from the repository.
        Returns status 204 (no content) on success.
        Returns status 404 if the requested question does not exist.
        Returns status 400 if the supplied ID was not a number.
        Returns status 500 on application error.
    """
    if not h.isValidInt(id):
        abort(400)    
    question = repository.getById(id)
    if question == None:
        abort(404)
    repository.remove(question)
    return '', 204


def invokeGetWithFilters(repository, request, ids = None):
    """
    Given a question repository and a validated request context,
    loads questions given various parameters.
    The parameters can be arbitrarily mixed and matched by the caller.
    """

    # ID filters
    idList = None
    if isinstance(ids, str):
        idList = ids.split(',')
    
    # Pagination filters
    start = None
    num = None
    if h.hasPaginationArgs(request):
        start = int(request.args.get('start'))
        num = int(request.args.get('num'))

    # Question value filters
    questionFilter = request.args.get('qf')
    answerFilter = request.args.get('af')
    distractorFilter = request.args.get('df')

    # Sorting
    sortKey = request.args.get('sk')
    if not isinstance(sortKey, str):
        sortKey = 'i'
    sortDirection = request.args.get('sd')
    if not isinstance(sortDirection, str):
        sortDirection = 'a'

    questions = repository.getWithFilters(idList = idList, 
                                          startRecord = start, 
                                          numRecords = num,
                                          questionFilter = questionFilter,
                                          answerFilter = answerFilter,
                                          distractorFilter = distractorFilter,
                                          sortKey = sortKey,
                                          sortDescending = (sortDirection == 'd'))
    return questions


if __name__ == '__main__':
    initialize(app)
    app.run()
