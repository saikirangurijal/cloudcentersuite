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
  - Oracle WebLogic 12C JAR file is mandatory to run weblogic, Please make it available, by purchasing the same from its proprietor. For further details please refer [here](http://download.oracle.com/otn/nt/middleware/12c/12213/fmw_12.2.1.3.0_wls_Disk1_1of1.zip). 
  
#### CloudCenter
 - CloudCenter 5.0.1 and above
 - Knowledge on how to use Workload Manager 
 - Supported OS: CentOS 7

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

Also, Convert the Oracle WebLogic JAR file you had purchased, into .zip format, and name it as "weblogicjar.zip".

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.

	    Example: 
        wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.

##### PLEASE NOTE : You will be prompted with location of service bundle zip, application bundle zip on client machine. The files (including the weblogic jar_to_zip converted file) must be copied on to the repository before proceeding to deploy.

    - Service Bundle under <services_path>/<bundle.zip>
                    
               Example : http://<Your_REPO_Server_IP>/<services_path>/weblogic.zip 
    
    - Application Bundle under <app_path>/<your_package_name>
            
               Example : http://<Your_REPO_Server_IP>/<app_path>/petclinic.war
                
    - Converted JAR file under <images_path>/<your_jar_to_zip_converted_file>
    
               Example :  http://<Your_REPO_Server_IP>/<images_path>/weblogicjar.zip

# Defaults
 - Application Profile has been configured with 3 Nodes
 
##### Notes:
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
