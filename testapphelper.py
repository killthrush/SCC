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


def invoke_get_with_filters(repo, args, id_numbers=None):
    """
    Given a question repository and a validated request context,
    loads questions given various parameters.
    The parameters can be arbitrarily mixed and matched by the caller.
    """

    # ID filters
    id_list = None
    if isinstance(id_numbers, str):
        id_list = id_numbers.split(',')

    # Pagination filters
    start = None
    num = None
    if has_pagination_args(args):
        start = int(args.get('start'))
        num = int(args.get('num'))

    # Question value filters
    question_filter = args.get('qf')
    answer_filter = args.get('af')
    distractor_filter = args.get('df')

    # Sorting
    sort_key = args.get('sk')
    if not isinstance(sort_key, str):
        sort_key = 'i'
    sort_direction = args.get('sd')
    if not isinstance(sort_direction, str):
        sort_direction = 'a'

    questions = repo.get_with_filters(id_list=id_list,
                                      start_record=start,
                                      num_records=num,
                                      question_filter=question_filter,
                                      answer_filter=answer_filter,
                                      distractor_filter=distractor_filter,
                                      sort_key=sort_key,
                                      sort_descending=(sort_direction.lower() == 'd'))
    return questions