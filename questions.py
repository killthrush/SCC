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
        self.distractors = csvRow[2].split(', ')

    def setFromJson(self, jsonString):
        json.loads(jsonString, self)

    def setIdentity(self, idValue):
        if (self.id == None):
            self.id = idValue
        else:
            pass
            # TODO: exception?

    def toJson(self):
        return json.dumps(self.__dict__, indent=4, sort_keys=True) # TODO: not used; remove

    def toCsv(self):
        return ''


class QuestionCollection():

    """
    QuestionCollection is a simple convenience wrapper around a primitive list of Questions
    """

    def __init__(self):
        self._questionsInternal = []

    def toJson(self): # TODO : clean this up
        jsonString = '['
        jsonSnippets = []
        jsonSnippets2 = []
        for question in self._questionsInternal:
            jsonSnippets.append(question.toJson())
            jsonSnippets2.append(question.__dict__)
        jsonString += ','.join(jsonSnippets)
        jsonString += ']'  

        jsonString = json.dumps(jsonSnippets2, indent=4, sort_keys=True)
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
        self._questionsInternal = dict()
        self._nextId = 1

    def loadFromFile(self, path):
        _questionsInternal = dict()

        with open(path) as csvFile: # TODO: probably should wrap with a try/catch

            csvSniffer = csv.Sniffer()
            sample = csvFile.read(1024)
            dialect = csvSniffer.sniff(sample, '|')
            hasHeader = csvSniffer.has_header(sample)
            csvFile.seek(0)

            csvRows = csv.reader(csvFile, dialect, delimiter ='|')

            rowIndex = 0
            for row in csvRows:
                rowIndex += 1
                if (hasHeader and rowIndex == 1):
                    continue
                question = Question()
                question.setFromCsv(row)
                question.setIdentity(rowIndex)
                self._questionsInternal.setdefault(question.id, question)

            self._nextId += len(_questionsInternal) + 1


    def getAll(self):
        returnCollection = QuestionCollection() 
        for question in self._questionsInternal.values():
            returnCollection.addQuestion(question)
        return returnCollection


    def getByIds(self, idSet):
        returnCollection = QuestionCollection()        

        for id in idSet:
            idValue = int(id)
            if not idValue in self._questionsInternal:
                continue
            question = self._questionsInternal[idValue]
            returnCollection.addQuestion(question)

        return returnCollection


if __name__ == '__main__':
    pass  # TODO: add some tests