# Splunk Agent
## Introduction
    The Workload Manager supports integration to various third party services. 
    This document provides information on integration with Splunk Server 
    by creating a Virtual Machine (VM) with Agent service in Workload Manager.
    
    Splunk Enterprise is a software product that enables you to search, analyze, 
	and visualize the data gathered from the components of your IT infrastructure or business. 
	Splunk Enterprise takes in data from websites, applications, sensors, devices, and so on. 
	After you define the data source, Splunk Enterprise indexes the data stream and parses it into a series of individual events that you can view and search.

	There are three types of Data forwarders:

		- The universal forwarder contains only the components that are necessary to forward data. Learn more about the universal forwarder in the Universal Forwarder manual.
		- A heavy forwarder is a full Splunk Enterprise instance that can index, search, and change data as well as forward it. 
			The heavy forwarder has some features disabled to reduce system resource usage.
		- A light forwarder is also a full Splunk Enterprise instance, with more features disabled to achieve as small a resource footprint as possible. 
			The universal forwarder supersedes the light forwarder for nearly all purposes and represents the best tool for sending data to indexers.

    Please refer the below link for more details.
    https://docs.splunk.com/Documentation/Splunk/6.0/Forwarding/Typesofforwarders
	
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use CloudCenter 
- Ensure Splunk server is up and running.
  
## Where to Download the service bundles
 Step 1 : Fetch Splunk agent File by copying & pasting the contents from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Logging/Splunk-Agent/WorkloadManager/src/splunk-agent/splunk-agent) into a new file named "splunk-agent". Place the file in a repository and its location is http://YourIP/services/splunk-agent/splunk-agent.
 
 Step 2 : With any existing App Profile, this agent script can be configured by defining value with proper repository path like  "services/splunk-agent/splunk-agent" under "Post Start script" in service Initialization  Actions. Sample App Profile has been given for demo.
   
 Step 3 : Download the Sample Modelled Application Profiles with splunk agent pre-configured in Service lifecycle action, from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Logging/Splunk-Agent/WorkloadManager/splunk-agent_iu.zip)
 
 Step 4 : Verify the location of the application packages and Agent File in file Repository. Make sure its placed correctly, By default Application Package will be under apps/your-packages and Node Lifecycle Agent file will be under services/splunk-agent/<splunk-agent-file>.
   
 Step 5 : Login into your Cloud Center Suite with your credentials namely IP address, Email address, Password & Tenant ID. Navigate to App profiles section under Workload Manager. Click on "Import" button found on the top right corner of App profiles section. You will be prompted to choose the application profile that needs to be imported. Choose the Modelled Application Profile Zip file extracted from Step-3 downloaded splunk-agent_iu.zip file. Then You will be prompted to map your file repository in which you have placed the Node Lifecycle Agent file. Map your file repository.
   
You will be presented with a message saying "Application Profile Imported Successfully".
   
# Service Package Bundle

The Package of Service bundle consists of the following files:

Shell script:
 - splunk-agent: This script will install agent and configure the splunk agent with splunk server.


# Service Initialization actions
   - Under "Post-Start Script" lifecycle action, agent script would be configured like services/splunk-agent/splunk-agent
   
# Minimum Resource Specifications
     
S.No    | Resource    |  Value   | Remarks
----    | ----------  | ---------| ------- 
 1      |  CPU        | 1        |        
 2      |  Memory     | 1 GB     |     
 
 # Supported Cloud and OS

S.No    | Cloud   |  OS   
------  | ---------- | --------- 
 1      |  Google    |  CentOS 7 , Ubuntu 16 and Ubuntu 14               
 2      |  Azure     |  CentOS 7 , Ubuntu 16 and Ubuntu 14
 3      |  AWS     |  CentOS 7 and Ubuntu 14

 # Global Parameters in Application Profile

| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| splunkServerHost | String | Splunk Server Host IP |   |  |  |
| splunkForwarderPort | Number | Data Forwarder Port to Server as same as Receiver Port in Splunk Server | 81-65534 (Splunk Server Receiver Port) | 9997 | 
| splunkServerUserName | String | Splunk Server UserName | | admin |
| splunkServerPassword | Password | Splunk Server Password | | |
| logPath | String | Monitoring Log File Path | | /var/log | 
   
 
