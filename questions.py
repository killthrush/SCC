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

    def trySetFromJson(self, jsonDict):
        if jsonDict == None or not isinstance(jsonDict, dict):
            return False
        if not 'question' in jsonDict or not 'answer' in jsonDict or not 'distractors' in jsonDict:
            return False
        self.question = jsonDict['question']
        self.answer = jsonDict['answer']
        self.distractors = jsonDict['distractors']
        return True

    def setIdentity(self, idValue):
        if (self.id == None):
            self.id = idValue
        else:
            pass
            # TODO: exception if we try to change an already-set ID?

    def toJson(self):
        return json.dumps(self.__dict__, indent=4, sort_keys=True)

    def toCsv(self):
        distractorsString = ', '.join(self.distractors)
        return str(self.id) + '|' + self.question + '|' + self.answer + '|' + distractorsString + '\n'


class QuestionCollection():

    """
    QuestionCollection is a simple convenience wrapper around a primitive list of Questions
    """

    def __init__(self):
        self._questionsInternal = []

    def __iter__(self):
        return self._questionsInternal.__iter__()

    def __next__(self):
        return self._questionsInternal.__next__()

    def toJson(self):
        jsonSnippets = []
        for question in self._questionsInternal:
            jsonSnippets.append(question.__dict__)
        jsonString = json.dumps(jsonSnippets, indent=4, sort_keys=True)
        return jsonString

    def toCsv(self):
        csvData = 'id|question|answer|distractors\n'
        for question in self._questionsInternal:
            csvData += question.toCsv()
        return csvData

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


    def loadStateFromFile(self, path):
        self._questionsInternal = dict()
        self._nextId = 1
        with open(path) as csvFile: # TODO: probably should wrap with a try/catch

            csvSniffer = csv.Sniffer()
            sample = csvFile.read(1024)
            dialect = csvSniffer.sniff(sample, '|')
            hasHeader = csvSniffer.has_header(sample)
            csvFile.seek(0)

            csvRows = csv.reader(csvFile, dialect, delimiter ='|')
            rowNumber = 0
            for row in csvRows:
                rowNumber += 1
                if (hasHeader and rowNumber == 1):
                    continue
                question = Question()
                question.setFromCsv(row)
                self.create(question)


    def saveStateToFile(self, path):
        pass #TODO: implement this as a function of shutting down the app


    def getById(self, id): # TODO: should return copies of the questions; we want to avoid side effects
        idValue = int(id)
        if not idValue in self._questionsInternal:
            return None
        question = self._questionsInternal[idValue]    
        return question


    def getWithFilters(self, 
                       idList = None, 
                       startRecord = None, 
                       numRecords = None,
                       questionFilter = None,
                       answerFilter = None,
                       distractorFilter = None): # TODO: should return copies of the questions; we want to avoid side effects
        workingQuestionList = []

        # Load main list of questions; this will be filtered further if needed
        if idList != None:
            workingQuestionList = [self.getById(id) for id in idList if self.getById(id) != None]
        else:
            workingQuestionList = list(self._questionsInternal.values()) # this wrapping is necessary for python 3

        # TODO: apply sorting here

        # Apply value filters, if needed
        if isinstance(questionFilter, str):
            workingQuestionList = [q for q in workingQuestionList if q.question.find(questionFilter) != -1]
        if isinstance(answerFilter, str):
            workingQuestionList = [q for q in workingQuestionList if q.answer.find(answerFilter) != -1]
        if isinstance(distractorFilter, str):
            workingQuestionList = [q for q in workingQuestionList if len([d for d in q.distractors if d.find(distractorFilter) != -1]) > 0]

        # Apply pagination filter to remaining results
        if isinstance(startRecord, int) and isinstance(numRecords, int):
            workingQuestionList = workingQuestionList[startRecord-1:startRecord+numRecords-1]

        returnCollection = QuestionCollection()
        for question in workingQuestionList:
            returnCollection.addQuestion(question)  
        return returnCollection


    def create(self, question):
        question.setIdentity(self._nextId)
        self._questionsInternal.setdefault(question.id, question)
        self._nextId += 1
        return question


    def change(self, question):
        if not question.id in self._questionsInternal:
            return
        self._questionsInternal[question.id] = question
        return question


    def remove(self, question):
        if not question.id in self._questionsInternal:
            return
        self._questionsInternal.pop(question.id)


if __name__ == '__main__':
    pass  # TODO: add some tests