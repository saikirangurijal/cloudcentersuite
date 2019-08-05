# Puppet Agent

## Introduction

    The Workload Manager platform supports integration to various Configuration Management tools as VM with agent 
    type of service.

    This document provides information on integrating Puppet with Cisco Workload Manager.

    Puppet is an open-core software configuration management tool. It runs on many Unix-like systems as well as on Microsoft Windows, and includes its own declarative language to describe system configuration

    Please refer the below link for more details.

    https://puppet.com/docs
	
## Note
- This ReadMe for Existing Puppet agent.

## Prequisties
- Navigate to service menu and edit "puppet" service and change Agent Action Bundle to custom repository path.
	Example : http://<Your_REPO_Server_IP>/<service_path>/puppet.zip

#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager
- Supported OS : CentOS 7
- Supported Clouds : Google, AWS

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker".

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to execute "yum install wget -y" in case of centos7, and "apt install wget" in case of Ubuntu16.04.

	    Example: 
       wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.

##### PLEASE NOTE : 
You will be prompted with location of service bundle zip on linux machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/puppet.zip
   
## Service Package Bundle

The Package Service bundle consists of the following file:

Shell script:

- service: Installs puppet agent and Executes Puppet Roles.

## Agent Lifecycle Actions 

Agent Action Bundle:  
 - http://YourIP/services/puppet.zip - Location where your agent action bundle zip (service bundle zip file) is found.
 
Agent Lifecycle Actions: 
 - Install: Script from bundle: **service install**
 - Configure: Script from bundle: **service configure** 
 - Start: Script from bundle: **service start** 
 - Stop: Script from bundle: **service stop** 
 - Restart: Script from bundle: **service restart** 

#  Global Parameters:

| Parameter Name | Type | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| puppet_hostname| String | Puppet master hostname should be DNS name |

