"""
Module that contains core classes for working with Questions.
"""

import json
import csv

class Question():

    """
    Represents a Question, an object with text to represent the question itself,
    along with text to represent right and wrong answers.
    """

    def __init__(self):
        """
        Initializes the Question instance
        """
        self.id_number = None
        self.question = ''
        self.answer = ''
        self.distractors = []

    def try_set_from_csv(self, csv_row):
        """
        Attempt to safely set the Question's fields using a row of data parsed from csv.
        """
        if csv_row == None or len(csv_row) != 3:
            return False
        try:
            self.question = csv_row[0]
            self.answer = csv_row[1]
            self.distractors = csv_row[2].split(', ')
        except Exception:
            return False
        return True

    def try_set_from_json(self, json_dict):
        """
        Attempt to safely set the Question's fields using json data parsed from a web request.
        """
        if json_dict == None or not isinstance(json_dict, dict):
            return False
        if not 'question' in json_dict or not 'answer' in json_dict or not 'distractors' in json_dict:
            return False
        self.question = json_dict['question']
        self.answer = json_dict['answer']
        self.distractors = json_dict['distractors']
        return True

    def set_identity(self, id_value):
        """
        Sets the question's ID. Raises an exception if this is attempted more than once.
        """
        if self.id_number == None:
            self.id_number = int(id_value)
        else:
            message = 'Tried to change a Question ID value from ' + self.id_number + ' to ' + id_value
            raise RuntimeError(message)

    def to_json(self):
        """
        Converts the Question's fields to pretty-printed JSON.
        """
        return json.dumps(self.__dict__, indent=4, sort_keys=True)

    def to_csv(self):
        """
        Converts the Question's fields to pipe-separated format.
        """
        distractors_string = ', '.join(self.distractors)
        csv_string = "{0}|{1}|{2}|{3}\n".format(str(self.id_number),
                                                self.question,
                                                self.answer,
                                                distractors_string)
        return csv_string


class QuestionCollection():

    """
    QuestionCollection is a simple convenience wrapper around a primitive list of Questions
    """

    def __init__(self):
        """
        Initializes the QuestionCollection instance
        """
        self._internal_questions = []

    def __iter__(self):
        """
        Returns a standard iterator for the QuestionCollection instance
        """
        return self._internal_questions.__iter__()



    def to_json(self):
        """
        Converts the QuestionCollection's fields to pretty-printed JSON.
        """
        json_snippets = []
        for question in self._internal_questions:
            json_snippets.append(question.__dict__)
        json_string = json.dumps(json_snippets, indent=4, sort_keys=True)
        return json_string

    def to_csv(self):
        """
        Converts the QuestionCollection's fields to pipe-separated format.
        """
        csv_data = 'id|question|answer|distractors\n'
        for question in self._internal_questions:
            csv_data += question.to_csv()
        return csv_data

    def add_question(self, question):
        """
        Adds a Question to the QuestionCollection's instance.
        """
        self._internal_questions.append(question)



class SimpleQuestionRepository():

    """
    SimpleQuestionRepository is an implementation of a repository pattern for Questions that uses in-memory types for run-time operations and
    csv files on disk for persistence.
    """

    _sortFunctions = {'i':lambda question: question.id_number,
                      'q':lambda question: question.question,
                      'a':lambda question: question.answer,
                      'd':lambda question: len(question.distractors)}

    def __init__(self):
        """
        Initializes the SimpleQuestionRepository instance
        """
        self._internal_questions = dict()
        self._next_id = 1


    def load_state_from_file(self, path):
        """
        Initializes the SimpleQuestionRepository instance by loading data from a csv file.
        """
        self._internal_questions = dict()
        self._next_id = 1
        try:
            with open(path) as csv_file:

                sniffer = csv.Sniffer()
                sample = csv_file.read(1024)
                dialect = sniffer.sniff(sample, '|')
                has_header = sniffer.has_header(sample)
                csv_file.seek(0)

                csv_rows = csv.reader(csv_file, dialect, delimiter='|')
                row_number = 0
                for row in csv_rows:
                    if len(row):
                        pass
                    row_number += 1
                    if has_header and row_number == 1:
                        continue
                    question = Question()
                    if question.try_set_from_csv(row):
                        self.create(question)
        except OSError:
            pass  # TODO: if we had a logger, now would be the time to use it

    def save_state_to_file(self, path):
        """
        Dumps the internal state of the repository to a csv file.
        """
        pass #TODO: implement this as a function of shutting down the app


    def get_by_id(self, id_number):
        """
        Loads a single Question from the repository by its ID.
        Returns None if the question is not found.
        """
        id_value = int(id_number)
        if not id_value in self._internal_questions:
            return None
        question = self._internal_questions[id_value]
        return question


    def get_with_filters(self,
                         id_list=None,
                         start_record=None,
                         num_records=None,
                         question_filter=None,
                         answer_filter=None,
                         distractor_filter=None,
                         sort_key='i',
                         sort_descending=False):
        """
        Loads a QuestionCollection from the repository based on a set of optional filters.
        Also can apply a simple set of sort conditions.
        Returns an empty QuestionCollection if no questions matched the filters.
        """
        working_question_list = []

        # Load main list of questions; this will be filtered further if needed
        if id_list != None:
            working_question_list = [self.get_by_id(id_number) for id_number in id_list if self.get_by_id(id_number) != None]
        else:
            working_question_list = list(self._internal_questions.values()) # this wrapping is necessary for python 3

        # Apply sorting
        if not sort_key.lower() in self._sortFunctions:
            sort_key = 'i'
        working_question_list = sorted(working_question_list, key=self._sortFunctions[sort_key.lower()], reverse=sort_descending)

        # Apply value filters, if needed
        if isinstance(question_filter, str):
            working_question_list = [q for q in working_question_list if q.question.find(question_filter) != -1]
        if isinstance(answer_filter, str):
            working_question_list = [q for q in working_question_list if q.answer.find(answer_filter) != -1]
        if isinstance(distractor_filter, str):
            working_question_list = [q for q in working_question_list if len([d for d in q.distractors if d.find(distractor_filter) != -1]) > 0]

        # Apply pagination filter to remaining results
        if isinstance(start_record, int) and isinstance(num_records, int):
            working_question_list = working_question_list[start_record-1:start_record+num_records-1]

        return_collection = QuestionCollection()
        for question in working_question_list:
            return_collection.add_question(question)
        return return_collection


    def create(self, question):
        """
        Creates a Question in the repository and defines its ID.
        """
        question.set_identity(self._next_id)
        self._internal_questions.setdefault(question.id_number, question)
        self._next_id += 1
        return question


    def change(self, question):
        """
        Replaces a Question in the repository with the one supplied.
        """
        if not question.id_number in self._internal_questions:
            return
        self._internal_questions[question.id_number] = question
        return question


    def remove(self, question):
        """
        Removes the given Question from the repository.
        """
        if not question.id_number in self._internal_questions:
            return
        self._internal_questions.pop(question.id_number)


if __name__ == '__main__':
    pass  # TODO: add some tests
