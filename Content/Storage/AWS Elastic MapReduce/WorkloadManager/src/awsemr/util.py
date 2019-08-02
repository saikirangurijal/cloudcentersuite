#!/usr/bin/env python

# Raise Error with message
def print_error(msg):
    print('CLIQR_EXTERNAL_SERVICE_ERR_MSG_START')
    print(msg)
    print('CLIQR_EXTERNAL_SERVICE_ERR_MSG_END')


# Logging messages
def print_log(msg):
    print('CLIQR_EXTERNAL_SERVICE_LOG_MSG_START')
    print(msg)
    print('CLIQR_EXTERNAL_SERVICE_LOG_MSG_END')


# Print result
def print_result(msg):
    print('CLIQR_EXTERNAL_SERVICE_RESULT_START')
    print(msg)
    print('CLIQR_EXTERNAL_SERVICE_RESULT_END')
