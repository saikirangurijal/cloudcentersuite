# Kibana Integration Unit
## Introduction
    Kibana is an open source data visualization plugin for Elasticsearch. 
    
    It provides visualization capabilities on top of the content indexed on an Elasticsearch cluster. 
    Users can create bar, line and scatter plots, or pie charts and maps on top of large volumes of data.

    Kibana also provides a presentation tool, referred to as Canvas, 
    that allows users to create slide decks that pull live data directly from Elasticsearch.

    The combination of Elasticsearch, Logstash, and Kibana, referred to as 
    the "Elastic Stack" (formerly the "ELK stack"), is available as a product or service. 
    
    Logstash provides an input stream to Elasticsearch for storage and search, 
    and Kibana accesses the data for visualizations such as dashboards. 
    
    Elastic also provides "Beats" packages which can be configured to provide 
    pre-made Kibana visualizations and dashboards about various database 
    and application technologies.
      
    Please refer the below link for more details.
    https://www.elastic.co/guide/en/kibana
 
 ## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager 
- Supported OS: CentOS 7 , Ubuntu 16
  
# Download the service bundles
 Step 1 : Download the Service Bundle zip from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Logging/Kibana/WorkloadManager/ServiceBundle/kibana.zip).
   
 Step 2 : Place the service bundle from Step 1 under services/<bundle.zip>
          
            - Service Bundle under services/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/services/kibana.zip
  
 Step 3 : Download the integration unit bundle (that contains logo, service json) from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Logging/Kibana/WorkloadManager/kibana_iu.zip)
 
 Step 4 : Extract the above bundle on any linux based machine and navigate to extracted folder

 Step 5 : Download the Service Import script zip file from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Scripts/serviceimport.zip) 
 
 Step 6 : Copy the Service Import script zip file to the directory extracted above in Step 4 and Unzip the service import script bundle.

 Step 7 : Download the Dockerfile from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Dockerfile) and copy to the extracted folder in  
 
 
 ##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier
   
 Ensure your directory in the linux based client machine contains :

- Service import json file (named as kibana_service.json)
- Service import script zip file (named as serviceimport.zip)
- main.py file
- serviceimport.sh
- Kibana logo (named as logo.png)
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
    [root@ip-172-31-27-127 kibana]# chmod 755 kibana_service.json serviceimport.zip logo.png Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

###### [root@ip-172-31-27-127 kibana]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

[root@ip-172-31-27-127 kibana]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

    docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it 
    **[Your IMAGE ID]** /bin/bash

Example:  

[root@ip-172-31-27-127 kibana]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Where to Download The Service Bundles". 

    - Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"Kibana Service imported successfully."**

Step 7: After importing Kibana service successfully, Please import the Elasticsearch service and application profile by following [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Logging/Elasticsearch).

## Service Package Bundle

The Package Service bundle consists of the following files:

Shell script:

 - service: This script will install, configure kibana and installs necessary packages.


# Minimum Resource Specifications

S.No    | Resource   |  Value   | Remarks
------  | ---------- | ---------| ------- 
 1      |  CPU       |  1       |        
 2      |  Memory    |  2 GB    |   
 
 
## Agent Lifecycle Actions 

Agent Action Bundle:  
 - http://YourIP/services/kibana.zip - Location where your agent action bundle zip (service bundle zip file) is found.
 
Agent Lifecycle Actions:
 - Install: Script from bundle: **service install**
 - Configure: Script from bundle: **service configure**
 - Start: Script from bundle: **service start**
 - Stop: Script from bundle: **service stop**
 - Restart: Script from bundle: **service restart**

##### Detailed Steps To Retrieve Data From Elasticsearch To Kibana Dashboard

Step 1 : Deploy ELK application.

Step 2 : In a web browser, go to the public IP address of your Kibana server. You will see the Kibana homepage. 
         
          - http://your_server_ip:5601/
          
Step 3 : Goto Discover in the left side menu, create one index pattern same as elasticsearch index pattern.

Step 4 : Refresh the discover to check the data of elasticsearch in kibana dashboard.



