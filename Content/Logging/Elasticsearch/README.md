# Elasticsearch
## Introduction
     ElasticSearch is an open source, RESTful search engine and near-realtime search platform. 
    
    Elasticsearch is used for storing data and used to perform a search task on stored data.
       
    The Workload Manager platform supports integration to various logging purpose third party services.
    
    This document provides information on Elasticsearch integration with Cisco Workload Manager by creating a
     
    Virtual Machine (VM) with Agent service .
    

    Please refer the below link for more details.

    https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started-concepts.html
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above
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

Step 3 : Download the logstashservice Bundle zip from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Logging/Elasticsearch/WorkloadManager/ApplicationProfiles/artifacts/logstashservice.zip).

##### PLEASE NOTE : You be prompted with location of service bundle zip, logstashservice bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/dynamodb.zip 
    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/dynamodb-php-app.zip
             
         - logstashservice Bundle under apps/logstash/<logstashservice.zip>
            
                create logstash directory under apps and place your logstashservice in logstash directory
                
                Exmaple : https://<Your_REPO_Server_IP>/apps/logstash/logstashservice.zip    

## Service Package Bundle

The Packer Service bundle consists of the following files:

Shell script:
 - service: The script will set all required environmental variables and installs necessary packages also invokes all external life cycle action.

Python script :

 - install_setup.py: The script will installs necessary python packages also invokes external life cycle action.

 - main.py : The script that invokes creation, deletion and fetch the details of dynamo tables.

 - util.py: utility file

 - error_utils.py: The script that handles error functionality

## Agent Lifecycle Actions

External Action Bundle:  
 - http://YourIP/services/elasticsearch.zip the Agent action bundle zip file is found.
 
External Lifecycle Actions:
 - install: Script from bundle: **service install**
 - configure: Script from bundle: **service configure** 
 - Stop: Script from bundle: **service stop**
 - restart: Script from bundle: **service restart**

		
#  Deployment Parameters:

| Parameter Name | Type | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| Indexparam       | String  | Index to be configured for the service. | User Defined Value | samplelogs |



# Apache2 server deployment parameters:

| Parameter Name | Type | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| Indexparam       | String  | value must be same which is in elasticsearch service deployment paramter(Indexparam) | User Defined Value | samplelogs |
| LogPath          | String  | location of log file| user Defined Value|/var/log/httpd/error.log|


##### Detailed Steps To Retrieve Data From Elasticsearch

Step 1 : Deploy ELK application.

Step 2 : In a web browser, follow below format url to check data in Elasticsearch
         
     		- http://your_Elasticsearch_server_ip:9200/your_indexname/_search?pretty
          


