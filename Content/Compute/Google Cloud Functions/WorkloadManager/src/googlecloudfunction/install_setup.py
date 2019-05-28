# !/usr/bin/env python
import os
from subprocess import STDOUT, check_call
import sys,time
from util import print_error,print_log,print_result

pip_sources = [
    'google-api-python-client',
    'oauth2client',
	'google-cloud-storage'
    ]

def install_packages():
    print("Installing packeges.")
    print_log("Initiated...")
    global pip_sources


    for pip_pkg in pip_sources:
        s = check_call([sys.executable, '-m', 'pip', 'install', pip_pkg])
        print(s)
    print("Reloading python packages")

if __name__ == '__main__':

    try:
        print('prequistes python packages installation')
        install_packages()

    except Exception as e:
        print("Error while creating Google cloud function Server " ,e)
        f = open('FAILURE', 'w')
        f.write(str(e))
        f.close()
        time.sleep(30)
