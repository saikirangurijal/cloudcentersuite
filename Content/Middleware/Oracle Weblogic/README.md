# Oracle Weblogic
## Introduction
    The Workload Manager supports integration to various third party services. This document provides information 
    on integration with Weblogic Cluster by creating a Virtual Machine (VM) with Agent service in Workload Manager.
    
    WebLogic Server is a Middleware or Application Server. WebLogic cluster consists of multiple WebLogic Server 
    instances running simultaneously and working together to provide increased scalability and reliability. The 
    server instances that constitute a cluster can run on the same machine, or be located on different machines.

    Please refer the below link for more details.
    https://www.oracle.com/middleware/technologies/weblogic.html
 
## Pre-Requisites
  - This Application Profile uses Azure ELB Service, so first need to import Azure ELB Service from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/loadbalancers/AzureELB).
  - Oracle WebLogic 12C JAR file is mandatory to run weblogic, Please make it available, by purchasing the same from its proprietor. For further details please refer [here](http://download.oracle.com/otn/nt/middleware/12c/12213/fmw_12.2.1.3.0_wls_Disk1_1of1.zip).
  
#### CloudCenter
 - CloudCenter 5.0.1 and above
 - Knowledge on how to use Workload Manager 
 - Supported OS: CentOS 7 
	
# Download the service bundles
   Step 1 : Download the service bundle from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Middleware/Oracle%20Weblogic/WorkloadManager/ServiceBundle/weblogic.zip).
   
   Step 2 : Download the application bundle to be used with application profile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Middleware/Oracle%20Weblogic/WorkloadManager/ApplicationProfiles/artifacts/petclinic.war).

   Step 3 : Convert the Oracle WebLogic JAR file you had purchased, into .zip format, and name it as "weblogicjar.zip".

   Step 4 : Place the service bundle from Step 1 under services/<bundle.zip>, application bundle from Step 2 under apps/<your_package_name> and the converted JAR file from Step 3 under images/<your_jar_to_zip_converted_file> in your file repository.
          
    - Service Bundle under services/<bundle.zip>
                    
                Example : http://<Your_REPO_Server_IP>/services/weblogic.zip 
    
    - Application Bundle under apps/<your_package_name>
            
               Example : http://<Your_REPO_Server_IP>/apps/petclinic.war
                
    - Converted JAR file under images/<your_jar_to_zip_converted_file>
    
               Example :  http://<Your_REPO_Server_IP>/images/weblogicjar.zip
              
  Step 5 : Download the integration unit bundle (that contains logo, service json and application profile) from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Middleware/Oracle%20Weblogic/WorkloadManager/weblogic_iu.zip).
    
  Step 6 : Extract the above bundle on any linux based machine and navigate to extracted folder.

  Step 7 : Download the service import script zip file from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip).
  
  Step 8 : Copy the Service Import script zip file to the directory extracted above in Step 6 and Unzip the service import script bundle.
  
  Step 9 : Download the Dockerfile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Dockerfile) and copy to the extracted folder in Step 6.
  
  ##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier.
  
  Ensure your directory in the linux based client machine contains :

- Service import json file (named as weblogic_service.json)
- Service import script zip file (named as serviceimport.zip)
- main.py file
- serviceimport.sh
- Weblogic logo (named as logo.png)
- Modelled application profile(named as weblogic_sample_app.zip)
- Dockerfile (named as Dockerfile) , **Only needed if you wish to create a Docker image for the first time**

## How to Create a Service in Cisco Workload Manager

User can create the service by using **Import Service** functionality using script.

#### Prerequisite for creating a service through service import script:

Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx) on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running the command "docker -v".
- You can check , if docker is running , by executing the command "systemctl status docker".
  
#### Detailed steps for creating a service through the service import script:

##### Step 1 :Provide executable permissions to the above files. Navigate to the directory where all the files are placed and run the below command:
   
      chmod 755 <your file>

Example : 
    [root@ip-172-31-27-127 weblogic]# chmod 755 weblogic_service.json serviceimport.zip logo.png weblogic_sample_app.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

    [root@ip-172-31-27-127 weblogic]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command.

    [root@ip-172-31-27-127 weblogic]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

    docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it 
    **[Your IMAGE ID]** /bin/bash

Example:  

[root@ip-172-31-27-127 weblogic]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Where to Download The Service Bundles". 

    - Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"weblogic Service imported successfully. Imported Application Profile Successfully"**

# Defaults
 - Application Profile has been configured with 3 Nodes
 
# Notes:
 - After Application Profile is imported **Please specify your WebLogic JAR Repository Location, Weblogic UserName and Password by editing Application Profile**.
 - While deployment **Please select more than 4 CPUs and Minimum 30GB Disk Size**.
 - While deployment **Please select Persist Private Key under SSH Options**.

# Service Package Bundle

The Package of Service bundle consists of the following files:

Shell script:
 - service: This script will set all required environment variables, installs necessary packages and also invokes the external life cycle actions.
 - create-swapspace: This script will create the desired swapspace, which is a mandatory prerequisite before installing weblogic server. 
 - msserver: This shell script will start child nodes NodeManager.
 
Python file:
 - initialize_weblogic_server.py: This script will create basic WebLogic Domain Cluster with Admin ,Manages Servers, JMS and JDBC User.
 - move_domains.py: This script will move primary node domain to all child nodes.
 - run_server.py: This script will start the Cluster, the Admin Server, the Managed Server and deploy the Application.
 - utils.py: This script will have the utility functions.
 
Properties file:
- domain.properties: Properties file for weblogic configuration

# Minimum Resource Specifications

S.No    | Resource     |  Value   | Remarks
----    | ----------   |--------- | ------- 
 1      |  CPU         | 4        |        
 2      |  Memory      | 8 GB    |        
 3      |  Disk Space  | 30 GB     | 


# Agent Lifecycle Actions 
Agent Action Bundle:  
 - http://YourIP/services/weblogic.zip - Location where your agent action bundle zip is found.

Agent Lifecycle Actions:
 - Install: Script from bundle: **service install**
 - Deploy: Script from bundle: **service deploy**
 - Start: Script from bundle: **service start**
 - Stop: Script from bundle: **service stop**
 - Restart: Script from bundle: **service restart**


 # Service Parameters

| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| webLogicVersion | List | Weblogic Version | 12RC  | 12RC|  |
| appPackage |	Path |	 Application Package which is to be deployed on server  |  | | 
| appConfigFile | string  | Application configuration file  |
| appDeployFolder|	string |Application Deployment folder	 | 
| JDK | list |  Java Development Kit(JDK) version| 8| 8|
| webLogicJARPath | path | Repository path where JAR file to install weblogic server is available| | 
| adminUsername | string | Administrator Username  | | |
| adminPassword | string | Administrator Password | | |

