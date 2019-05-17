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

	    Example: 
       wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the correspondong application profile.

##### PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <services_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/mongodbcluster.zip 
    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/mongodb-j2ee-app.zip
             
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
| dbUsername | string| Database Username | mongo | mongo 
| dbPassword | string| Database Password | mongocluster | mongocluster |
