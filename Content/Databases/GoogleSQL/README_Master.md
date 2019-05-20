# Google Cloud SQL

## Introduction

    The Workload Manager platform supports integration to various Database layers 
    as an external service.

    This document provides information on Google Cloud SQL integration with Cisco
    Workload Manager by creating an external service.

    Google Cloud SQL platform gives you the ability to manage the database.

    Please refer the below link for more details.

    https://cloud.google.com/sql/docs/
## Pre-Requisites

#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to add "yum install wget -y" in case of centos7.

	    Example: 
<<<<<<< HEAD
        wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
=======
      wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
>>>>>>> 9e8504c298ad8e3b5ca87f9b49e331e6f5f35dc3
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.


##### PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/googlesql.zip 
    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/googlesql-petclinic-app.zip
   
## Service Package Bundle

The Package Service bundle consists of the following files:

Shell script:

- service: Initiates the python script to start integration.

Python script :

- install_setup.py: The script will install necessary python packages also invokes external life cycle action.

- google_sql.py : The script will invoke the creation and deletion service based on user selection type (MYSQL/POSTGRESQL) using google management client.

- google_management_client.py : The script will invoke the main method of google cloud sql.

- common.py: The script contains common functionality which is required for other script files.

- util.py: utility file

- error_messages.json : Json file contains error messages.

- error_utils.py: The script that handles error functionality

## External Lifecycle Actions 

External Action Bundle:  
 - http://YourIP/services/googlesql.zip - Location where your external action bundle zip (service bundle zip file) is found.
 
External Lifecycle Actions: 
 - Start: Script from bundle: **service start**
 - Stop: Script from bundle: **service stop** 

#  Deployment Parameters:

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


