# Cassandra Cluster
## Introduction
    The  Workload Manager platform supports integration to various NoSQL database as Virtual Machine with Agent.
    This document provides information on Cassandra integration with Cisco Workload Manager by creating 
    Virtual Machine with Agent.
    
    Cassandra is a distributed database from Apache that is highly scalable and designed to manage very large 
    amounts of structured data. It provides high availability with no single point of failure.
    
    Please refer the below link for more details.
    http://cassandra.apache.org/doc/latest/
	https://github.com/GoogleCloudPlatform/cassandra-docker/blob/master/3/README.md	
# Pre-Requisites
#### CloudCenter Suite
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager
- Supported OS: CentOS 7

	
## Download the service bundles
   
Step 1 : Download the Service Bundle zip from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/NoSQL%20Databases/Cassandra%20Cluster/WorkloadManager/ServiceBundle/cassandracluster.zip)
   
Step 2 : Download the application bundle to be used with application profile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/NoSQL%20Databases/Cassandra%20Cluster/WorkloadManager/ApplicationProfiles/artifacts/ntier-cassandra-app.zip)
   
Step 3 : Place the service bundle from Step 1 under services/<bundle.zip> and application bundle from Step 2 under apps/<your_package_name> in your file repository.
          
            - Service Bundle under services/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/services/cassandracluster.zip 
    
            - Application Bundle under apps/<your_package_name>
            
                    Example : http://<Your_REPO_Server_IP>/apps/ntier-cassandra-app.zip 
   
 Step 4 : Download the integration unit bundle (that conatins logo, service json and application profile) from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/NoSQL%20Databases/Cassandra%20Cluster/WorkloadManager/cassandracluster_iu.zip).
 
 Step 5 : Extract the above bundle on any linux based machine and navigate to extracted folder.
 
 Step 6 : Download the service import script zip file from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip)
   
 Step 7: Copy the Service Import script zip file to the directory extracted above in Step 5 and Unzip the service import script bundle.

 Step 8 : Download the Dockerfile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Dockerfile) and copy to the extracted folder in Step 5
 
 ##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier
   
 Ensure your directory in the linux based client machine contains :
 
- Service import json file (named as cassandra_service.json)
- Service import script zip file (named as serviceimport.zip)
- main.py
- serviceimport.sh
- Cassandra logo (named as logo.png)
- Modelled application profile(named as cassandra_sample_app.zip)
- Dockerfile (named as Dockerfile)

## How to Create a Service in Cisco Cloud Center
   
User can create the service by using **Import Service** functionality. 
  
#### Prerequisite for creating a service through service import script:

Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx) on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running docker -v
- You can check , if docker is running , by executing the command "systemctl status docker"  

#### Detailed steps for creating a service through the service import script:

##### Step 1 : Provide executable permissions to the above files, Navigate to the directory where the files are placed and Run the below command

	chmod 755 <your file>

Example : 
	[root@ip-172-31-27-127 cass]# chmod 755 cassandra_service.json serviceimport.zip logo.png cassandra_sample_app.zip Dockerfile


**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

	 [root@ip-172-31-27-127 cass]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

	 [root@ip-172-31-27-127 cass]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

	docker run -v **[HOST_DIRECTORY_WHERE_DOWNLOADED_FILES_ARE_PLACED]**:/ccsworker -w /ccsworker -it 
	**[Your IMAGE ID]** /bin/bash

Example: 

[root@ip-172-31-27-127 cass]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

##### Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Download The Service Bundles". 

    Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"Cassandra Cluster Service imported successfully. Imported Application Profile Successfully"**

## Service Package Bundle

The Packer Service bundle consists of the following files:

Shell script:
 - service: The script will set all required environmental variables and installs necessary packages also invokes all external life cycle action.
 
SQL file:
 - dbsetup: The script will create Keyspace on cassandra db with replication factor.
 
# Minimum Resource Specifications

S.No | Resource   |  Value   | Remarks
---- | ---------- |--------- | ------- 
 1   |  CPU       | 2        |        
 2   |  Memory    | 8 GB     |        

# Supported Cloud and OS

S.No    | Cloud   |  OS   
------  | ---------- | --------- 
 1      |  Google    |  CentOS 7                
 2      |  Azure     |  CentOS 7  
 3 		|  AWS       |  CentOS 7
 
## External Lifecycle Actions 

External Action Bundle:  
 - http://YourIP/cassandra/cassandracluster.zip the external action bundle zip file is found.
 
External Lifecycle Actions:
 - Install: Script from bundle: **service install**
 - Start: Script from bundle: **service start**
 - Stop: Script from bundle: **service stop**
 - Restart: Script from bundle: **service restart**
		
## Service parameters


| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| NoSqlClusterName | String | Default cluster name would be TestCluster.| TestCluster |  TestCluster |
| NoSqlDatabaseName |	String |	Default Database name would be demo_cassdb. | demo_cassdb | demo_cassdb | 
| NoSqlDatabaseRootPass | String | Database Password for Superuser cassandra | cassandra | cassandra |
| numClusterNodes |	number | Number of Nodes in the Cluster | 3 | 2 |
| numSeedNodes | number| Number of Seed Nodes | 1 | 1 |
| minClusterSize | number|Minimum Number of Nodes | 2 | 2 |
| maxClusterSize | number| Maximum Number of Nodes | 3 | 3 |
