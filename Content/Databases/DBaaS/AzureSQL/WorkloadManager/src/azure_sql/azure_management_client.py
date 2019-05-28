#!/usr/bin/env python
# Azure Management Client
# Construct Azure Client with Credentials
# Create Resource Management Client Object
# Create SQL Management Client Object

import os
import json
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.resource import ResourceManagementClient
from haikunator import Haikunator
import sys
from util import *
from azure_sql import AzureSQL
from error_utils import ErrorUtils



'''
    Load Parameters
'''
try:
    with open('params.json', 'r') as file:
        global params
        params = json.loads(str(file.read()), object_pairs_hook=deunicodify_hook)

        print(params)
except Exception as err:
    print_error(ErrorUtils.internal_error(err))
    sys.exit(127)

'''
    Azure Management Client
'''
class AzureManagement(object):
    def __init__(self):
        #
        # Initialize Azure Basic Setup
        #
        print(params['account'])
        self.location = params['account']['location']
        self.group_name = params['resourceGroup']

        self.subscription_id = params['account']['subscriptionId']

        print("client_id",params['account']['clientId'])
        _client_id = params['account']['clientId']
        _secrete=params['account']['clientSecret']
        _tenant=params['account']['tenantId']

        print(_client_id)
        print(_secrete)
        print(_tenant)
        self.credentials = ServicePrincipalCredentials(
            client_id=_client_id,
            secret=_secrete,
            tenant=_tenant
        )
        try:
            self.resource_mgmt = ResourceManagementClient(self.credentials, self.subscription_id)
            self.sql_mgmt = SqlManagementClient(self.credentials, self.subscription_id)

            self.params = params

            self._azure_sql_conn = AzureSQL(self.location, self.subscription_id, params)

            self._azure_sql_conn.client = self


            print("Connected. ")
            print_log("Connected.")
        except Exception as er:
            print_error("Cloud connection failed.")
            print_log(err)


    @property
    def azure_sql_conn(self):
        # Get SQL Object
        return self._azure_sql_conn
       
        


      
