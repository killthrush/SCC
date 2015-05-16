from flask import Flask
import questions as q

app = Flask(__name__)

# Keep questions in memory
# This doesn't look thread-safe...
questions = q.SimpleQuestionRepository()

def initialize(app):
    app.debug = True # allow stack traces for development
    questions.loadFromFile('./question_state.csv')


@app.route('/questions/<ids>/', methods=['GET']) # get questions; can use format specifier here (json or csv).  Can also use page arguments, filters, sorting
def get_questions(ids):
    jsonString = questions.getAll().toJson()
    return jsonString

@app.route('/questions', methods=['POST']) # post to create one or more questions using json or csv format
def create_questions():
    pass

@app.route('/questions', methods=['PUT']) # put to replace one or more questions using json format
def edit_questions():
    pass

@app.route('/questions', methods=['DELETE']) # delete to drop a question
def remove_questions():
    pass

if __name__ == '__main__':
    initialize(app)
    app.run()
