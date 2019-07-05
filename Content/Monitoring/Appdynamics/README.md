# AppDynamics
## Introduction
    This document briefs down information on integration with Appdynamics in Workload Manager.
    AppDynamics, an application performance management solution provides the required metrics 
    of server monitoring tools along with the the troubleshooting capabilities of APM software.
    Please refer the below link for more details.
    https://docs.appdynamics.com/
    
## Pre-Requisites
 - Appdynamics controller should be up and running with minimum configuration. For details on Minimum configuration, System requirement and Installation setup, Please refer

##### CloudCenter

   - CloudCenter 5.0.1 and above
   - Knowledge on how to use Workload Manager
   - Supported OS (client): CentOS 7 and Ubuntu 16.04
   
#### Supported agents for appdynamics
- Database Agent
- Java Agent
- Webserver Agent
- Machine Agent

**NOTE** :  while deploying webserver agent in workload manager it may take more than one hour to monitor and update in appdynamics controller.

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

Once the script is run, please follow the prompts to import the service or the correspondong application profile.


##### PLEASE NOTE : You will be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

        - Agent Bundle under <service_path>/<your_bundle_name>
            Example: http://<Your_REPO_Server_IP>/<service_path>/appdynamics/appdynamicsagent 
    
        - AppdynamicPackage under <app_path>/<your_package_name>	
            
                    Example : http://<Your_REPO_Server_IP>/<app_path>/agentsdownload.zip

## Service Package Bundle

The Package Service bundle consists of the following files:

Shell script:

- service: This script will set all required environment variables, install necessary packages and also invokes the Agent life cycle actions.

## Minimum Resource Specifications

S.No | Resource   |  Value   | Remarks
---- | ---------- |--------- | ------- 
 1   |  CPU       | 2        |        
 2   |  Memory    | 8GB      |        

# Agent Bundle

The Package of agent bundle consists of the following files:

Shell script:
 - appdynamicsagent : This script will download and agentsdownload.zip and invokes the service script.
Agents bundle :
 - service : This script will invoke python script agentsdownload.py
 - agentsdownload.py : This script will identify the agent and installs the agent.
 - httpd.conf : configuration file for apache webserver
 - appdynamics.cer : SSL certificate for appdynamics 

# Service Initialization actions / Node Initialization & Clean Up
   - Under "Post-Start Script" lifecycle action, agent script would be configured like services//appdynamics/appdynamicsagent
# Global Parameters in Application Profile
| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| AppdynamicPackage | Path | AppdynamicPackage Bundle location |   |  |  |

# Deployment parameters in Application Profile for Java Agent 
| Parameter Name	| Type	 | Description | 
| ------ | ------ | ------ 
| AppdynamicsUsername | String | Appdynamics registered username or E-mail address  | 
| AppdynamicsPassword | String | Appdynamics password  |  
| AppDynamicsAccountName | String | Account name of controller  |
| AppDynamicsAccessKey | String | Accesskey of controller  |  
| AppDynamicsControllerHost | String | Host address of controller  |  
| AppDynamicsControllerPort | Number | Port for connecting to controller  |  
| ApplicationName | String | Application name to be monitored  |  

# Deployment parameters in Application Profile for DB Agent 
| Parameter Name	| Type	 | Description | 
| ------ | ------ | ------ 
| AppdynamicsUsername | String | Appdynamics registered username or E-mail address  | 
| AppdynamicsPassword | String | Appdynamics password  |  
| AppDynamicsAccountName | String | Account name of controller  |
| AppDynamicsAccessKey | String | Accesskey of controller  |  
| AppDynamicsControllerHost | String | Host address of controller  |  
| AppDynamicsControllerPort | Number | Port for connecting to controller  |  


# Deployment parameters in Application Profile for Webserver Agent 
| Parameter Name	| Type	 | Description | 
| ------ | ------ | ------ 
| AppdynamicsUsername | String | Appdynamics registered username or E-mail address  | 
| AppdynamicsPassword | String | Appdynamics password  |  
| AppDynamicsAccountName | String | Account name of controller  |
| AppDynamicsAccessKey | String | Accesskey of controller  |  
| AppDynamicsControllerHost | String | Host address of controller  |  
| AppDynamicsControllerPort | Number | Port for connecting to controller  |  
| ApplicationName | String | Application name to be monitored  |  

