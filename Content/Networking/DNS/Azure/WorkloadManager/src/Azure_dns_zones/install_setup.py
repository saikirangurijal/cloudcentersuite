# !/usr/bin/env python
import os
from subprocess import STDOUT, check_call
import sys,time
from util import print_error,print_log,print_result

"""
boto3 amazon cloud python packages installation part. 
"""

command = sys.argv[1]

pip_sources = [
    'azure'
    ]

def install_packages():
    """
    Installing  python packages for accessing amazon cloud
    :return:
    """

    try:
        print("Installing packeges.")
        print_log("Initiated...")
        global pip_sources

        for pip_pkg in pip_sources:
            s = check_call([sys.executable, '-m', 'pip', 'install', pip_pkg])
            print s
        print("Reloading python packages")
        return True
    except Exception as err:
        print(err)
        print_log(err)
        sys.exit(127)


if __name__ == '__main__':
    # install_packages()
    # if install_packages():
    #     print_log("Azure Sdk installed successfully.")
    #     from azure_dns_management import mainmethod
    #     mainmethod(command)

    try:
        print('prequistes python packages installation')
        install_packages()
        if install_packages():
            print_log("Azure Sdk installed successfully.")
            from azure_dns_management import main
            main(command)

    except Exception as e:
        print("Error while installing python package. " ,e)
        f = open('FAILURE', 'w')
        f.write(str(e))
        f.close()
        time.sleep(30)