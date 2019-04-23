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
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager
- Table name should be unique
	
## Download the service bundles

 Step 1 : Download the Service Bundle zip from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/NoSQL%20Databases/DynamoDB/WorkloadManager/ServiceBundle/dynamodb.zip). 
   
 Step 2 : Download the application bundle to be used with application profile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/NoSQL%20Databases/DynamoDB/WorkloadManager/ApplicationProfiles/artifacts/dynamodb-php-app.zip).
   
 Step 3 : Place the service bundle from Step 1 under services/<bundle.zip> and application bundle from Step 2 under apps/<your_package_name> in your file repository.
          
            - Service Bundle under services/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/services/dynamodb.zip 
    
            - Application Bundle under apps/<your_package_name>
            
                    Example : http://<Your_REPO_Server_IP>/apps/dynamodb-php-app.zip
   
 Step 4 : Download the integration unit bundle (that contains logo, service json and application profile) from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/NoSQL%20Databases/DynamoDB/WorkloadManager/dynamodb_iu.zip  )
 
 Step 5: Extract the above bundle on any linux based machine and navigate to extracted folder

 Step 6 : Download the Service Import script zip file from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip) 
 
 Step 7: Copy the Service Import script zip file to the directory extracted above in Step 5 and Unzip the service import script bundle.

 Step 8 : Download the Dockerfile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Dockerfile) and copy to the extracted folder in Step 5
 ##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier
   
 Ensure your directory in the linux based client machine contains :

- Service import json file (named as dynamodb_service.json)
- Service import script zip file (named as serviceimport.zip)
- main.py
- serviceimport.sh
- DynamoDB logo (named as dynamodb.png)
- Modelled application profile(named as dynamodb_sample_app.zip)
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
   
    chmod 755 <your file> or chmod 755 *
    
    
Example : 
    [root@ip-172-31-27-127 dynamodb]# chmod 755 dynamodb_service.json serviceimport.zip dynamodb.png dynamodb_sample_app.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

    [root@ip-172-31-27-127 dynamodb]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

    [root@ip-172-31-27-127 dynamodb# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

    docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it 
    **[Your IMAGE ID]** /bin/bash

Example:  

[root@ip-172-31-27-127 dynamodb]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Where to Download The Service Bundles". 

    - Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"Dynamo DB Service imported successfully. Imported Application Profile Successfully"**


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

