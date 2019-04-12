import sys
from util import print_error,print_log,print_result
command = sys.argv[1]

if __name__ == '__main__':

    try:
        print("Calling creating sql server service script")
        from google_sql import main
        main(command)

    except Exception as e:
        print e
        f = open('FAILURE', 'w')
        f.write(str(e))
        f.close()
		