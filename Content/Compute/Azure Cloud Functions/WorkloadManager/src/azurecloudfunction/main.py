import sys
import os
from azure_cloud_function import *
from util import *
from error_utils import ErrorUtils

OS_TYPE = 'Windows'
APP_NAME = os.environ['app_name']
RUNTIME = os.environ['runtime']
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
print_log(len(DEPENDENTS))
if(len(DEPENDENTS) > 0):
    DB_NAME = os.environ.get('CliqrTier_'+DEPENDENTS+'_dbName')
    DB_USERNAME = os.environ.get('CliqrTier_'+DEPENDENTS+'_serverUsername')
    DB_PASSWORD = os.environ.get('CliqrTier_'+DEPENDENTS+'_serverPassword')
    SERVER_NAME = os.environ.get('CliqrTier_'+DEPENDENTS+'_serverName')
else:
    DB_NAME = None
    DB_USERNAME = None
    DB_PASSWORD = None
    SERVER_NAME = None

arg1 = sys.argv[1]
print_log(arg1)
try:
    if arg1 == 'login':
        login(APP_ID, PASSWORD, TENANT_ID)
    elif arg1 == 'deploy':
        deploy_application(RESOURCE, APP_NAME, APP_PACKAGE, DEPENDENTS, DB_NAME, DB_USERNAME, DB_PASSWORD, SERVER_NAME)
    elif arg1 == 'create':
        create_function(APP_NAME, OS_TYPE, RESOURCE, RUNTIME, LOCATION, STORAGE_NAME)
    elif arg1 == 'resource':
        create_resource(RESOURCE, LOCATION)
    elif arg1 == 'storage':
        create_storage(STORAGE_NAME, RESOURCE, LOCATION)
except Exception as e:
    write_error(e)
    print_error(e)
    #sys.exit(127)

