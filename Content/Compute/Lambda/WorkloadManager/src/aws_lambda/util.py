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


def write_error(e):
    f = open('FAILURE', 'w')
    f.write(str(e))
    f.close()
