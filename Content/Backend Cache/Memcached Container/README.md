# Memcached Container
## Introduction
    The  Workload Manager platform supports integration to various Backend Cache as Container service.
    This document provides information on memcached integration as container with Cisco Workload Manager by creating 
    Container Service.
    
    Memcached is a general-purpose distributed memory caching system. It is often used to speed up dynamic database-driven websites by caching data and 
	objects in RAM to reduce the number of times an external data source (such as a database or API).
	
    Please refer the below link for more details.
    https://memcached.org/
	https://hub.docker.com/_/memcached
	
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager 
	
# Download the service bundles
   
 Step 1 : Download the integration unit bundle (that contains logo, service json and application profile) from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Backend%20Cache/Memcached%20Container/WorkloadManager/memcached_cont_iu.zip).
 
 Step 2 : Extract the above bundle on any linux based machine and navigate to extracted folder.
 
 Step 3 : Download the service import script zip file from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip)
   
 Step 4 : Copy the Service Import script zip file to the directory extracted above in Step 2 and Unzip the service import script bundle.

 Step 5 : Download the Dockerfile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Dockerfile) and copy to the extracted folder in Step 2
 
 ##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier
   
 Ensure your directory in the linux based client machine contains :
 
- Service import json file (named as memcached_cont_service.json)
- Service import script zip file (named as serviceimport.zip)
- main.py                 
- serviceimport.sh
- Memcached logo (named as logo.png)
- Modelled application profile(named as memcached_cont_sample_app.zip)
- Dockerfile (named as Dockerfile)

## How to create a service in Cisco Cloud Center
   
User can create the service by using **Import Service** functionality. 
  
#### Prerequisite for creating a service through service import script:

Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx) on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running docker -v
- You can check , if docker is running , by executing the command "systemctl status docker"  

#### Detailed steps for creating a service through the service import script:

##### Step 1 : Provide executable permissions to the above files, Navigate to the directory where the files are placed and Run the below command

	chmod 755 <your file> or chmod 755 *

Example : 
	[root@ip-172-31-27-127 mem]# chmod 755 memcached_cont_service.json serviceimport.zip logo.png memcached_cont_sample_app.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

	 [root@ip-172-31-27-127 mem]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

	 [root@ip-172-31-27-127 mem]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

	docker run -v **[HOST_DIRECTORY_WHERE_DOWNLOADED_FILES_ARE_PLACED]**:/ccsworker -w /ccsworker -it 
	**[Your IMAGE ID]** /bin/bash

#### Note: Make sure there is no other zip file than app profile zip before execute docker run.

Example: 

[root@ip-172-31-27-127 mem]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

##### Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Where to Download The Service Bundles". 

    Select the corresponding Repository ID and Hit Enter.
	
If service creation is successful, You will be presented with a message **"Memcached Container Service imported successfully. Imported Application Profile Successfully"**

 
# Minimum Resource Specifications

S.No | Resource   |  Value   | Remarks
---- | ---------- |--------- | ------- 
 1   |  MilliCPUs | 100      |        
 2   |  Memory    | 250MB    |        


		