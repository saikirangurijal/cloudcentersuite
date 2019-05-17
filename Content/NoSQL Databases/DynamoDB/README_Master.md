# DynamoDB
## Introduction
    The  Workload Manager platform supports integration to various NoSQL database as an external service.
    This document provides information on DynamoDB integration with Cisco Workload Manager 
    by creating an external service.
    
    DynamoDB is a fully managed NoSQL database service that provides fast and predictable performance with seamless scalability. 
    
    The service which we have created will support Dynamo DB to create tables or can use existing table by giving table name in deployment parameters that can store and retrieve any amount of data, and serve any level of request traffic.
    
    Please refer the below link for more details.
    https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager
- Table name should be unique
	
#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.

	    Example: 
       wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.

##### PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <services_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/dynamodb.zip 
    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/dynamodb-php-app.zip

## Service Package Bundle

The Packer Service bundle consists of the following files:

Shell script:
 - service: The script will set all required environmental variables and installs necessary packages also invokes all external life cycle action.

Python script :

 - install_setup.py: The script will installs necessary python packages also invokes external life cycle action.

 - main.py : The script that invokes creation, deletion and fetch the details of dynamo tables.

 - util.py: utility file

 - error_utils.py: The script that handles error functionality

## External Lifecycle Actions 

External Action Bundle:  
 - http://YourIP/services/dynamodb.zip the external action bundle zip file is found.
 
External Lifecycle Actions:
 - Start: Script from bundle : **service start** 
 - Stop: Script from bundle : **service stop**

		
## Service parameters


| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| partitionKey | string| Primary key for the table | User defined value | id |
| partitionAttrType | list| Type of attribute. For more details on the type of attribute, check DynamoDB documentation	 | Number,String,Binary | String |
| streamEnabled | list| Stream enable for the table | True,False | True |
| streamViewType | list | Stream View Type | NEW_IMAGE,OLD_IMAGE,NEW_AND_OLD_IMAGES,KEYS_ONLY | NEW_AND_OLD_IMAGES |

## Deployment parameters


| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| tableName |	string | Table name to be configured for the service.	 | User defined value | users |

