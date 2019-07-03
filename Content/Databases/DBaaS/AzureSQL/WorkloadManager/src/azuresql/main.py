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
    print(err)
    write_error(err)
    print_error(ErrorUtils.internal_error(err.message))

    sys.exit(127)

# External Life Cycle Action
# Start - Create SQL Server and Database
def start():
    try:
        print_log("starts")
        result = azure_mgmt_instance.azure_sql_conn.create()

    except Exception as err:
        print_error(err)
        write_error(err)
        sys.exit(127)


def stop() :
    try:
        print("Stop")
        result = azure_mgmt_instance.azure_sql_conn.delete()
    except Exception as err:
        write_error(err)
        print_log(err)
        sys.exit(127)


