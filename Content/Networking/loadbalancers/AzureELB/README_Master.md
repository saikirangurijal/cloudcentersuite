# Azure Load Balancer
## Introduction

	The Workload Manager supports integration to various Load Balancers as an external service.
    This document provides information on Azure Load Balancer integration with Workload Manager 
    by creating an external service.
    
    Azure RM Load Balancing gives you the ability to distribute load-balanced compute resources.

    Please refer the below link for more details.
	For your reference : https://docs.microsoft.com/en-us/azure/load-balancer/

## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager  
- Azure needs access to create load balancer through REST API, please refer for more details [here](https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal).

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
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/azurelb.zip 
    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/petclinic.zip

## Service Package Bundle

The Package Service bundle consists of the following files:

Shell script:
 - service: Initiates the python script to start integration.

Python script :
 - install_setup.py: The script will check all mandatory parameters available and installs necessary python packages also invokes external life cycle action.
 - service_parameter_util.py: script that checks all mandatory parameters available and create a parameter json file.
 - main.py: This script will have all lifecycle actions.
 - azure_management_client.py: Script that creates an azure client for managing load balancer using Azure SDK REST API
 - azure_load_balancer.py: A script that invokes creation, deletion and fetch the details of load balancer service using azure management client.
 - common.py: This script contains common functionalities which is required for other script files.
 - util.py: utility file
 - error_utils.py: A script that handles error functionalities
 
Other Files:
 - error_messages.json: Custom error message for load balancer
 - params.json: JSON Template of Azure Load Balancer Configuration

# External Lifecycle Actions 

External Action Bundle:  
 - http://YourIP/services/azurelb.zip - Location where your external action bundle zip is found.

External Lifecycle Actions:
 - Start: Script from bundle: **service start**
 - Stop: Script from bundle: **service stop**

# Service Parameters
| Parameter Name| Type	 | Mandatory |Description | Allowed Value |Default Value |
| ------ | ------ | ------ | ------ |------ | ------ |
| lbType |	List | Yes |Type of Load Balancer. For more details on the type of load balancer to choose, check Microsoft Azure Load Balancer documentation | Private / Public |  Public |
| loadBalancerRules | String | Yes	| Load Balancer Listener Rules which accepts FrontEnd Port, BackEnd Port, Protocol, Idle Timeout. | [["TCP", "80", "80", "30"]] |
| healthProbeRequestPath | String |	Yes | Health Request Probe Path for Load Balancer. | </> | /
| healthProbePort | Number | Yes | Port Number to check health probe path for application. | <80> | 80
| healthCheckProtocol | List | Yes | Ping Protocol Type. | TCP / HTTP / HTTPS | HTTP
| healthCheckInterval | Number | Yes | Health Check Interval in seconds (Max 30 Seconds). | <30> | 30
| unhealthThreshold | Number | Yes | Number of health check failures for unhealthly threshold. | <2> | 2


# Deployment Parameters:

| Parameter Name| Type	 | Mandatory |Description | Allowed Value |Default Value |
| ------ | ------ | ------ | ------ |------ | ------ |
| loadBalancerName | String | Yes | Name of the Load balancer. | <azureloadbalncer> |
