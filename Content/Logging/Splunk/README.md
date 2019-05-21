# Splunk Server Integration Unit
## Introduction
    The Workload Manager supports integration to various third party services. 
    This document provides information on integration with Splunk Server 
    by creating a Virtual Machine (VM) with Agent service in Workload Manager.
    
    Splunk Enterprise is a software product that enables you to search, analyze, 
	and visualize the data gathered from the components of your IT infrastructure or business. 
	Splunk Enterprise takes in data from websites, applications, sensors, devices, and so on. 
	The latest released version of splunk enterprise is '6.5'.
	After you define the data source, Splunk Enterprise indexes the data stream and parses it into a 
	series of individual events that you can view and search.
      
    Please refer the below link for more details.
    https://docs.splunk.com/Documentation
 
 ## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager 
- Supported OS: CentOS 7  
 
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

Once the script is run, please follow the prompts to import the service or the corresponding application profile.

##### PLEASE NOTE : You will be prompted with location of service bundle zip on client machine. The file must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/splunk.zip 

## Service Package Bundle

The Package Service bundle consists of the following files:

Shell script:

 - service: This script will install splunk server and load configuration from service parameters and installs necessary packages and also invokes the agent life cycle actions.


# Minimum Resource Specifications

S.No    | Resource   |  Value   | Remarks
------  | ---------- | ---------| ------- 
 1      |  CPU       |  1       |        
 2      |  Memory    |  8 GB    |   
 
 
## Agent Lifecycle Actions 

Agent Action Bundle:  
 - http://YourIP/services/splunk.zip - Location where your agent action bundle zip (service bundle zip file) is found.
 
Agent Lifecycle Actions:
 - Install: Script from bundle: **service install**
 - Configure: Script from bundle: **service configure**
 - Start: Script from bundle: **service start**
 - Stop: Script from bundle: **service stop**
 - Restart: Script from bundle: **service restart**

 # Service Parameters

| Parameter Name |  Type  |    Description     |       Allowed Value        |Default Value |
| -------------- | ------ | ------------------ | -------------------------- | ------------ |
|  serverPort    | Number |  Server Web Port   | 80-65534 (Any Unused Port) |     80       |
|  receiverPort  | Number | Data Receiver Port | 81-65534 (Any Unused Port) |    9997      | 


