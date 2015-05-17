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


def hasPaginationArgs(request):
    """
    Quick helper to check for pagination args
    """
    start = request.args.get('start')
    num = request.args.get('num')
    return isinstance(start, str) and isinstance(num, str)


def paginationArgsAreValid(request):
    """
    Quick helper to check that pagination args are valid
    """
    if not hasPaginationArgs(request):
        return False
    start = request.args.get('start')
    num = request.args.get('num')
    if not isValidInt(start) or not isValidInt(num):
        return False
    if int(start) < 1 or int(num) < 1:
        return False
    return True


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
        if not isValidInt(id):
            return False
    return True


def isValidInt(stringToCheck):
    """
    Safely checks that a string value is an integer
    """
    if stringToCheck == None:
        return False
    try:
        int(stringToCheck)
        return True
    except ValueError:
        return False