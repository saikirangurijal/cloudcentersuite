# Splunk Server Integration Unit
## Introduction
    The Workload Manager supports integration to various third party services. 
    This document provides information on integration with Splunk Server 
    by creating a Virtual Machine (VM) with Agent service in Workload Manager.
    
    Splunk Enterprise is a software product that enables you to search, analyze, 
	and visualize the data gathered from the components of your IT infrastructure or business. 
	Splunk Enterprise takes in data from websites, applications, sensors, devices, and so on. 
	After you define the data source, Splunk Enterprise indexes the data stream and parses it into a series of individual events that you can view and search.

    Please refer the below link for more details.
    https://docs.splunk.com/Documentation
  
# Download the service bundles
 Step 1 : Download the Service Bundle zip from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Logging/Splunk/WorkloadManager/ServiceBundle/splunk.zip).
 
 Step 2 : Create the Splunk File by copying & pasting the contents from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Logging/Splunk/WorkloadManager/src/splunk/service)into a new file named "service". 
   
 Step 3 : Place the service bundle from Step 1 under services/<bundle.zip> and splunk file from Step 2 under services/splunk/service in your file repository.
          
            - Service Bundle under services/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/services/splunk.zip
					
            - Service file under services/splunk/service
			        
		    Example : http://<Your_REPO_Server_IP>/services/splunk/service
  
 Step 4 : Download the integration unit bundle (that conatins logo, service json and application profile) from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Logging/Splunk/WorkloadManager/splunk_iu.zip)
 
 Step 5 : Extract the above bundle on any linux based machine and navigate to extracted folder

 Step 6 : Download the Service Import script zip file from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip) 
 
 Step 7 : Copy the Service Import script zip file to the directory extarcted above in Step 5 and Unzip the service import script bundle.

 Step 8 : Download the Dockerfile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Dockerfile) and copy to the extracted folder in    Step 5 
 
 ##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier
   
 Ensure your directory in the linux based client machine contains :

- Service import json file (named as splunk_service.json)
- Service import script zip file (named as serviceimport.zip)
- main.py file
- serviceimport.sh
- Splunk logo (named as logo.png)
- Modelled application profile(named as splunk_sample_app.zip)
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
    [root@ip-172-31-27-127 splunk]# chmod 755 splunk_service.json serviceimport.zip logo.png splunk_sample_app.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

###### [root@ip-172-31-27-127 splunk]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

[root@ip-172-31-27-127 splunk]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

    docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it 
    **[Your IMAGE ID]** /bin/bash

Example:  

[root@ip-172-31-27-127 splunk]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Where to Download The Service Bundles". 

    - Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"Splunk Service imported successfully. Imported Application Profile Successfully"**


## Service Package Bundle

The Package Service bundle consists of the following files:

Shell script:

 - service: This script will install splunk server and load configuration from service parameters and installs necessary packages and also invokes the external life cycle actions.


# Minimum Resource Specifications

S.No    | Resource   |  Value   | Remarks
------  | ---------- | ---------| ------- 
 1      |  CPU       |  1       |        
 2      |  Memory    |  8 GB    |   
   
# Supported Cloud and OS

S.No    | Cloud   |  OS   
------  | ---------- | --------- 
 1      |  Google    |  CentOS 7  and Ubuntu 14               
 2      |  Azure     |  CentOS 7  and Ubuntu 14
 3      |  AWS     |  CentOS 7 and Ubuntu 14
 
 
## External Lifecycle Actions 

External Action Bundle:  
 - http://YourIP/services/splunk.zip - Location where your external action bundle zip (service bundle zip file) is found.
 
External Lifecycle Actions:
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



