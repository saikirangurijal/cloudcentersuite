#!/usr/bin/env python3
import sys
import os
from azure_webapp import *
from util import *
from error_utils import ErrorUtils

OS_TYPE = 'Windows'
APP_NAME = os.environ['app_name']
RUNTIME = os.environ.get('runtime', '')
APP_PACKAGE = os.environ["AppPackage"]
RESOURCE = os.environ["Cloud_Setting_ResourceGroup"]
LOCATION = os.environ["region"]
store = (os.environ["Cloud_Setting_StorageAccount"]).split(' ')
STORAGE_NAME = store[1]
print_log(STORAGE_NAME)
APP_ID = os.environ["CliqrCloud_ClientId"]
TENANT_ID = os.environ["CliqrCloud_TenantId"]
PASSWORD = os.environ["CliqrCloud_ClientKey"]
DEPENDENTS = os.environ.get('CliqrDependencies', '')
WEB_RESOURCE =  os.environ["CliqrCloud_ClientId"] + "_rg_Linux_centralus"
print_log(len(DEPENDENTS))
if(len(DEPENDENTS) > 0):
    DB_NAME = 'azure'
    DB_USERNAME = 'azuser'
    DB_PASSWORD = 'admin@123'
    DB_HOST = os.environ.get('CliqrTier_'+DEPENDENTS+'_PUBLIC_IP')
else:
    DB_NAME = None
    DB_USERNAME = None
    DB_PASSWORD = None
    DB_HOST = None
print_log(DB_NAME)
print_log(DB_USERNAME)
print_log(DB_PASSWORD)
print_log(DB_HOST)
print_log(RUNTIME)


arg1 = sys.argv[1]
print_log(arg1)
try:
    if arg1 == 'login':
        login(APP_ID, PASSWORD, TENANT_ID)
    elif arg1 == 'createweb':
        create_webapp(APP_NAME, APP_PACKAGE, WEB_RESOURCE, DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, DEPENDENTS)
    elif arg1 == 'resource':
        create_resource(RESOURCE, LOCATION)
    elif arg1 == 'storage':
        create_storage(STORAGE_NAME, RESOURCE, LOCATION)
except Exception as e:
    write_error(e)
    print_error(e)
    #sys.exit(127)
