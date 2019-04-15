#!/usr/bin/env python

import os
from subprocess import STDOUT, check_call
import pip
import sys
from util import *

'''
    Required AWS Python Packages
'''
pip_sources = [
    'boto3'
]

cmd = sys.argv[1]

# Install Python Packages
try:
    from pip import main
except ImportError as err:
    from pip._internal import main


def install_packages():
    global pip_sources
    main(['install'] + pip_sources)


# Validate Mandatory parameters
# Invoke External LifeCyle Actions
try:
    print_log("Initializing")
    install_packages()

    from main import start, stop

    if cmd in "start":
        start()
    elif cmd in "stop":
        stop()
    else:
        sys.exit(127)

except Exception as e:
    write_error(e)
    sys.exit(127)