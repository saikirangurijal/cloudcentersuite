# Splunk Agent
## Introduction
    The Workload Manager supports integration to various third party services. 
    This document provides information on integration with Splunk Server 
    by creating a Virtual Machine (VM) with Agent service in Workload Manager.
    
    Splunk Enterprise is a software product that enables you to search, analyze, 
	and visualize the data gathered from the components of your IT infrastructure or business. 
	Splunk Enterprise takes in data from websites, applications, sensors, devices, and so on. 
	After you define the data source, Splunk Enterprise indexes the data stream and parses it into a series of individual events that you can view and search.

	There are three types of Data forwarders:

		- The universal forwarder contains only the components that are necessary to forward data. Learn more about the universal forwarder in the Universal Forwarder manual.
		- A heavy forwarder is a full Splunk Enterprise instance that can index, search, and change data as well as forward it. 
			The heavy forwarder has some features disabled to reduce system resource usage.
		- A light forwarder is also a full Splunk Enterprise instance, with more features disabled to achieve as small a resource footprint as possible. 
			The universal forwarder supersedes the light forwarder for nearly all purposes and represents the best tool for sending data to indexers.

    Please refer the below link for more details.
    https://docs.splunk.com/Documentation/Splunk/7.2.4/Forwarding/Typesofforwarders
	
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use CloudCenter 
- Ensure Splunk server is up and running.
  
## Where to Download the service bundles
 Step 1 : Download the Service Bundle zip from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Logging/Splunk-Agent/WorkloadManager/ServiceBundle/splunk-agent.zip).
 
 Step 2 : Create the Splunk Agent File by copying & pasting the contents from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Logging/Splunk-Agent/WorkloadManager/src/splunk-agent/splunk-agent) into a new file named "splunk-agent". 
	
 Step 3 : Place the service bundle from Step 1 under services/splunk-agent.zip and splunk-agent file from Step 2 under services/splunk-agent/splunk-agent in your file repository.
          
            - Service Bundle under services/splunk-agent.zip
                    
                    Example : http://<Your_REPO_Server_IP>/services/splunk-agent.zip
					
            - Splunk Agent under services/splunk-agent/splunk-agent
			        
		      Example : http://<Your_REPO_Server_IP>/services/splunk-agent/splunk-agent
   
 Step 4 : Download the integration unit bundle (that conatins application profile) from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Logging/Splunk-Agent/WorkloadManager/splunk-agent_iu.zip)
 
 Step 5 : Extract the above bundle on any linux based machine and navigate to extracted folder

 Step 6 : Download the Service Import script zip file from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip) 
 
 Step 7 : Copy the Service Import script zip file to the directory extarcted above in Step 5 and Unzip the service import script bundle.

 Step 8 : Download the Dockerfile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Dockerfile) and copy to the extracted folder in    Step 5 
 
 ##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier
   
 Ensure your directory in the linux based client machine contains :

- Service import script zip file (named as serviceimport.zip)
- main.py file
- serviceimport.sh
- Modelled application profile(named as splunk_agent_app_profile.zip)
- Dockerfile (named as Dockerfile) , **Only needed if you wish to create a Docker image for the first time**


## How to Create a Service in Cisco Workload Manager

User can create the service by using **Import Service** functionality using script.

#### Prerequisite for creating a service through service import script:

Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx) on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running docker -v
- You can check , if docker is running , by executing the command "systemctl status docker"
  
#### Detailed steps for creating a service through the service import script:

##### Step 1 :Provide executable permissions to the above files. Navigate to the directory where all the files are placed and run the below command:
   
   chmod 755 <your file>

Example : 
    [root@ip-172-31-27-127 splunk-agent]# chmod 755 serviceimport.zip splunk_agent_app_profile.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

###### [root@ip-172-31-27-127 splunk-agent]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

[root@ip-172-31-27-127 splunk-agent]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

    docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it 
    **[Your IMAGE ID]** /bin/bash

Example:  

[root@ip-172-31-27-127 splunk-agent]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note :  App profile zip bundle is implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Where to Download The Service Bundles". 

    - Select the corresponding Repository ID and Hit Enter.

If application proflie is successful, You will be presented with a message **"Imported Application Profile Successfully"**


## Integration Unit Bundle

The Package Service bundle consists of the following files:

Shell script:

Shell script:

 - splunk-agent: This script will install and configure splunk agent.

# Supported Cloud and OS

S.No    | Cloud   |  OS   
------  | ---------- | --------- 
 1      |  Google    |  CentOS 7  and Ubuntu 14               
 2      |  Azure     |  CentOS 7  and Ubuntu 14
 3      |  AWS     |  CentOS 7 and Ubuntu 14

## External Lifecycle Actions 

External Action Bundle:  

 Node Lifecycle Action File:  
 - http://YourIP/services/splunk-agent/splunk-agent - Location where your Node Lifecycle action file is found.


# Notes
  - splunk-agent file can be used in Node Life Cycle Actions.
  

 # Global Parameters in Application Profile

| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| splunkServerHost | String | Splunk Server Host IP |   |  |  |
| splunkForwarderPort | Number | Data Forwarder Port to Server as same as Receiver Port in Splunk Server | 81-65534 (Splunk Server Receiver Port) | 9997 | 
| splunkServerUserName | String | Splunk Server UserName | | admin |
| splunkServerPassword | Password | Splunk Server Password | | |
| logPath | String | Monitoring Log File Path | | | 

   
 
