# Azure Backup Service

   ## Introduction
   The Azure Backup service backs up Azure Virtual Machines to the Microsoft Azure cloud.It provides independent and isolated backups to 
   guard against accidental destruction of original data. Backups are stored in a Recovery Services vault with built-in managed of recovery points.
   
   Please refer the below link for more details.
   
   For your reference : https://docs.microsoft.com/en-us/azure/backup/backup-overview
	
## Before you start
 For Single-Tier, make sure that Azure Virtual Machines exists in same region where the Recovery Service Vault exists beacause the Vault 
 will allow to take the backup of Virtual Machines if it exists in same region only.
	
## How it works
   1. Import the service and application profile using Import service script. Refer 
   section ## Importing the service.It creates application profiles Azure_Backup_Service and NTierAzureBackupService.
   
   2. Backup the AzureVM  using above profile by providing Recovery Service vault name and Azure Virtual Machine Name.
   
   3. After your successful deployment, the Recovery Service vault will be created and our Azure Virtual Machines will 
   be stored under backupitems of vault,the backup will be taken as per the defaultpolicy.We can find the backitems under Recovery Service
   vault exists in azureportal(https://portal.azure.com/)
   
## Limitations
   1. We can create up to 500 Recovery Services Service
	  vaults, per supported region of Azure Backup, per subscription.
   
   2. We can register up to 1000 Azure Virtual machines per vault..
   
   3. Backup data stored in a vault can't be moved to a different vault.
   
   4. We can  back up Azure VMs once a day.
   
   5. Azure Backup doesn't support deleting or purging individual items from 
      stored backups
    
   ## Docker Install

1. Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"	
 	

## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above.
- Knowledge on how to use Workload Manager. 
 

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to execute "yum install wget -y" in case of centos7.

	    Example: 
      wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.

##### PLEASE NOTE : You be prompted with location of service bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/azurebackupservice.zip
			 

## Service Package Bundle

The Packer Service bundle consists of the following files:

Shell script:
 - service: Initiates the python script to start integration.

Python script :
 - azure_backup.py : script that invokes the rest APIs to backup AzureVMs. 
 - main.py - calling functions based on operations like startbackup,stop and delete backup
 - util.py: utility file
 - error_messages.json : Json file contains error messages.
 - error_utils.py: The script that handles error functionality.
  

## External Lifecycle Actions
    - External Action Bundle:   http://YourIP/services/azurebackupservice.zip
    - External Lifecycle Actions:
        Start:
            Script from bundle: service start
        Stop:
            Script from bundle: service stop


## Deployment Parameters(Single-Tier):
| Parameter Name| Type	 | Mandatory |Description |  
| ------ | ------ | ------ | ------   
| vaultname |	String | Yes | Name of the Recovery vault where backup will be taken. |
| vm_name | String | Yes | Azure Virtual Machine name which we need to take backup. | 
| policyname | String | No | Backup policy name if exists for vaultname provided. If not, DefaultPolicy will be applied |

## Deployment Parameters(N-Tier):
| Parameter Name| Type	 | Mandatory |Description |
| ------ | ------ | ------ | ------
| vaultname |	String | Yes | Name of the Recovery vault where backup will be taken. |
| policyname | String | No | Backup policy name if exists for vaultname provided. If not, DefaultPolicy will be applied |


