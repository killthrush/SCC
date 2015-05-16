import json
from flask import Flask
from flask import Response
import questions as q

app = Flask(__name__)

# Keep questions in memory
# This doesn't look thread-safe...
repository = q.SimpleQuestionRepository()

def initialize(app):
    app.debug = True # allow stack traces for development
    repository.loadFromFile('./question_state.csv')


@app.route('/questions/<ids>/', methods=['GET']) # get questions; can use format specifier here (json or csv).  Can also use page arguments, filters, sorting
def get_some_questions(ids):
    idSet = ids.split(',') # TODO: this needs some hardening
    questions = repository.getByIds(idSet)
    jsonString = questions.toJson()
    return Response(jsonString, mimetype='application/json')
 
@app.route('/questions/', methods=['GET']) # get all questions; can use format specifier here (json or csv).  Can also use page arguments, filters, sorting
def get_all_questions():
    questions = repository.getAll() # Methinks this is dangerous in general - DDoS waiting to happen
    jsonString = questions.toJson()
    return Response(jsonString, mimetype='application/json')

@app.route('/questions/', methods=['POST']) # post to create one or more questions using json format
def create_questions():
    pass

@app.route('/questions/', methods=['PUT']) # put to replace one or more questions using json format
def edit_questions():
    pass

@app.route('/questions/', methods=['DELETE']) # delete to drop a question
def remove_questions():
    pass

if __name__ == '__main__':
    initialize(app)
    app.run()
