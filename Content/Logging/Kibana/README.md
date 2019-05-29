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

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to add "yum install wget -y" in case of centos7.

	    Example: 
        wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.


##### PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/kibana.zip 
   
## Service Package Bundle

The Package Service bundle consists of the following files:

Shell script:

- service: This script will install kibana and installs necessary packages, loads configuration and also invokes the agent life cycle actions.


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


