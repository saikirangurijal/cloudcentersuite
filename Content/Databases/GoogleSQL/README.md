# Google Cloud SQL

## Introduction

    The Workload Manager platform supports integration to various Database layers as an external service.

    This document provides information on Google Cloud SQL integration with Cisco Workload Manager by creating an 
    external service.

    Google Cloud SQL platform gives you the ability to manage the database.

    Please refer the below link for more details.

    https://cloud.google.com/sql/docs/
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use CloudCenter

## Download the service bundles

 Step 1 : Download the Service Bundle zip from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Databases/GoogleSQL/WorkloadManager/ServiceBundle/googlesql.zip). 
   
 Step 2 : Download the application bundle to be used with application profile from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Databases/GoogleSQL/WorkloadManager/ApplicationProfiles/artifacts/googlesql-petclinic-app.zip).
   
 Step 3 : Place the service bundle from Step 1 under services/<bundle.zip> and application bundle from Step 2 under apps/<your_package_name> in your file repository.
          
            - Service Bundle under services/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/services/googlesql.zip 
    
            - Application Bundle under apps/<your_package_name>
            
                    Example : http://<Your_REPO_Server_IP>/apps/googlesql-petclinic-app.zip
   
 Step 4 : Download the integration unit bundle (that conatins logo, service json and application profile) from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Databases/GoogleSQL/WorkloadManager/googlesql_iu.zip)
 
 Step 5: Extract the above bundle on any linux based machine and navigate to extracted folder

 Step 6 : Download the Service Import script zip file from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Scripts/serviceimport.zip) 
 
 Step 7: Copy the Service Import script zip file to the directory extarcted above in Step 5 and Unzip the service import script bundle.

 Step 8 : Download the Dockerfile from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Dockerfile) and copy to the extracted folder in Step 5
 
 ##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier
   
 Ensure your directory in the linux based client machine contains :

- Service import json file (named as googlesql_service.json)
- Service import script zip file (named as serviceimport.zip)
- main.py file
- serviceimport.sh
- Google SQL logo (named as logo.png)
- Modelled application profile(named as googlesql_sample_app.zip)
- Dockerfile (named as Dockerfile) , **Only needed if you wish to create a Docker image for the first time**
   
## How to Create a Service in Cisco Workload Manager

User can create the service by using **Import Service** functionality using script.

#### Prerequisite for creating a service through service import script:

Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx) on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running docker -v
- You can check , if docker is running , by executing the command "systemctl status docker"
  
#### Detailed steps for creating a service through the service import script:

##### Step 1 :Provide executable permissions to the above files. Navigate to the directory where all the files are placed and run the below command:
   
    chmod 755 <your file>
    
    
Example : 
    [root@ip-172-31-27-127 googlesql]# chmod 755 googlesql_service.json serviceimport.zip logo.png googlesql_sample_app.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

    [root@ip-172-31-27-127 googlesql]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

    [root@ip-172-31-27-127 googlesql]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

    docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it 
    **[Your IMAGE ID]** /bin/bash

Example:  

[root@ip-172-31-27-127 googlesql]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Where to Download The Service Bundles". 

    - Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"Google SQL Service imported successfully. Imported Application Profile Successfully"**

## Service Package Bundle

The Package Service bundle consists of the following files:

Shell script:

- service: Intiates the python script to start intergration.

Python script :

- install_setup.py: The script will installs necessary python packages also invokes external life cycle action.

- google_sql.py : The script will invoke the creation and deletion service based on user selection type (MYSQL/POSTGRESQL) using google management client.

- google_management_client.py : The script will invoke the main method of google cloud sql.

- common.py: The script contains common functionalities which is required for other script files.

- util.py: utility file

- error_utils.py: The script that handles error functionalities

## External Lifecycle Actions 

External Action Bundle:  
 - http://YourIP/services/googlesql.zip - Location where your external action bundle zip (service bundle zip file) is found.
 
External Lifecycle Actions: 
 - Start: Script from bundle: **service start**
 - Stop: Script from bundle: **service stop** 

#  Deployement Parameters:

| Parameter Name | Type | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| geSqlType | List | Type of Sql. For more details on the type of sql to choose, check Google cloud documentation | MYSQL, POSTGRESQL | MYSQL| 
| geInstanceName | String | Instance names to be configured for the service. Ensure the instance name is  not available in cloud and can't use the same instance name even though deleted in cloud until 2 months.|


#  Service Parameters:

| Parameter Name | Type | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| geDbUserName | String | Database username to be configured for the service. | User Defined Value | petclinic |
| geDbPassword| Password | Database password to be configured for the service. |
| geDbName | String | Database name to be configured for the service.| User Defined Value | petclinic |
| geDbHost | String | Database host to be configured for the service.| % | %



