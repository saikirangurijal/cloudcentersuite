
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
- Supported OS: Centos7, Ubuntu16.

## Download the service bundles

 Step 1 : Download the Service Bundle zip from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Logging/Elasticsearch/WorkloadManager/ServiceBundle/elasticsearch.zip). 
   
 Step 2 : Download the application bundle to be used with application profile from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Logging/Elasticsearch/WorkloadManager/ApplicationProfiles/artifacts/phpcontactform.zip).
 
 step 3 : Download the logstashservice Bundle zip from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Logging/Elasticsearch/WorkloadManager/ApplicationProfiles/artifacts/logstashservice.zip).
 
 Step 4 : Place the service bundle from Step 1 under services/<bundle.zip>,application bundle from Step 2 under apps/<your_package_name> and logstashservice bundle from step 3 under apps/logstash/<bundle.zip> in your file repository.
          
            - Service Bundle under services/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/services/elasticsearch.zip 
    
            - Application Bundle under apps/<your_package_name>	
            
                    Example : http://<Your_REPO_Server_IP>/apps/phpcontactform.zip
                    
            _ logstashservice Bundle under apps/logstash/<logstashservice.zip>
            
                create logstash directory under apps and place your logstashservice in logstash directory
                
                Exmaple : https://<Your_REPO_Server_IP>/apps/logstash/logstashservice.zip
   
 Step 5 : Download the integration unit bundle (that contains logo, service json and application profile) from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Logging/Elasticsearch/WorkloadManager/elasticsearch_iu.zip)
 
 Step 6: Extract the above bundle on any linux based machine and navigate to extracted folder

 Step 7 : Download the Service Import script zip file from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Scripts/serviceimport.zip) 
 
 Step 8 : Copy the Service Import script zip file to the directory extracted above in Step 5 and Unzip the service import script bundle.

 Step 9 : Download the Dockerfile from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Dockerfile) and copy to the extracted folder in Step 5
 
 ##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier
   
 Ensure your directory in the linux based client machine contains :

- Service import json file (named as elasticsearch_service.json)
- Service import script zip file (named as serviceimport.zip)
- main.py file
- serviceimport.sh
- elasticsearch logo (named as logo.png)
- Modelled application profile(named as elk_sample_app.zip)
- Dockerfile (named as Dockerfile) , **Only needed if you wish to create a Docker image for the first time**
   
## How to Create a Service in Cisco Workload Manager

User can create the service by using **Import Service** functionality using script.

#### Prerequisite for creating a service through service import script:

Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx) on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running docker -v
- You can check , if docker is running , by executing the command "systemctl status docker"
  
#### Detailed steps for creating a service through the service import script:

##### Step 1 :Provide executable permissions to the above files. Navigate to the directory where all the files are placed and run the below command:
   
    chmod 755 <your file> or chmod 755 *
    
    
Example : 
    [root@ip-172-31-27-127 elasticsearch]# chmod 755 elasticsearch_service.json serviceimport.zip logo.png elk_sample_app.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

    [root@ip-172-31-27-127 elasticsearch]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

    [root@ip-172-31-27-127 elasticsearch]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

    docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it 
    **[Your IMAGE ID]** /bin/bash

Example:  

[root@ip-172-31-27-127 elasticsearch]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Where to Download The Service Bundles". 

    - Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"elasticsearch Service imported successfully. Imported Application Profile Successfully"**

## Integration Unit Bundle

The Package Service bundle consists of the following files:

Shell script:

- service: This script will set all required environment variables, installs necessary packages and also invokes the Agent life cycle actions.

# Minimum Resource Specifications

S.No | Resource   |  Value   | Remarks
---- | ---------- |--------- | ------- 
 1   |  CPU       | 1       |        
 2   |  Memory    | 2GB      |        

## Agent Lifecycle Actions 

Agent Action Bundle: 
 - http://YourIP/services/elasticsearch.zip - Location where your agent action bundle zip (service bundle zip file) is found.
 
Agent Lifecycle Actions:
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
          





