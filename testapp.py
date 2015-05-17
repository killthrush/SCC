from flask import Flask
from flask import Response
from flask import request
import questions as q
import json

app = Flask(__name__)

# Keep questions in memory
# This doesn't look thread-safe...
repository = q.SimpleQuestionRepository()

def initialize(app):
    app.debug = True # allow stack traces for development
    repository.loadStateFromFile('./question_state.csv')


@app.route('/questions/<ids>/', methods=['GET']) # get specific questions; can use format specifier here (json or csv).  Can also use page arguments, filters, sorting
def get_some_questions(ids):
    idSet = ids.split(',') # TODO: this needs some hardening
    questions = repository.getByIds(idSet)
    format = request.args.get('fmt')
    if format == 'csv':
        csvString = questions.toCsv()
        return Response(csvString, mimetype='text/csv')
    jsonString = questions.toJson()
    return Response(jsonString, mimetype='application/json')

 
@app.route('/questions/', methods=['GET']) # get all questions; can use format specifier here (json or csv).  Can also use page arguments, filters, sorting
def get_all_questions():
    questions = repository.getAll() # Methinks this is dangerous in general - DDoS waiting to happen
    format = request.args.get('fmt')
    if format == 'csv':
        csvString = questions.toCsv()
        return Response(csvString, mimetype='text/csv')
    jsonString = questions.toJson()
    return Response(jsonString, mimetype='application/json')


@app.route('/questions/', methods=['POST']) # post to create one or more questions using json format
def create_questions():
    question = q.Question()
    question.setFromJson(request.json) # TODO: this should probably generate a bad request if this if request.json is undefined or init throws
    newQuestion = repository.create(question)

    # return the new question along with hypermedia links
    return Response(newQuestion.toJson(), mimetype='application/json')


@app.route('/questions/<id>/', methods=['PUT']) # put to replace one or more questions using json format
def edit_questions(id):
    question = repository.getById(id)
    if question == None:
        return '', 404
    question.setFromJson(request.json)
    returnQuestion = repository.change(question)
    return Response(returnQuestion.toJson(), mimetype='application/json')


@app.route('/questions/<id>/', methods=['DELETE']) # delete to drop a question
def remove_questions(id):
    question = repository.getById(id)
    if question == None:
        return '', 404
    repository.remove(question)
    return '', 204


if __name__ == '__main__':
    initialize(app)
    app.run()
