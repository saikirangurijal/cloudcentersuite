import boto3
import base64
import time
import os
import sys
import json
from util import print_error,print_log,print_result,write_error
# External Life Cycle Action
# Start - Create Load Balancer and attach VMS

### AWS Conncetion ########
def aws_conncetion(env_data):
    '''
    :param env_data: 
    :return: 
    '''

    try:
        # boto3 client configuration
        client = boto3.client('dynamodb',aws_access_key_id=env_data["ACCESS_KEY"],aws_secret_access_key=env_data["SECRET_KEY"],region_name=env_data["region"])
        # boto3 resource configuration
        dynamodb = boto3.resource('dynamodb',aws_access_key_id=env_data["ACCESS_KEY"],aws_secret_access_key=env_data["SECRET_KEY"],region_name=env_data["region"])
        return dynamodb

    except Exception as err:
        #write_error(err)
        print_error(err)
        sys.exit(127)

### Start Functionality #####
def start(env_data, dynamodb):
    '''
    :param env_data:
    :param dynamodb:
    :return:
    '''
    print_log("Creating Table")
    try:
        table = dynamodb.create_table(
            TableName=env_data["tableName"],
            KeySchema=[
				{'AttributeName': env_data["Partitionkey"], 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
				{'AttributeName': env_data["Partitionkey"], 'AttributeType': env_data["AttributeType"]}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5},
            StreamSpecification={
                'StreamEnabled': env_data["StreamEnabled"],
                'StreamViewType': env_data["StreamViewType"]
            },
        )
        time.sleep(5)
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=env_data["tableName"])
        table = dynamodb.Table(env_data["tableName"])
        print_log("Table Created")
        # Insertion of  data
        print_log("Adding default items in table")
        table.put_item(
            Item={
                env_data["Partitionkey"]: env_data["value"]
            }
        )
        print_log("Items added in table.")
        response = {
            'tableName': env_data['tableName'],
            'region': env_data['region'],
            'param1': base64.b64encode(env_data['ACCESS_KEY']),
            'param2': base64.b64encode(env_data['SECRET_KEY']),

        }

        return response
    except Exception as err:
        print_error(err)
        sys.exit(127)
		
def stop(env_data, dynamodb):
    print_log('Deleting table')
    try:
        table = dynamodb.Table(env_data["tableName"])
        table.delete()
    except Exception as err:
        # write_error(err)
        print_error(err)
        sys.exit(127)



def main(cmd):
    """
        This is the function to create or delete the service action based on life cycle action command
        :param cmd:
        :return:
        """
    arguments = cmd
    db_password = ''

    try:
        # get environmantal data and stored in dict
        print_log("Getting environment variables")
        env_data = {}
        env_data["tableName"] = os.environ["tableName"]
        env_data["ACCESS_KEY"] = os.environ["CliqrCloudAccountPwd"]
        env_data["SECRET_KEY"] = os.environ["CliqrCloud_AccessSecretKey"]
        env_data["region"] = os.environ["region"]
        print_log("Start AWS Connection")
        dynamodb = aws_conncetion(env_data)
        print_log("AWS Connected")
        dependents = os.environ.get('CliqrDependencies', "")
        if arguments in "start":
            env_data["Partitionkey"] = os.environ["partitionKey"]
            env_data["AttributeType"] = os.environ["partitionAttrType"][0]
            env_data["StreamEnabled"] = bool(os.environ["streamEnabled"])
            env_data["StreamViewType"] = os.environ["streamViewType"]
            env_data["value"] = 'testuser' if env_data["AttributeType"] == 'S' else 1
            response = start(env_data, dynamodb)
            print_log("Table and Items Added Successfully!")
            json_result = {
                "hostName": dependents,
                "ipAddress": "",
                "environment": response
            }
            print_result(json.dumps(json_result))
        elif arguments in "stop":
            print_log("Deleting Table...")
            stop(env_data, dynamodb)
            print_log("Deleted Table")

    except Exception as er:
        print_error(er.message)
        f = open('FAILURE', 'w')
        f.write(str(er))
        f.close()
        print_error("Unable to get environmental variables")
        sys.exit(127)
