# PostgreSQL Server

## Introduction

    The Workload Manager platform supports integration to various Database third party services.

    This document provides information on PostgreSQL server integration with Cisco Workload Manager by creating a 
    Virtual Machine (VM) with Agent service .

    PostgreSQL is a open source Relational Database system  which gives you the ability to manage the database.

    Please refer the below link for more details.

    https://www.postgresql.org/about/

## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager
- Supported OS: Centos7, Centos6 and Ubuntu16

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


##### PLEASE NOTE : You will be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

      - Service Bundle under <service_path>/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/<service_path>/psqlserver.zip 
    
      - Application Bundle under <app_path>/<your_package_name>	
            
                    Example : http://<Your_REPO_Server_IP>/<app_path>/psql-app.zip

## Service Package Bundle

The Package Service bundle consists of the following files:

Shell script:

- service: This script will set all required environment variables, installs necessary packages and also invokes the Agent life cycle actions.

# Minimum Resource Specifications

S.No | Resource   |  Value   | Remarks
---- | ---------- |--------- | ------- 
 1   |  CPU       | 2        |        
 2   |  Memory    | 8GB      |        

## Agent Lifecycle Actions 

Agent Action Bundle: 
 - http://YourIP/services/psqlserver.zip - Location where your agent action bundle zip (service bundle zip file) is found.
 
Agent Lifecycle Actions:
 - install: Script from bundle: **service install**
 - configure: Script from bundle: **service configure** 
 - Stop: Script from bundle: **service stop**
 - restart: Script from bundle: **service restart**

#  Service Parameters:

| Parameter Name | Type | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| UserName       | String  | username to be configured for the service. | User Defined Value | testuser |
| SqlPassword    | String  | password to be configured for the service. | User Defined Value | 123456 |


