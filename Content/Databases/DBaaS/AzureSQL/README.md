# Azure SQL Database

## Introduction

    The Workload Manager supports integration to Azure SQL database as an external service.
    This document provides information on Azure SQL integration with Workload Manager 
    by creating an external service.

    Please refer the below link for more details.

    https://docs.microsoft.com/en-us/azure/sql-database/sql-database-single-index
## Pre-Requisites

#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to add "yum install wget -y" in case of centos7.

	    Example: 
        wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.


##### PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/azureesql.zip 
    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/azuresql_app.war
   
## Service Package Bundle

The Package Service bundle consists of the following files:

Shell script:
 - service: Initiates the python script to start integration.

Python script :
 - install_setup.py: The script will check all mandatory parameters available and installs necessary python packages also invokes external life cycle action.
 - service_parameter_util.py: script that checks all mandatory parameters available and create a parameter json file.
 - main.py: This script will have all lifecycle actions.
 - azure_management_client.py: Script that creates an azure client for managing SQL using Azure SDK REST API
 - azure_sql.py: A script that invokes creation, deletion and fetch the details of SQL service using azure management client.
 - util.py: utility file
 - error_utils.py: A script that handles error functionalities
 
Other Files:
 - error_messages.json: Custom error message for load balancer
 - params.json: JSON Template of Azure Load Balancer Configuration

## External Lifecycle Actions 

External Action Bundle:  
 - http://YourIP/services/azuresql.zip - Location where your external action bundle zip is found.

External Lifecycle Actions:
 - Start: Script from bundle: **service start**
 - Stop: Script from bundle: **service stop**

#  Deployment Parameters:

| Parameter Name| Type	 | Mandatory |Description | Allowed Value |Default Value |
| ------ | ------ | ------ | ------ |------ | ------ |
| serverName|	String | Yes |Name of the SQL server going to be created.|  | contentfactory   |
| dbName |	String | Yes | Name of the SQL database going to be created. |  | testcliqrdb   |
| serverUsername | String | Yes	|  Database server username.|  | testcliqr |
| serverPassword | Password | Yes	|  Database server password.|  | Welcome2cliqr! |


