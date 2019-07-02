#! /usr/bin/env python
import os
import sys
import time
import json
from util import print_log, print_error, write_error
from azure.cli.core import get_default_cli

def login(app_id, password, tenant_id):
    '''AZURE LOGIN WILL BE DONE IN THIS FUNCTION'''
    azure_login_cmd = get_default_cli().invoke(['login','--service-principal', '--username', app_id, '--password', password, '--tenant', tenant_id])

def set_db_env(resource, app_name, db_name, db_username, db_password, server_name):
    '''Set Environment variables for db details for Azurecloud Function'''
    dbuser_env =  "dbUsername={}".format(db_username)
    dbpswd_env = "dbPassword={}".format(db_password)
    dbserver_env = "dbServerName={}".format(server_name)
    dbname_env = "dbName={}".format(db_name)
    get_default_cli().invoke(['functionapp', 'config', 'appsettings', 'set', '--name', app_name, '--resource-group', resource, '--settings', dbuser_env])
    get_default_cli().invoke(['functionapp', 'config', 'appsettings', 'set', '--name', app_name, '--resource-group', resource, '--settings', dbpswd_env])
    get_default_cli().invoke(['functionapp', 'config', 'appsettings', 'set', '--name', app_name, '--resource-group', resource, '--settings', dbserver_env])
    get_default_cli().invoke(['functionapp', 'config', 'appsettings', 'set', '--name', app_name, '--resource-group', resource, '--settings', dbname_env])

def create_function(app_name, os_type, resource, runtime, location, storage_name):
    '''Azure Fucntion app created'''
    languages = ['node', 'java', 'dotnet', 'powershell']
    if runtime in languages:
        if runtime != 'java':
            azure_functionapp = get_default_cli().invoke(['functionapp', 'create', '--resource-group', resource,
                                                      '--os-type', os_type, '--consumption-plan-location',
                                                      location,  '--runtime', runtime, '--name', app_name,
                                                      '--storage-account', storage_name])
        else:
            pass
    else:
        print_error("{} is not a valid runtime".format(runtime))

def create_resource(resource, location):
    '''Create resource group'''
    create_resource = get_default_cli().invoke(['group', 'create', '--name', resource, '--location', location])

def create_storage(storage_name, resource, location):
    '''Create storage'''
    print_log("creating Stroage")
    create_storage = get_default_cli().invoke(['storage', 'account', 'create', '--name', storage_name,
                                                            '--location', location, '--resource-group', resource
                                                            , '--sku', 'Standard_LRS'])

def get_package_base_name(app_package):
    '''Get the base name of app package'''
    name_list = app_package.split('/')
    package_zip = name_list[len(name_list) - 1].split('.')
    return package_zip[0]

def deploy_application(resource, app_name, app_package, dependents, db_name, db_username, db_password, server_name):
    '''Deploying zipcode to create function in Functionapp'''
    app_package_base_name = get_package_base_name(app_package)
    source_file_name = "/opt/remoteFiles/cliqr_local_file/" + app_package_base_name + ".zip"
    deploy_function_cmd = get_default_cli().invoke(['functionapp', 'deployment', 'source', 'config-zip',
                                      '-g', resource, '-n', app_name, '--src', source_file_name])
    print_log(len(dependents))
    if(len(dependents) > 0):
        set_db_env(resource, app_name, db_name, db_username, db_password, server_name)



