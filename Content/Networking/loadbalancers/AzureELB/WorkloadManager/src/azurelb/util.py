#!/usr/bin/env python

import json

# Hook Method to convert unicode
def deunicodify_hook(pairs):
    new_pairs = []
    for key, value in pairs:
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        new_pairs.append((key, value))
    return dict(new_pairs)

# Raise Error with message
def print_error(msg):
    print('CLIQR_EXTERNAL_SERVICE_ERR_MSG_START')
    print(msg)
    print('CLIQR_EXTERNAL_SERVICE_ERR_MSG_END')


def print_log(msg):
    print('CLIQR_EXTERNAL_SERVICE_LOG_MSG_START')
    print(msg)
    print('CLIQR_EXTERNAL_SERVICE_LOG_MSG_END')


def print_result(msg):
    print('CLIQR_EXTERNAL_SERVICE_RESULT_START')
    print(msg)
    print('CLIQR_EXTERNAL_SERVICE_RESULT_END')


# Write Error on FAILURE file
def write_error(e):
    f = open('FAILURE', 'w')
    f.write(str(e))
    f.close()

# Get Error Messages Object from Error Message JSON file
def get_error_messages():
    messages = {}
    try:
        with open('error_messages.json', 'r') as file:
            messages = json.loads(str(file.read()), object_pairs_hook=deunicodify_hook)
    except Exception as err:
        print err

    return messages

# Generate error message with parameters
def generate_params_error_message(parameters, error_message):
    reason = ""
    if isinstance(parameters, list):
        reason = ','.join(parameters)
    else:
        reason = parameters

    reason += " ," + error_message
    return reason

# Global Error Message 
def error_message():
    global error_messages
    error_messages = get_error_messages()

error_message()    