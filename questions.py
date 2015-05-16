import json
import csv

class Question():
    
    """
    Represents a Question, an object with text to represent the question itself, along with text to represent right and wrong answers.
    """

    def __init__(self):
        self.id = None
        self.question = ''
        self.answer = ''
        self.distractors = []

    def setFromCsv(self, csvRow):
        self.question = csvRow[0] # TODO: need to be more defensive about this
        self.answer = csvRow[1]
        self.distractors = csvRow[2].split(', ', 1)

    def setFromJson(self, jsonString):
        json.loads(jsonString, self)

    def setIdentity(self, idValue):
        if (self.id == None):
            self.id = idValue
        else:
            pass
            # TODO: exception?

    def toJson(self):
        return json.dumps(self.__dict__)

    def toCsv(self):
        return ''


class QuestionCollection():

    """
    QuestionCollection is a simple convenience wrapper around a primitive list of Questions
    """

    def __init__(self):
        self._questionsInternal = []

    def toJson(self):
        jsonString = '['
        jsonSnippets = []
        for question in self._questionsInternal:
            jsonSnippets.append(question.toJson())
        jsonString += ','.join(jsonSnippets)
        jsonString += ']'  
        return jsonString

    def toCsv(self):
        return ''

    def addQuestion(self, question):
        self._questionsInternal.append(question)


class SimpleQuestionRepository():

    """
    SimpleQuestionRepository is an implementation of a repository pattern for Questions that uses in-memory types for run-time operations and
    csv files on disk for persistence.
    """

    def __init__(self):
        self._questionsInternal = QuestionCollection()
        self._nextId = 1

    def loadFromFile(self, path):
        _questionsInternal = []
        with open(path) as csvFile: # TODO: probably should wrap with a try/catch
            csvSniffer = csv.Sniffer()
            sample = csvFile.read(1024)
            dialect = csvSniffer.sniff(sample, '|')
            hasHeader = csvSniffer.has_header(sample)
            csvFile.seek(0)
            csvRows = csv.reader(csvFile, dialect, delimiter ='|')
            rowIndex = 1
            for row in csvRows:
                if (hasHeader and rowIndex > 1) or not hasHeader:
                    question = Question()
                    question.setFromCsv(row)
                    question.setIdentity(rowIndex)
                    self._questionsInternal.addQuestion(question)  # TODO: should probably add the question to an index for things like lookups
                rowIndex += 1
        self._nextId += len(_questionsInternal) + 1

    def getAll(self):
        return self._questionsInternal

    def getByIds(self, idSet):
        return self._questionsInternal

if __name__ == '__main__':
    pass  # TODO: add some tests