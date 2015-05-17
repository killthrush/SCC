"""
Module that contains some helpful shortcut functions for the test web app.
Helps keep the routes nice and readable.
"""

from flask import Response

def format_question_response(questions, query_string):
    """
    Quick helper to check for formatting args and return question data in the correct format
    """
    format_string = query_string.get('fmt')
    if isinstance(format_string, str) and format_string.lower() == 'csv':
        csv_string = questions.to_csv()
        return Response(csv_string, mimetype='text/csv')
    json_string = questions.to_json()
    return Response(json_string, mimetype='application/json')


def has_pagination_args(query_string):
    """
    Quick helper to check for pagination args
    """
    start = query_string.get('start')
    num = query_string.get('num')
    return isinstance(start, str) and isinstance(num, str)


def pagination_args_are_valid(query_string):
    """
    Quick helper to check that pagination args are valid
    """
    if not has_pagination_args(query_string):
        return False
    start = query_string.get('start')
    num = query_string.get('num')
    if not is_valid_int(start) or not is_valid_int(num):
        return False
    if int(start) < 1 or int(num) < 1:
        return False
    return True


def is_valid_id_list(id_list):
    """
    Safely checks that an ID list contains a valid comma-separated list of integers
    """
    if id_list == None:
        return False
    if not isinstance(id_list, str):
        return False
    # strip all whitespace; if there is any, input isn't valid
    temp_id_list = ''.join(id_list.split())
    if len(id_list) != len(temp_id_list):
        return False
    id_strings = temp_id_list.split(',')
    for id_string in id_strings:
        if not is_valid_int(id_string):
            return False
    return True


def is_valid_int(string_to_check):
    """
    Safely checks that a string value is an integer
    """
    if string_to_check == None:
        return False
    try:
        int(string_to_check)
        return True
    except ValueError:
        return False
