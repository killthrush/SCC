from flask import Flask
from flask import Response
from flask import request
from flask import abort
import questions as q
import testapphelper as h

app = Flask(__name__)

# TODO:
# 1) Pagination
# 2) Filtering
# 5) code TODOs
# 6) clean up, linting
# 7) deployment, readme
# 8) save state
# 9) attempt some tests
# 10) test driver (angular?)

# Keep questions in memory
# This doesn't look thread-safe...
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
        Returns status 200 along with the formatted question data on success.
        Returns status 400 if the ID list is malformed.
        Returns status 500 on application error.
    """    
    if not h.isValidIdList(ids):
        abort(400)
    idList = ids.split(',')
    questions = repository.getByIds(idList)
    return h.formatQuestionResponse(questions, request)

 
@app.route('/questions/', methods=['GET'])
def getAllQuestions():
    """
    Returns all available questions in JSON format (the default), or in csv format.
        Allowed parameters:
            * fmt: set to 'csv' to return the questions in pipe-delimited format
        Returns status 200 along with the formatted question data on success.
        Returns status 500 on application error.
    """
    questions = repository.getAll() # Methinks this is dangerous in general
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
    if not h.isValidId(id):
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
    if not h.isValidId(id):
        abort(400)    
    question = repository.getById(id)
    if question == None:
        abort(404)
    repository.remove(question)
    return '', 204



if __name__ == '__main__':
    initialize(app)
    app.run()
