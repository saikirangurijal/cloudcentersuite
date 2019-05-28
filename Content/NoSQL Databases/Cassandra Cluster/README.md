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
- wget command may not be installed. Need to execute "yum install wget -y" in case of centos7.

	    Example: 
      wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.


##### PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <services_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/cassandracluster.zip 
    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/apps/ntier-cassandra-app.zip

## Service Package Bundle

The Packer Service bundle consists of the following files:

Shell script:
 - service: The script will set all required environmental variables and installs necessary packages also invokes all agent life cycle action.
 
SQL file:
 - dbsetup: The script will create Keyspace on cassandra db with replication factor.
 
# Minimum Resource Specifications

S.No | Resource   |  Value   | Remarks
---- | ---------- |--------- | ------- 
 1   |  CPU       | 2        |        
 2   |  Memory    | 8 GB     |        

  
## Agent Lifecycle Actions 

Agent Action Bundle:  
 - http://YourIP/cassandra/cassandracluster.zip the agent action bundle zip file is found.
 
Agent Lifecycle Actions:
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