# Apache Hadoop Cluster
## Introduction
    The Apache Hadoop project develops open-source software for 
	reliable, scalable, distributed computing.

	The Apache Hadoop software library is a framework that allows for the 
	distributed processing of large data sets across clusters of computers 
	using simple programming models. 
	
	It is designed to scale up from single servers to thousands of machines, 
	each offering local computation and storage. 
	
	Rather than rely on hardware to deliver high-availability, 
	the library itself is designed to detect and handle failures at the application layer, 
	so delivering a highly-available service on top of a cluster of computers, 
	each of which may be prone to failures.
    
    Please refer the below link for more details.
	https://hadoop.apache.org/
	
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager 
- Supported OS: CentOS 7 , Ubuntu 16


#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

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

##### PLEASE NOTE : You be prompted with location of service bundle zip, application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/apachehadoopcluster.zip 
    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/phpsimpleform.zip

## Service Package Bundle

The Packer Service bundle consists of the following files:

Shell script:
 - service: The script will set all required environmental variables and installs necessary packages also invokes all external life cycle action.
 
## Agent Lifecycle Actions

External Action Bundle:  
 - http://YourIP/services/apachehadoopcluster.zip the Agent action bundle zip file is found.
 
External Lifecycle Actions:
 - install: Script from bundle: **service install**
 - configure: Script from bundle: **service configure** 
 - Stop: Script from bundle: **service stop**
 - restart: Script from bundle: **service restart**
 
 
 ## Service parameters


| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| numClusterNodes |	number | Number of Nodes in the Cluster | 2 | 2|
| minClusterSize | number|Minimum Number of Nodes | 2 | 2 |
| maxClusterSize | number| Maximum Number of Nodes | 3 | 3 |


Note: When deploying the application, please select "Persist Private Key" in SSh Options.

	| SSH Options | No Preference | Assign Public Key | Persist Private Key
