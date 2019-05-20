# Sensu Agent
## Introduction
    The Workload Manager supports integration to various third party services. 
	This document briefs down information on integration with Sensu Server by creating 
	a Virtual Machine (VM) with Agent service in Workload Manager.
    
    Sensu agent is a lightweight client that runs on the infrastructure components you want to monitor. 
    Agents register with the Sensu backend as monitoring entities with type: "agent". 
	Agent entities are responsible for creating check and metrics events to send to the backend event pipeline. 
    
    Please refer the below link for more details.
    https://docs.sensu.io/sensu-go/5.3/reference/agent/

# Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager 
- Supported OS: CentOS 7

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

## Importing the Application Profile

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to add "yum install wget -y" in case of centos7.

	    Example: 
        wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".
				

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the application profile.


##### PLEASE NOTE : You will be prompted with location of agent script file on client machine. The files must be copied on to the repository before proceeding to deploy.

       - Service Zip file under <service_path>/sensu-agent/<your_script_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/sensu-agent/sensu-agent

# Agent Bundle

The Package of agent bundle consists of the following files:

Shell script:
 - sensu-agent: This script will install agent and configure the sensu agent with sensu server.


# Service Initialization actions / Node Initialization & Clean Up
   - Under "Pre-Start Script" lifecycle action, agent script would be configured like services/sensu-agent/sensu-agent

# Minimum Resource Specifications

     
S.No    | Resource    |  Value   | Remarks
----    | ----------  | ---------| ------- 
 1      |  CPU        | 1        |        
 2      |  Memory     | 1 GB     |     
  
 
 # Global Parameters in Application Profile
 
   - If sensu server deployment uses default values and credentials,  then add only the below global variable and skip/ignore 2nd table data.

| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| sensuServerHost | String | Sensu Server Host IP Address |   |  |  |

   - If sensu server deployment is not using the default values, then add the following details in App Profile as Global Parameters in addition with the above variable.
   - If the sensu agent needs to point to external sensu server, add the following parameters.

| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| rabbitmqPort | Number | Port for connecting to Sensu Server  |  | 5672 | 
