# Memcached Container
## Introduction
    The  Workload Manager platform supports integration to various Backend Cache as Container service.
    This document provides information on memcached integration as container with Cisco Workload Manager by creating 
    Container Service.
    
    Memcached is a general-purpose distributed memory caching system. It is often used to speed up dynamic 
    database-driven websites by caching data and objects in RAM to reduce the number of times an external data source 
    (such as a database or API).
	
    Please refer the below link for more details.
    https://memcached.org/
	https://hub.docker.com/_/memcached
	
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

## Importing the service

Step 1 : Download the service import utility file from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.

	    Example: 
        wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.


##### PLEASE NOTE : You be prompted with location of application bundle zip on client machine. The file must be copied on to the repository before proceeding to deploy.

          - Application Bundle under <app-path>/<your_package_name>
        
                Example : http://<Your_REPO_Server_IP>/<app_path>/memcache-app.zip


**Note : Make Sure your deployment be in hybrid cloud
 
# Minimum Resource Specifications

S.No | Resource   |  Value   | Remarks
---- | ---------- |--------- | ------- 
 1   |  MilliCPUs | 100      |        
 2   |  Memory    | 250MB    |        