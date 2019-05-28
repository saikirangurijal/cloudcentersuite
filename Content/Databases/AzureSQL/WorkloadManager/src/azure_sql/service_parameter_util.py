#!/usr/bin/env python

import json
import os
import sys,time
from util import *
from error_utils import ErrorUtils

# Azure Account Parameters
account_params = {
    'CliqrCloudAccountId': "subscriptionId",
    'CliqrCloud_ClientId': "clientId",
    'CliqrCloud_ClientKey': "clientSecret",
    'CliqrCloud_TenantId': "tenantId",
    'region': "location"
}

#SQL Required parameters
mandatory_params = [
    "CliqrCloudAccountId",
    "CliqrCloud_ClientId",
    "CliqrCloud_ClientKey",
    "CliqrCloud_TenantId",
    "region",
    "resourceGroupName",
    "serverName",
    "serverUsername",
    "serverPassword",
    "dbName",
    "publicIP"
]

# Open Parameter Template and filling values
try:
    with open('params.json', 'r') as file:
        global params
        params = json.loads(file.read())
except IOError as ioerr:
    print_error(ErrorUtils.bundle_error(ioerr))
    write_error(ioerr)

    sys.exit(127)
except Exception as err:
    print_error(ErrorUtils.internal_error(err.message))
    write_error(err)
    sys.exit(127)

# Create Parameters JSON using Template
def create_params_json():
    # Account params
    print("inside create params method..")
    try:
        params['appTierName'] = os.environ.get("cliqrAppTierName", "")
        
        for k,v in account_params.items():
            params['account'][v] = os.environ[k]
            print(os.environ[k])
        print("all parameters collected..")

    except KeyError as kerr:
        print(kerr)
        print_log(kerr)
        print_error(ErrorUtils.mandatory_params_missing(kerr), kerr.message)
        write_error(kerr)

        sys.exit(127)

        return False
    except Exception as err:
        print_error(ErrorUtils.internal_error(err))
        write_error(err)
        print_log(err)
        print(err)
        sys.exit(127)

        return False

    # mandatory params
    try:
        dependents = os.environ['CliqrDependents']
        if len (dependents) == 0:
            print_error ("There is no dependent tier")
            print_log("There is no dependent tier")
            print("There is no dependent tier")
            sys.exit (127)

        #params['resourceGroup'] = os.environ['CliqrTier_' + dependents + "_Cloud_Setting_ResourceGroup"]  # Azure Resource Group
        #print(os.environ['CliqrTier_' + dependents + "_Cloud_Setting_ResourceGroup"])


        params['publicIP'] = os.environ['CliqrTier_' + dependents + "_PUBLIC_IP"]  # Public IP

        params['resourceGroup'] = os.environ['Cloud_Setting_ResourceGroup']
        print("resource group is ",os.environ['Cloud_Setting_ResourceGroup'])
        params['name']=os.environ['serverName']
        print(os.environ['serverName'])
        params['administrator_login']=os.environ['serverUsername']
        print(os.environ['serverUsername'])
        params['administrator_login_password']=os.environ['serverPassword']
        print(os.environ['serverPassword'])
        params['dbName']=os.environ['dbName']
        print(os.environ['dbName'])
        time.sleep (130)

    except Exception as err:
        print("Some of the parameters are not given properly.")
        print_error("Some of the parameters are not given properly.")
        write_error(err)
        print(err)
        sys.exit(127)


    with open('params.json', 'w') as file:
        file.write(json.dumps(params))

    print_log("Updating Configuration.")

    return True



    
    







