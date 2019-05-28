# Splunk Agent
## Introduction
    The Workload Manager supports integration to various third party services. 
    This document provides information on integration with Splunk Server 
    by creating a Virtual Machine (VM) with Agent service in Workload Manager.
    
    Splunk Enterprise is a software product that enables you to search, analyze, 
	and visualize the data gathered from the components of your IT infrastructure or business. 
	Splunk Enterprise takes in data from websites, applications, sensors, devices, and so on. 
	After you define the data source, Splunk Enterprise indexes the data stream and parses 
	it into a series of individual events that you can view and search.

	There are three types of Data forwarders:

		- The universal forwarder contains only the components that are necessary to forward 
		  data. Learn more about the universal forwarder in the Universal Forwarder manual.
		- A heavy forwarder is a full Splunk Enterprise instance that can index, search, and 
		  change data as well as forward it. 
			 The heavy forwarder has some features disabled to reduce system resource usage.
		- A light forwarder is also a full Splunk Enterprise instance, with more features disabled 
		  to achieve as small a resource footprint as possible. 
			 The universal forwarder supersedes the light forwarder for nearly all purposes and 
			 represents the best tool for sending data to indexers.

    Please refer the below link for more details.
    https://docs.splunk.com/Documentation/Splunk/6.0/Forwarding/Typesofforwarders
	
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager  
- Ensure Splunk server is up and running
- Supported OS: CentOS 7

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

## Importing the application profile

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to execute "yum install wget -y" in case of centos7.

	    Example: 
      wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".
				

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the application profile.

##### PLEASE NOTE : You will be prompted with location of agent script file and application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/splunk-agent/<your_script_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/splunk-agent/splunk-agent 
    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/petclinic.war

# Agent Bundle

The Package of Agent bundle consists of the following files:

Shell script:
 - splunk-agent: This script will install agent and configure the splunk agent with splunk server.

# Service Initialization actions
   - Under "Post-Start Script" lifecycle action, agent script would be configured like services/splunk-agent/splunk-agent
   
# Minimum Resource Specifications
     
S.No    | Resource    |  Value   | Remarks
----    | ----------  | ---------| ------- 
 1      |  CPU        | 1        |        
 2      |  Memory     | 1 GB     |     
 

 # Global Parameters in Application Profile

| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| splunkServerHost | String | Splunk Server Host IP |   |  |  |
| splunkForwarderPort | Number | Data Forwarder Port to Server as same as Receiver Port in Splunk Server | 81-65534 (Splunk Server Receiver Port) | 9997 | 
| splunkServerUserName | String | Splunk Server UserName | | admin |
| splunkServerPassword | Password | Splunk Server Password | | |
| logPath | String | Monitoring Log File Path | | /var/log | 
   
 