# Smarterer Code Challenge
Come see a n00b try to write some Python code! 

This sample API is implemented as a Flask application written in Python 3.  I chose Flask because I've been wanting to try it for a while - it's simple, elegant, and perfect for a small coding exercise.  I chose Python 3 because I didn't know better.  At least I won't be breaking anything!

# Setup
* Clone this repo
* Install Python 3 if you don't already have it
* Install Flask as described here: http://flask.pocoo.org/docs/0.10/installation/#installation
* Windows installations for Flask are a bit more complicated; you might need to install easy_install and pip first (see documentation)
* Run testapp.py from your python shell.  This will run the API endpoint on http://localhost:5000.  The application will parse and read question_state.csv into memory, so you will be able to test the endpoint immediately.
* Test the endpoint using curl or your favorite Chrome REST plugin (I use the Advanced Rest Client)

# Rough Edges
* Normally I write a lot of unit tests, but as this is my first Python app, I haven't learned how it all works yet so there's no tests
* There's no driver UI.  Given some more time I would have built something with angular and included it in the project.
* The state of the questions does not persist to disk.  I wrote a stub but didn't finish.
* I'm not sure that this Flask app is thread-safe with its in-memory repo. I need to read more on how this stuff works
* There's not much in the way of indexing for the question data beyond a dictionary to handle quick lookups by ID
* I tried to stick to accepted python style as much as possible, but there still might be a C# accent.  Went nuts with pylint, maybe I went overboard?

# API Documentation

## GET /questions/
    Returns all available questions in JSON format (the default), or in csv format.
        Allowed parameters:
            * fmt: set to 'csv' to return the questions in pipe-delimited format
            * start: set to the ordinal number of the first question to return.
                Must appear with num.
            * num: set to the total number of questions to return.  Must appear with start.
            * qf: set to a string; if the question text contains this string, it will be returned.
                Conjunctive with 'af' and 'df' filters.
            * af: set to a string; if the answer text contains this string, it will be returned.
                Conjunctive with 'qf' and 'df' filters.
            * df: set to a string; if the text of any of the distractors contains this string,
                it will be returned.  Conjunctive with 'af' and 'qf' filters.
            * sk: set to one of the following to set the sorting key for questions:
                * 'i': sort by id_number (the default)
                * 'q': sort by question text
                * 'a': sort by answer text
                * 'd': sort by the number of distractors
            * sd: set to one of the following to set the sorting direction for questions:
                * 'a': sort ascending (the default)
                * 'd': sort descending
        Returns status 200 along with the formatted question data on success.
        Returns status 400 if pagination arguments (start, num) are supplied but are invalid.
        Returns status 500 on application error.

## GET /questions/&lt;id_numbers&gt;/
    Returns questions matching the given IDs in JSON format (the default), or in csv format.
        Allowed parameters:
            * fmt: set to 'csv' to return the questions in pipe-delimited format
            * start: set to the ordinal number of the first question to return.
                Must appear with num.
            * num: set to the total number of questions to return.  Must appear with start.
            * qf: set to a string; if the question text contains this string, it will be returned.
                Conjunctive with 'af' and 'df' filters.
            * af: set to a string; if the answer text contains this string, it will be returned.
                Conjunctive with 'qf' and 'df' filters.
            * df: set to a string; if the text of any of the distractors contains this string,
                it will be returned.  Conjunctive with 'af' and 'qf' filters.
            * sk: set to one of the following to set the sorting key for questions:
                * 'i': sort by id_number (the default)
                * 'q': sort by question text
                * 'a': sort by answer text
                * 'd': sort by the number of distractors
            * sd: set to one of the following to set the sorting direction for questions:
                * 'a': sort ascending (the default)
                * 'd': sort descending
        Returns status 200 along with the formatted question data on success.
        Returns status 400 if the ID list is malformed or if pagination arguments (start, num)
            are supplied but are invalid.
        Returns status 500 on application error.

## POST /questions/
    Allows creation of anew question, given a JSON payload.
    Returns the new questions (with IDs) on success.
        Returns status 201 along with the JSON for the new questions on success.
        Returns status 400 if the JSON payload is malformed.
        Returns status 500 on application error.
        
## PUT /questions/&lt;id_number&gt;/
    Changes the data for a question given an ID and a JSON payload.  Returns the edited
    question on success.
        Returns status 200 along with the JSON for the updated question on success.
        Returns status 404 if the requested question does not exist.
        Returns status 400 if the supplied ID was not a number, the JSON payload is malformed,
            or the ID in the payload does not match the URL.
        Returns status 500 on application error.
        
## DELETE /questions/&lt;id_number&gt;/
    Removes the given question from the repository.
        Returns status 204 (no content) on success.
        Returns status 404 if the requested question does not exist.
        Returns status 400 if the supplied ID was not a number.
        Returns status 500 on application error.
        
## HEAD /questions/ and HEAD /questions/&lt;id_numbers&gt;/
These endpoints are provided by Flask free of charge and accept the same arguments as a GET request.

# JSON Format
The format of a proper JSON document looks like this:
    
    {
        "answer": "3333",
        "distractors": [
            "3",
            "34",
            "345",
            "3456"
        ],
        "id": 300,
        "question": "What is 34 - 45?"
    }

