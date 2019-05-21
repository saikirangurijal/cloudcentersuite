# Commvault
## Introduction
    This document briefs down information on integration with commvault in Workload Manager.
    
    Commvault is an enterprise-level data platform that assists in Data Deduplication, Integrated 
    Backup & archiving, Data restoration, Cloud infrastructure & management, Enterprise-level 
    virtual infrastructure protection.
    
    It supports a variety of sources such File Systems, Databases, Virtual Servers, Cloud Apps, etc. 
    Here, Commvault is enabled with the following features:
    
           * Linux File System Backup and Restore
           * MySQL DB Backup and Restore
    
    Please refer the below link for more details.
    https://www.commvault.com/
    
## Pre-Requisites
 - Commserve (Commvault's server component) should be up and running with minimum configuration. For details on Minimum configuration, System requirement and Installation setup, Please refer [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Backup/Commvault/Commvault_Installation_And_SetUp_Manual.docx). 
 - To install CommServe agent in client VMs as part of app profile deployment, Download the Commvault Linux agent from [here](https://cloud.commvault.com/webconsole/downloadcenter/packageDetails.do?packageId=11968&status=0&type=details). Place it in a public access URL(/linux_pkg.tar). Register in commvault.com in order to download. 
 - For File Backup, App Profile should contain any VM with Agent Service (Sample App profile provided).
 - For DB Backup, App Profile should contain VM with MYSQL Service (Sample App profile provided).

Note: Storage Policy/Plan by name "Server Plan" will be created automatically by default. If the plan needs to be customised, Please create a storage plan by referring [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Backup/Commvault/Commvault_Installation_And_SetUp_Manual.docx). 

#### CloudCenter

   - CloudCenter 5.x.x and above
   - Knowledge on how to use Workload Manager
   - Supported OS (client): CentOS 7

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

Once the script is run, please follow the prompts to import application profile.

##### PLEASE NOTE : You will be prompted with location of application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

    - Application Bundle under <app_path>/<your_package_name>
            
               Example : http://<Your_REPO_Server_IP>/<app_path>/commvault-agent.zip


# Application Package Bundle

The Application Package bundle consists of the following files:

Shell scripts:
 - commvaultbackup.sh : This script will set all required environment variables, invokes utility shell scripts and the actual Python file for performing Commvault operations relating to Backup.
 - commvaultrestore.sh : This script will set all required environment variables, invokes utility shell scripts and the actual Python file for performing Commvault operations relating to restore.
 - install_client.sh : This script will be installed on the remote client to be connected with Commserve.
 
Python scripts:
 - commvaultbackup.py : This script will perform Commvault operations relating to Backup by invoking Commvault Python REST APIs.
 - commvaultrestore.py : This script will perform Commvault operations relating to restore by invoking Commvault Python REST APIs.
 - install_agent.py : This script will install the required agents on the client machine.
 
Miscellaneous scripts:
- db_init.sql : This script is invoked to create and setup a Mysql DB before Commvault Backup starts.
- default-final.xml : This script contains the attributes for Client Setup.
- agent.xml : This script contains attributes for agent installation.
- updateinstance.xml : This script contains attributes to update the contents of the instance during Database backup.

# Service Initialization actions / Node Initialization & Clean Up

## Commvault Backup

- Under "Pre-Start Script" lifecycle action, client installation script would be configured like "commvault/install_client.sh". 
- Under "Post-Start Script" lifecycle action, commvault_backup script would be configured like "commvault/commvaultbackup.sh".
- Under "DB Setup Script", DB setup script would be configured like "commvault/db_init.sql".
   
   Note: Ensure Database name is provided, under "General Settings" section in App profile.

## Commvault Restore

- Under "Pre-Start Script" lifecycle action, client installation script would be configured like "commvault/install_client.sh".
- Under "Post-Start Script" lifecycle action, commvault restore script would be configured like "commvault/commvaultrestore.sh".
- Under "DB Setup Script", DB setup script would be configured like "commvault/db_init.sql".

  Note: Ensure Database name is provided, under "General Settings" section in App profile.

# Minimum Resource Specifications

S.No    | Resource    |  Value   | Remarks
----    | ----------  | ---------| ------- 
 1      |  CPU        | 2       |        
 2      |  Memory     | 8 GB     |        
 

# Global Parameters for Commvault Backup 

Parameter Name        | Type    |  Description  | Allowed Value  | Default Value       |  Mandatory  
----                 | ----------| ---------| ------- | ----- | ----- 
commvaultCustomPackageURL    |String    |   CommVault Client Custom Package TAR File to Install in VMs | | http://xxxx/linux_pkg.tar| Yes
commserveName | String |Commvault Server Host Name / Server Name | | | Yes
commvaultServerIp    |String    |   commvault account host name | | | Yes
commvaultUserName   | String    |   commvault account user name |  | | Yes      
commvaultPassword   | Password  |   commvault account password | | |Yes
commCellId  | Number  |   CommCell ID | | 2 | Yes
backupType   | List  |   File System , Database  | | | Yes
dbName   | String  |   Database Name to be backed up | | |No
path   | String  |   File Path to be backed up || | No
authcodevalue   | String  |   Generated Auth Code while downloading Commvault Bundle if exists | | | No

# Global Parameters for Commvault Restore

Parameter Name        | Type    |  Description  | Allowed Value  | Default Value       |    Mandatory
----                 | ----------| ---------| ------- | ----- | ----- 
commvaultCustomPackageURL    |String    |   CommVault Client Custom Package TAR File to Install in VMs  | | http://xxxx/linux_pkg.tar|  Yes
commserveName | String |Commvault Server Host Name / Server Name | | |  Yes
commvaultServerIp    |String    |   commvault account host name |  | |   Yes
commvaultUserName   | String    |   commvault account user name |    | |     Yes    
commvaultPassword   | Password  |   commvault account password |  | |   Yes
commCellId  | Number  |   CommCell ID | | 2 |  Yes
restoreType   | List  |   File System , Database  |  | |   Yes
sourceClient   | String  |   From Which The Backup set would be retrieved for Restore  | | |  Yes
destinationClient   | String  |   To where Backedup Files/Databases to be Restored. Whether it is same Client or Different client  | |current-system|  No
dbName   | String  |   Database Name to be backed up | | |  No
path   | String  |   File Path to be backed up | | |  No
authcodevalue   | String  |   Generated Auth Code while downloading Commvault Bundle if exists | | | No
storagePolicy | String  | Storage Policy / Plan configured in CommServe || Server plan|Yes   