# Active Directory Domain Services Integration Unit
## Introduction
    The Workload Manager supports integration to various third party services. 
    This document provides information on integration with Active Directory Services
    by creating a Virtual Machine (VM) with Agent service in Workload Manager.
    
    Active Directory stores information about objects on the network and makes this information easy for administrators and users to find and use. 
	Active Directory uses a structured data store as the basis for a logical, hierarchical organization of directory information.
      
    Please refer the below link for more details.
    https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/ad-ds-getting-started
 
 ## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager  
- Ensure Active Directory Domain is up
- Supported OS: Windows Server 2012 


#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

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

         - Service Zip file under <service_path>/<your_script_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/ad-agent.ps1
    
# Service Package Bundle

The Package of Service bundle consists of the following files:

PowerShell script:
 - ad-agent.ps1: This powershell script will add computer to given domain.


# Service Initialization actions
   - Under "Post-Start Script" lifecycle action, agent script would be configured like services/ad-agent.ps1
   
# Minimum Resource Specifications
     
S.No    | Resource    |  Value   | Remarks
----    | ----------  | ---------| ------- 
 1      |  CPU        | 1        |        
 2      |  Memory     | 1 GB     |     
 

 # Global Parameters in Application Profile

| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| userName | String | Domain Controller username |   |  |  |
| dnsServerIp | String | DNS Server IP | | | 
| domainPassword | Password | Domain Controller password | |  |
| domain | String | Domain Name | | |

# Note
	- Please reboot VM Instance after successfully deployed


