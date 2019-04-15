#!/usr/bin/env python

# External Life Cycle Action Invocation

from azure_management_client import AzureManagement
import sys
from util import *
from msrest.exceptions import AuthenticationError
from error_utils import ErrorUtils
import json

# Create Azure Management Object with credentials
try:
    azure_mgmt_instance = AzureManagement()
except AuthenticationError as aerr:
    write_error(aerr)
    print_error(ErrorUtils.api_error("AuthenticationError", aerr.message))

    sys.exit(127)
    
except Exception as err:
    write_error(err)
    print_error(ErrorUtils.internal_error(err.message))

    sys.exit(127)

# External Life Cycle Action
# Start - Create Load Balancer and attach VMS
def start():
    try:
        result = azure_mgmt_instance.load_balancer.create()
        print_result(json.dumps(result))
    except Exception as err:
        write_error(err)
        sys.exit(127)

# Stop - Delete Load Balancer and Dettach VMS
def stop() :
    try:
        result = azure_mgmt_instance.load_balancer.delete()
        print_result(json.dumps(result))
    except Exception as err:
        write_error(err)
        sys.exit(127)
    



