
import os
import sys
from util import *
from lambda_management import LambdaManagement
import json

try:

    function_name = os.environ["functionName"]
    function_description = os.environ["functionDescription"]
    run_time = os.environ["runtimes"]
    app_package = os.environ["appPackage"]
    role_for_lambda=os.environ["roleForLambda"]
    dynamo_db_table_name = ""
    dependents = False
    if 'CliqrDependencies' in os.environ:
        dependents = os.environ.get('CliqrDependencies', "")
        if dependents:
            dynamo_db_table_name = os.environ.get('CliqrTier_'+dependents+'_tableName')

    if dependents == False:
	print_error("There is no depedency found to create the table.")
	sys.exit(127)
	
    print_log("table name ="+dynamo_db_table_name)
    if dynamo_db_table_name == "":
	print_error("There is no table found.")
	sys.exit(127)


    print_log(function_name)
    print_log(function_description)
    print_log(run_time)
    print_log(app_package)
    print_log(role_for_lambda)


except Exception as er:
    print_log("some of the parameters are not given properly...")
    print("my error",er)
    print_error("some of the parameters are not given properly.")

    sys.exit(127)


def get_package_base_name(appPackage):

    name_list=appPackage.split('/')
    package_zip=name_list[len(name_list)-1].split('.')
    return package_zip[0]


def start():

    object = LambdaManagement()

    app_package_base_name = get_package_base_name(app_package)

    handler = app_package_base_name + "/" + os.environ["initFile"] + "." + os.environ["invokeMethod"]

    app_package_local="/opt/remoteFiles/cliqr_local_file/"+app_package_base_name+".zip"

    fun_response = object.function_creation(function_name, run_time, handler, function_description, app_package_local,role_for_lambda)


    if fun_response["FunctionArn"] is not None:
        print_log("Lambda Function created.....")
    else:
        print_log("Lambda function creation failed.")

    trigger_response=object.event_source_mapping(fun_response["FunctionArn"], dynamo_db_table_name)

    trigger_uuid = trigger_response["UUID"]


    result = {
        "hostName": os.environ.get('appTierName', ""),
        "environment": {
            "trigger_uuid": trigger_uuid
        }
    }




def stop():

        object = LambdaManagement()

        trigger_uuid = os.environ.get("trigger_uuid", "")

        object.delete_trigger_mapping(trigger_uuid)

        object.delete_role_created(role_for_lambda)

        object.delete_lambda_function(function_name)






