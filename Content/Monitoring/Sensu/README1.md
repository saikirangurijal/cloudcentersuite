# Sensu Server Integration Unit
## Introduction
    The Workload Manager supports integration to various third party services. This document briefs down 
    information on integration with Sensu server by creating a Virtual Machine (VM) with Agent service 
    in Workload Manager.
    
    Sensu is an open source monitoring event pipeline, basically used for monitoring production workloads. 
    Sensu monitors application and system services, detecting those in an unhealthy state.    
    
    Please refer the below link for more details.
    https://docs.sensu.io/sensu-go/
# Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager 
- Supported OS: CentOS 7

# Download the service bundles
   Step 1 : Download the Service Bundle zip file [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Monitoring/Sensu/WorkloadManager/ServiceBundle/sensu.zip). 
   
   Step 2: Place the service bundle from Step 1 under services/<bundle.zip> in your file repository.
   
                  - Service Bundle under services/<bundle.zip>

                       Example : http://<Your_REPO_Server_IP>/services/sensu.zip 
   
   Step 3 : Download the integration unit bundle (that contains logo, service json and application profile) [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Monitoring/Sensu/WorkloadManager/sensu_iu.zip?raw=true).
   
   Step 4 : Extract the above bundle on any linux based machine and navigate to the extracted folder.
   
   Step 5 : Download the Service Import script zip file [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip).
   
   Step 6 : Copy the Service Import script zip file to the directory extracted above in Step 4 and Unzip the service import script bundle.
   
   Step 7 : Download the Dockerfile [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Dockerfile) and copy to the extracted folder in Step 4.
   
   ##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier.
   
   Ensure your directory in the linux based client machine contains :
 - Service import json file (named as sensu_service.json)
 - Service import script zip file (named as serviceimport.zip)
 - main.py file
 - serviceimport.sh file
 - sensu logo (named as logo.png)
 - Modelled application profile(named as sensuserver_sample_app.zip)
 - Dockerfile (named as Dockerfile), **Only needed if you wish to create a Docker image for the first time.**

## How to Create a Service in Cisco Workload Manager
User can create the service by using **Import Service** functionality using script.

#### Prerequisite for creating a service through service import script:

Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx) on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running the command "docker -v".
- You can check , if docker is running , by executing the command "systemctl status docker".
  
#### Detailed steps for creating a service through the service import script:

##### Step 1 :Provide executable permissions to the above files. Navigate to the directory where all the files are placed and run the below command:
   
      chmod 755 <your file> or chmod 755 *

Example : 
    [root@ip-172-31-27-127 sensu]# chmod 755 sensu_service.json serviceimport.zip logo.png sensu_sample_app.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases, Skip to Step 5.**

     [root@ip-172-31-27-127 sensu]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command.

     [root@ip-172-31-27-127 sensu]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

    docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it 
    **[Your IMAGE ID]** /bin/bash

#### Note: Make sure there is no other zip file than app profile zip before execute docker run.

Example:  

[root@ip-172-31-27-127 sensu]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.
Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Where to Download The Service Bundles". 

    - Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"sensu Service imported successfully. Imported Application Profile Successfully"**

# Service Package Bundle

The Package of Service bundle consists of the following files:

Shell script:
 - service: This script will set all required environment variables, installs necessary packages and also invokes the external life cycle actions.
 
# Minimum Resource Specifications

     
S.No    | Resource    |  Value   | Remarks
----    | ----------  | ---------| ------- 
 1      |  CPU        | 1        |        
 2      |  Memory     | 1 GB     |        
 
# Agent Lifecycle Actions 
Agent Action Bundle:  
 - http://YourFileRepositoryIP/services/sensu.zip - Location where your agent action bundle zip (service bundle zip file) is found.

Agent Lifecycle Actions:
 - Install: Script from bundle: **service install**
 - Start: Script from bundle: **service start**
 - Stop: Script from bundle: **service stop**
 - Restart: Script from bundle: **service restart**

