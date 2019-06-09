#!/usr/bin/env python

import os
from subprocess import STDOUT, check_call
import pip
import sys
from util import *
from error_utils import ErrorUtils
import json

'''
    Required Google DNS Python Packages
'''
pip_sources = [
    "google-cloud-dns",
    "oauth2client"
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
    
    print "Prequistes success............."
    
    print_log("Initializing")
    install_packages()

    def check_mandatory_params():
        if not os.environ.get("CliqrCloud_JsonServiceAccount", False):
            print_error(ErrorUtils.mandatory_params_missing("ServiceAccount"), "ServiceAccount")
            sys.exit(127)

        if not os.environ.get("Cloud_Setting_projectName", False):
            print_error(ErrorUtils.mandatory_params_missing("ProjectName"), "ProjectName")
            sys.exit(127)

    check_mandatory_params()

except Exception as e:
    print_error(ErrorUtils.internal_error(e.message))
    write_error(e)

    sys.exit(127)
