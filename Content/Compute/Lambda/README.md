# AWS Lambda
## Introduction

	AWS Lambda is a compute service that lets you run code without provisioning or managing servers.
	
	It is a computing service that runs code in response to events and automatically 
	manages the computing resources required by that code.

	Please refer the below link for more details.
	For your reference : https://docs.aws.amazon.com/lambda/latest/dg/welcome.html
	
## Pre-Requisites

#### CloudCenter
- CloudCenter 5.x.x and above.
- Knowledge on how to use Workload Manager. 
- Deployment Package(appPackage)-Lambda function package with proper handler in your apps repository.

## Before you start
### Docker Installation
Before you start with service import, Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

### DynamoDB Import
Before importing the lambda service, user must import dynamodb service in workload manager because Lambda function will be invoked on dynamo db table events (Any CRUD operation).
      
Refer Readme on how to import Dynamo DB Service from [here](https://github.com/datacenter/cloudcentersuite/blob/master/Content/NoSQL%20Databases/DynamoDB/README.md).
      
The lambda service will create a lambda function with provided name in AWS.

How it works :
- Once application deployed successfully user can access sample php application(which writes data into the aws dynamodb). 
- When user writes an item into a table(users), A new stream record is written to reflect that a new item has been added to the table.
- The new stream record triggers an AWS Lambda function(TestLambdaFunction).
- If the stream record indicates that a new item is added to table then lambda function will add two fields(Triggered On,UUID) to the existing item of the table
    (Triggered On indicates time of update and UUID is an unique id of the user created from lambda function).
- User can find the details of his entry with 'Triggered on' and 'UUID' from Find User functionality of sample php application.

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to execute "yum install wget -y" in case of centos7.

	    Example: 
      wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.


##### PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip(s) on client machine. The files must be copied on to the repository before proceeding to deploy.
          
           - Service Bundle under <service_path>/<your_bundle_name>
                    
                    Example : http://<Your_REPO_Server_IP>/<service_path>/aws_lambda.zip 
    
            - Application Bundle under <app_path>/<your_package_name>
            
                    Example : http://<Your_REPO_Server_IP>/<app_path>/lambda.zip
              
                    Example : http://<Your_REPO_Server_IP>/<app_path>/lambda-dynamodb-php-app.zip
                                        

## Service Package Bundle

Shell script:
 - service: Initiates the python script to start integration.

Python script :
 - install_setup.py: The script will check all mandatory parameters available and install necessary python packages also invokes external life cycle action.
 - main.py:script will get required environment variables and execute the required functionalities. 
 - lambda_management.py: script that invokes the api for aws_lambda and creates the lambda function with provided deployment package.
 - util.py: utility file.

## External Lifecycle Actions
External Action Bundle:  services/aws_lambda.zip

External Lifecycle Actions: 
 - Start: Script from bundle: **service start**
 - Stop: Script from bundle: **service stop** 

# Service Parameters:
| Parameter Name| Type	 | Mandatory |Description | Allowed Value |Default Value |
| ------ | ------ | ------ | ------ |------ | ------ |
| appPackage | Path |	Yes |Path of the Deployment Package(.zip). | | |
| initFile | String | Yes | File name of lambda function zipped in appPackage. |  | |
| invokeMethod | String | Yes | Lambda Handler Name where lambda functions starts execution. |  | |
| runtimes | List | Yes | Need to select required Run time for the lambda function. |  | |


# Deployment Parameters:
| Parameter Name| Type	 | Mandatory |Description | Allowed Value |Default Value |
| ------ | ------ | ------ | ------ |------ | ------ |
| roleForLambda |	String | Yes | A role will be created for lambda with dynamodb access policy attached.|  | RoleForLambda   |
| functionName |	String | Yes | Name of the lambda function to be created. |  | TestLambdaFunction   |
| functionDescription | String | No	| Description for the lambda function. |  | Sample lambda function |