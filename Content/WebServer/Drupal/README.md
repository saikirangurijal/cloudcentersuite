# Drupal
## Introduction

    The Workload Manager platform supports integration to various Webservers.

    This document provides information on Drupal integration with Cisco Workload Manager by creating a 
    Virtual Machine (VM) with Agent service .

    Drupal is a open source platform which gives you the ability to deploy Open Source CMS applications. 
	
	The service which we have installed LAMP(Linux, Apache, MySQL, PHP) stack and drupal plugin webapp on top of Web Server and modelled as single tier application.
	
    Please refer the below link for more details.

    https://www.drupal.org/docs/8

## Pre-Requisites	
#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager
- Supported OS: CentOS 7/Ubuntu 16.04
- Supported clouds: Google and Azure.

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"	

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to execute "yum install wget -y" in case of centos7.

	    Example: 
      wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.

##### PLEASE NOTE : You be prompted with location of service bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/drupal.zip  
             
## Service Package Bundle

The Packer Service bundle consists of the following files:

Shell script:
 - service: The script will uses to installs necessary packages also invokes all agent life cycle action.
 
SQL file:
 - drupalSetup.sql : This sql file used to import for creating tables with default sample content in drupal database.
 
# Minimum Resource Specifications

S.No    | Resource   |  Value   | Remarks
------  | ---------- | ---------| ------- 
 1      |  CPU       |  1       |        
 2      |  Memory    |  1 GB    |   
 
 
## Agent Lifecycle Actions 

Agent Action Bundle:  
 - http://YourIP/services/drupal.zip the agent action bundle zip file is found.
 
Agent Lifecycle Actions: 
 - Start: Script from bundle : **service start**
 - Stop: Script from bundle : **service stop**
 
## Service parameters


| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| dbUsername | string| Database Username | drupaluser | drupaluser |
| dbPassword | string| Database Password | admin@123 | admin@123 |
| siteUserPassword | string| Site Maintenance Account Password | welcome2cliqr | welcome2cliqr | 

## Deployment parameters


| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ | 
| siteUsername | string| Site Maintenance Account Name | User defined values | cliqrtech |
| siteUserEmail | string| Site Maintenance Account Email | User defined values | cliqrtech@cisco.com |
| dbName | string| Database Name | User defined values | drupal |

