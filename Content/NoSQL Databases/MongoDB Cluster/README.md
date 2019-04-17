# Mongodb Cluster
## Introduction
    The  Workload Manager platform supports integration to various NoSQL database as Virtual Machine with Agent.
    This document provides information on Mongodb integration with Cisco Workload Manager by creating Virtual Machine 
    with Agent.
    
    MongoDB is a cross-platform, document oriented database that provides, high performance, high availability, 
    and easy scalability. MongoDB works on concept of collection and document.
    
    The service which we have created will support Mongo DB Cluster with 'n' nodes. Of which the Final node 
    will have Config server, Router and a Shard server. Remaining nodes(n-1) will have one shard server 
    per node with its own Replica.
    
    Router is configured in Port 27011, Config server in 27010, and all Shard Servers will work on default Port 27017.
    
    Please refer the below link for more details.
    https://docs.mongodb.com/manual/tutorial/deploy-shard-cluster/
	https://www.mongodb.com/what-is-mongodb
	
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager 
- Supported OS: CentOS 7
	
# Download the service bundles
Step 1 : Download the Service Bundle zip from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/NoSQL%20Databases/MongoDB%20Cluster/WorkloadManager/ServiceBundle/mongodbcluster.zip).
   
Step 2 : Download the application bundle to be used with application profile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/NoSQL%20Databases/MongoDB%20Cluster/WorkloadManager/ApplicationProfiles/artifacts/mongodb-j2ee-app.zip).
   
Step 3 : Place the service bundle from Step 1 under services/<bundle.zip> and application bundle from Step 2 under apps/<your_package_name> in your file repository. 
          
            - Service Bundle under services/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/services/mongodbcluster.zip 
    
            - Application Bundle under apps/<your_package_name>
            
                    Example : http://<Your_REPO_Server_IP>/apps/mongodb-j2ee-app.zip

   
Step 4 : Download the integration unit bundle (that contains logo, service json and application profile) from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/NoSQL%20Databases/MongoDB%20Cluster/WorkloadManager/mongodbcluster_iu.zip)
   
Step 5 : Extract the above bundle on any linux based machine and navigate to extracted folder.

Step 6 : Download the service import script zip file from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip)
   
Step 7: Copy the Service Import script zip file to the directory extarcted above in Step 5 and Unzip the service import script bundle.

Step 8 : Download the Dockerfile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Dockerfile) and copy to the extracted folder in Step 5
 
##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier
   
Ensure your directory in the linux based client machine contains :

- Service import json file (named as mongodbcluster_service.json)
- Service import script zip file (named as serviceimport.zip)
- main.py
- serviceimport.sh
- MongoDB logo (named as logo.png)
- Modelled application profile(named as mongodb_sample_app.zip)
- Dockerfile (named as Dockerfile)

## How to Create a Service in Cisco Workload Manager
   User can create the service by using **Import Service** functionality. 

#### Prerequisite for creating a service through service import script:

Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx) on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running docker -v
- You can check , if docker is running , by executing the command "systemctl status docker"

#### Detailed steps for creating a service through the service import script:

##### Step 1 : Provide executable permissions to the above files, Navigate to the directory where the files are placed and run the below command

	chmod 755 <your file> or chmod 755 *

Example :

	[root@ip-172-31-27-127 mongo]# chmod 755 mongodbcluster_service.json serviceimport.zip logo.png mongodb_sample_app.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

	[root@ip-172-31-27-127 mongo]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

	[root@ip-172-31-27-127 mongo]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

#### Note: Make sure there is no other zip file than app profile zip before execute docker run.

Example : 

[root@ip-172-31-27-127 mongo]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have added the downloaded service bundle zip file as per section "Where to Download The Service Bundles".

    Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"Mongo DB Cluster Service is imported successfully. Imported Application Profile Successfully"**

## Service Package Bundle

The Packer Service bundle consists of the following files:

Shell script:
 - service: The script will set all required environmental variables and installs necessary packages also invokes all agent life cycle action.
 
conf file:
 - ubuntu_conf: This file used to Configure for Ubuntu.
 - centos_conf: This file used to Configure for CentOS.
 - mongod.conf : This file is used to Configure the Config Server Replica Set.
 - mongodrouter.conf : This file is used to Configure the mongos/Query Router and  Add shards to mongos/Query Router
 - mongodshard.conf : This file is used to Configure the Shard Replica Sets

js file:
 - test_config.js : This js file used to Create Config Server Replica Set
 - test_router.js : This js file used to Create mongos/Query Router and  Add shards to mongos/Query Router
 - test_shard.js : This js file used to Create Shard Replica Sets
 - mongo.js : This js file used to Create database and collection in route server.
 
# Minimum Resource Specifications

S.No    | Resource   |  Value   | Remarks
------  | ---------- | ---------| ------- 
 1      |  CPU       |  1       |        
 2      |  Memory    |  1 GB    |   
 
 
## Agent Lifecycle Actions 

Agent Action Bundle:  
 - http://YourIP/services/mongodbcluster.zip the agent action bundle zip file is found.
 
Agent Lifecycle Actions:
 - Install: Script from bundle : **service install**
 - Configure: Script from bundle : **service configure**
 - Stop: Script from bundle : **service stop**

		
## Service parameters


| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| numClusterNodes |	number | Number of Nodes in the Cluster | 2 | 2|
| minClusterSize | number|Minimum Number of Nodes | 2 | 2 |
| maxClusterSize | number| Maximum Number of Nodes | 3 | 3 |
| dbName | string| Database Name | mongodb-cluster | mongodb-cluster |
| dbUsername | string| Database Username | mongo | mongo |

