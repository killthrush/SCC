from flask import request
from flask import Response

def formatQuestionResponse(questions, request):
    """
    Quick helper to check for formatting args and return question data in the correct format
    """
    format = request.args.get('fmt')
    if isinstance(format, str) and format.lower() == 'csv':
        csvString = questions.toCsv()
        return Response(csvString, mimetype='text/csv')
    jsonString = questions.toJson()
    return Response(jsonString, mimetype='application/json')


def isValidIdList(idList):
    """
    Safely checks that an ID list contains a valid comma-separated list of integers
    """
    if idList == None:
        return False
    if not isinstance(idList, str):
        return False
    # strip all whitespace; if there is any, input isn't valid
    tempIdList = ''.join(idList.split())
    if len(idList) != len(tempIdList):
        return False
    ids = tempIdList.split(',')
    for id in ids:
        if not isValidId(id):
            return False
    return True


def isValidId(id):
    """
    Safely checks that an ID value is an integer
    """
    if id == None:
        return False
    try:
        int(id)
        return True
    except ValueError:
        return False