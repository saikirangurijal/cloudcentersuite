# AWS Lambda
## Introduction

	AWS Lambda is a compute service that lets you run code without provisioning or managing servers.
	
	It is a computing service that runs code in response to events and automatically 
	manages the computing resources required by that code.

	Please refer the below link for more details.
	For your reference : https://docs.aws.amazon.com/lambda/latest/dg/welcome.html
	
## Before you start	
Before importing the lambda service, user must import dynamodb service in workload manager because Lambda function will be invoked on dynamo db table events (Any CRUD operation).
      
Refer Readme on how to import Dynamo DB Service from [here](https://github.com/datacenter/cloudcentersuite/blob/master/Content/NoSQL%20Databases/DynamoDB/README.md).
      
The lambda service will create a lambda function with provided name in AWS.

#####How it works :
- Once application deployed successfully user can access sample php application(which writes data into the aws dynamodb). 
- When user writes an item into a table(users), A new stream record is written to reflect that a new item has been added to the table.
- The new stream record triggers an AWS Lambda function(TestLambdaFunction).
- If the stream record indicates that a new item is added to table then lambda function will add two fields(Triggered On,UUID) to the existing item of the table
    (Tiggered On indicates time of update and UUID is an unique id of the user created from lambda function).
- User can find the details of his entry with Triggered on and UUID from Find User functionality of sample php application.

	
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above.
- Knowledge on how to use Workload Manager. 
- Deployment Package(appPackage)-Lambda function package with proper handler in your apps repository.
 

## Download the service bundles

Step 1 : Download the service bundle from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Compute/Lambda/WorkloadManager/ServiceBundle/aws_lambda.zip)

Step 2 : Download the application bundles to be used with application profile for dynamodb from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Compute/Lambda/WorkloadManager/ApplicationProfiles/artifacts/dynamodb-lambda-php-app.zip) and
         for lambda from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Compute/Lambda/WorkloadManager/ApplicationProfiles/artifacts/lambda.zip).

Step 3 : Place the service bundle from Step 1 under services/<bundle.zip> and application bundles from Step 2 under apps/<your_package_name> in your file repository.
          
           - Service Bundle under services/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/services/aws_lambda.zip 
    
            - Application Bundle under apps/<your_package_name>
            
                    Example : http://<Your_REPO_Server_IP>/apps/lambda.zip
              
                    Example : http://<Your_REPO_Server_IP>/apps/dynamodb-lambda-php-app.zip
                                        
		
Step 4 : Download the integration unit bundle (that contains logo, service json and application profile) from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Compute/Lambda/WorkloadManager/lambda_iu.zip)

Step 5 : Extract the above bundle on any linux based machine and navigate to extracted folder

Step 6 : Download the Service Import script zip file from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip) 

Step 7: Copy the Service Import script zip file to the directory extracted above in Step 5 and Unzip the service import script bundle.

Step 8 : Download the Dockerfile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Dockerfile) and copy to the extracted folder in Step 5
 
##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier
   
 Ensure your directory in the linux based client machine contains :

- Service import json file (named as lambda_service.json)
- Service import script zip file (named as serviceimport.zip)
- main.py file
- serviceimport.sh
- lambda logo (named as logo.png)
- Modelled application profile(named as lambda_sample_app.zip)
- Dockerfile (named as Dockerfile) , **Only needed if you wish to create a Docker image for the first time**

## How to Create a Service in Cisco Workload Manager

User can create the service by using **Import Service** functionality using script.

#### Prerequisite for creating a service through service import script:

Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx) on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running docker -v
- You can check , if docker is running , by executing the command "systemctl status docker"
  
#### Detailed steps for creating a service through the service import script:

##### Step 1 :Provide executable permissions to the above files. Navigate to the directory where all the files are placed and run the below command:
   
   chmod 755 <your file>

Example : 
    [root@ip-172-31-28-215 lambda]# chmod 755 lambda_service.json serviceimport.zip logo.png lambda_sample_app.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

###### [root@ip-172-31-28-215 lambda]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

[root@ip-172-31-28-215 lambda]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

    docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it 
    **[Your IMAGE ID]** /bin/bash

Example:  

[root@ip-172-31-28-215 lambda]# docker run -v **[Your directory]**:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Where to Download The Service Bundles". 

    - Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"lambda Service imported successfully. Imported Application Profile Successfully"**


### The Packer Service bundle consists of the following files:

Shell script:
 - service: Initiates the python script to start integration.

Python script :
 - install_setup.py: The script will check all mandatory parameters available and installs necessary python packages also invokes external life cycle action.
 - main.py:script will get required environment variables and execute the required functionalities. 
 - lambda_management.py: script that invokes the api for aws_lambda and creates the lambda function with provided deployment package.
 - util.py: utility file.

# External Lifecycle Actions as below
    - External Action Bundle:  services/aws_lambda.zip
    - External Lifecycle Actions:
        Start:
            Script from bundle: service start
        Stop:
            Script from bundle: service stop

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

