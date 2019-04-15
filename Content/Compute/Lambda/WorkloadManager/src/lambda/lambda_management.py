import boto3
import sys,os,time,json
from util import print_log, print_error, print_result

class LambdaManagement(object):

    def __init__(self):
        """
        Initiallization for AWS cloud access using AccessKey ,SecreteKey and RegionName.
        """
        try:
            cliqr_cloud_account_pwd = os.environ["CliqrCloudAccountPwd"]
            cliqr_cloud_access_secret_key = os.environ["CliqrCloud_AccessSecretKey"]
            region_name = os.environ["region"]


            self.client_lambda = boto3.client('lambda', aws_access_key_id=cliqr_cloud_account_pwd,
                                              aws_secret_access_key=cliqr_cloud_access_secret_key,
                                              region_name=region_name)

            self.client_dynamodb = boto3.client('dynamodb', aws_access_key_id=cliqr_cloud_account_pwd,
                                                aws_secret_access_key=cliqr_cloud_access_secret_key,
                                                region_name=region_name)

            self.client_iam = boto3.client('iam', aws_access_key_id=cliqr_cloud_account_pwd,
                                           aws_secret_access_key=cliqr_cloud_access_secret_key,
                                           region_name=region_name)

            print("AWS Connection Succeded.")
            print_log("AWS Connection Succeded.")

        except Exception as er:
            print_error(er)
            sys.exit(127)

    def function_creation(self,function_name,run_time,handler,function_description, app_package_local):
        """
        method to create lambda function with the provided values

        :param:iamRoleName,functionName,runTime,handler,functionDescription
        :return:method response
        """
        try:

            print("Lambda function creation under progress.......")
            print_log("Lambda function creation under progress.......")

            role_arn=self.creating_role_attach_policy()
            time.sleep(30)
            print_log(role_arn)
            print(role_arn)

            if not app_package_local:
                print_error("Application Package Not Available")
                sys.exit(127)

            response= self.client_lambda.create_function(
                    FunctionName=function_name,
                    Runtime=run_time,Role=role_arn,

                    #need to know how to give deployment location
                    Code={
                        'ZipFile': open(app_package_local, 'rb').read()

                    },
                    Handler=handler,
                    Description=function_description,
                    Timeout=123,
                    Publish=True)
            if response is not None:
                print("Lambda function created.")
                print_log("Lambda function created.")

            return response

        except Exception as err:
            print_error(err)
            sys.exit(127)


    def find_stream_arn(self,table_name):
        """
        method to find the stream arn of the dynamo db table with the provided table name as input

         :param table_name:
         :return:
        """
        try:
           response = self.client_dynamodb.list_tables()
           print_log(response)
           table_names_list = response.get('TableNames')
           print_log(table_names_list)

           if table_name in table_names_list:
               print_log("In the loop for finding the stream arn")
               table_response = self.client_dynamodb.describe_table(TableName=table_name)
               print(table_response)
               is_stream_enabled = table_response.get('Table', {}).get('StreamSpecification', {}).get('StreamEnabled', None)
               print(is_stream_enabled)

               if is_stream_enabled:
                   table_stream_arn=table_response.get('Table',{}).get('LatestStreamArn',None)
                   print("table stream arn is")
                   print(table_stream_arn)

                   return table_stream_arn
               else:
                    print("Stream functionaliity on dynamodb table is disabled.")
                    print_log("Stream functionaliity on dynamodb table is disabled.")

           else:
               print_log("Specified tabled is not found.")

        except Exception as er:
            print_error(er)
            sys.exit(127)

    def event_source_mapping(self, function_arn,dynamodb_table_name):
        """
        method to trigger aws lambda function with the detection of change in stream of dynamo db table

        :param function_arn:
        :param dynamodbTableName:
        :return:
        """
        try:
             # lambdaclient = self.client_lambda.client('lambda',region_name="Ohio"
            db_stream_arn = self.find_stream_arn(dynamodb_table_name)
            print(db_stream_arn)
            print_log(db_stream_arn)
            response = self.client_lambda.create_event_source_mapping(

                EventSourceArn=db_stream_arn,
                FunctionName=function_arn,
                Enabled=True,
                BatchSize=123,
                StartingPosition='LATEST' or 'AT_TIMESTAMP'

            )

            print('Event source mapping done.')
            print_log("Event source mapping done.")
            return response
        except Exception as er:
            print_error(er)
            sys.exit(127)

    def delete_lambda_function(self,function_name):
        """
        method to delete the lambda function

        :param function_name:
        :return:
        """

        try:
            response = self.client_lambda.delete_function(
                FunctionName=function_name,
            )

            print("Function deleted. ")
            print_log("Function deleted. ")
        except Exception as er:
            print_error(er)
            sys.exit(127)


    def creating_role_attach_policy(self):
        """
        Method for creating a role dynamically for aws lambda service and attaching suitable policy(policy which will give access the dynamo db streams)
        :return:
        """
        try:

            data = {
                'Version': '2012-10-17',
                'Statement': {
                    'Effect': 'Allow',
                    'Principal': {
                        'Service': 'lambda.amazonaws.com'
                    },
                    'Action': 'sts:AssumeRole'
                }
            }
            role_response=self.client_iam.create_role(

                RoleName='dynamic_lambda_role',
                AssumeRolePolicyDocument=json.dumps(data),
                Description='Role created from the API'
                )
            response= self.client_iam.attach_role_policy(
                RoleName='dynamic_lambda_role',
                PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccesswithDataPipeline'
            )

            role_arn=role_response.get("Role",{}).get("Arn",None)

            return role_arn
        except Exception as er:
            print(er)
            print_error(er)

    def delete_role_created(self):
        """
        Method to delete the role which  we created during the creation of the lambda function
        :return:
        """
        try:
            policy_d_response = self.client_iam.detach_role_policy(
                RoleName='dynamic_lambda_role',
                PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccesswithDataPipeline'
            )
            print("policy ditached")
            response = self.client_iam.delete_role(
                RoleName='dynamic_lambda_role'
            )
            print("role deleted....")
            print_log("policy ditached...role deleted...")
        except Exception as er:
            print(er)
            print_error(er)

    def delete_trigger_mapping(self, trigger_uuid):
        """
        Method to delete the event source mapping for the lambda function
        :param trigger_uuid:
        :return:
        """
        try:
            response = self.client_lambda.delete_event_source_mapping(
                UUID=trigger_uuid
            )
            print("trigger disabled.....")
            print_log("trigger disabled for the function")
        except Exception as er:
            print(er)
            print_error(er)


