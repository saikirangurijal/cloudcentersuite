# MSSQL Server

## Introduction

    The Workload Manager platform supports integration to various Database third party services.

    This document provides information on MSSQl server 2017 integration with Cisco Workload Manager by creating a 
    Virtual Machine (VM) with Agent service .

    MSSQL is a open source Relational Database system  which gives you the ability to manage the database.

    Please refer the below link for more details.

    https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-ubuntu?view=sql-server-2017

## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager
- Supported OS: Ubuntu16
- Supported clouds: Google and Azure.

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

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

Once the script is run, please follow the prompts to import the service or the correspondong application profile.


##### PLEASE NOTE : You will be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

        - Service Bundle under <service_path>/<your_bundle_name>
                    
                    Example : http://<Your_REPO_Server_IP>/<service_path>/mssqlserver.zip 
    
        - Application Bundle under <app_path>/<your_package_name>	
            
                    Example : http://<Your_REPO_Server_IP>/<app_path>/mssql-app.zip

## Service Package Bundle

The Package Service bundle consists of the following files:

Shell script:

- service: This script will set all required environment variables, install necessary packages and also invokes the Agent life cycle actions.

## Minimum Resource Specifications

S.No | Resource   |  Value   | Remarks
---- | ---------- |--------- | ------- 
 1   |  CPU       | 1        |        
 2   |  Memory    | 4GB      |        

## Agent Lifecycle Actions 

Agent Action Bundle: 
 - http://YourIP/services/mssqlserver.zip - Location where your agent action bundle zip (service bundle zip file) is found.
 
Agent Lifecycle Actions:
 - install: Script from bundle: **service install**
 - configure: Script from bundle: **service configure** 
 - Stop: Script from bundle: **service stop**
 - restart: Script from bundle: **service restart**


##  Service Parameters:

| Parameter Name | Type | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| SqlPassword | String | password to be configured for the service. | User Defined Value | Cliqr@1234 |

