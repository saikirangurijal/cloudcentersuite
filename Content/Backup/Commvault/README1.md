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

##### CloudCenter

   - CloudCenter 5.0.1 and above
   - Knowledge on how to use Workload Manager
   - Supported OS (client): CentOS 7
    
# Download App bundles

Step 1 : Download the commvault app package zip file from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Backup/Commvault/WorkloadManager/ServiceBundle/commvault-agent.zip).

Step 2 : Place the app package bundle from Step 1 under apps/<bundle.zip> in a file repository. Its location will be http://YourIP/apps/commvault.zip.

Step 3 : For File/MySQL DB Backup, Download the Sample Modelled Application Profile for Commvault Backup, from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Backup/Commvault/WorkloadManager/ApplicationProfiles/commvault_backup_sample_app.zip).

Step 4 : For File/MySQL DB Restore, Download the Sample Modelled Application Profile for Commvault Restore, from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Backup/Commvault/WorkloadManager/ApplicationProfiles/commvault_restore_sample_app.zip).

Step 5 : For App Profile for Commvault Backup, Pre-start and Post-start script in service Initialization Actions are pre-configured with paths mentioned in section "Service Initialization actions / Node Initialization & Clean Up". Sample App Profile has been given for demo.

Step 6 : For App Profile for Commvault Restore, Pre-start and Post-start script in service Initialization Actions are pre-configured with paths mentioned in section "Service Initialization actions / Node Initialization & Clean Up". Sample App Profile has been given for demo.

Step 7 : Verify whether the commvault app package zip file is placed correctly in file Repository. By default, it will be under apps/commvault.zip.

Step 8 : Login into your Cloud Center Suite with your credentials namely IP address, Email address, Password & Tenant ID. Navigate to App profiles section under Workload Manager.
 - Click on "Import" button found on the top right corner of App profiles section. You will be prompted to choose the application profile that needs to be imported.
 - Choose the App Profile Zip file for Commvault Backup downloaded from Step-3. 
 - Then You will be prompted to map your file repository in which you have placed the commvault app package bundle zip file. Map your file repository.

You will be presented with a message saying "Application Profile Imported Successfully".

Step 9: Repeat Step 8 for importing the App Profile for Commvault Restore by choosing the App Profile Zip file for Commvault restore downloaded from Step-4.

You will be presented with a message saying "Application Profile Imported Successfully".

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
