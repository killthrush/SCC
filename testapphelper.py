from flask import request
from flask import Response

def format_question_response(questions, request):
    """
    Quick helper to check for formatting args and return question data in the correct format
    """
    format = request.args.get('fmt')
    if isinstance(format, str) and format.lower() == 'csv':
        csv_string = questions.to_csv()
        return Response(csv_string, mimetype='text/csv')
    json_string = questions.to_json()
    return Response(json_string, mimetype='application/json')


def has_pagination_args(request):
    """
    Quick helper to check for pagination args
    """
    start = request.args.get('start')
    num = request.args.get('num')
    return isinstance(start, str) and isinstance(num, str)


def pagination_args_are_valid(request):
    """
    Quick helper to check that pagination args are valid
    """
    if not has_pagination_args(request):
        return False
    start = request.args.get('start')
    num = request.args.get('num')
    if not is_valid_int(start) or not is_valid_int(num):
        return False
    if int(start) < 1 or int(num) < 1:
        return False
    return True


def is_valid_id_list(idList):
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
        if not is_valid_int(id):
            return False
    return True


def is_valid_int(stringToCheck):
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