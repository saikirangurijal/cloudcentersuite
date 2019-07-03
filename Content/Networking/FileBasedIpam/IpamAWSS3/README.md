# File Based IPAM Using AWS S3 

## Introduction
    File Based IPAM will manage the ipaddresses using a .csv file uploaded in AWS S3 only. 
	
    This document provides information on File Based IPAM integration with Cisco Workload Manager.
	
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager

# Download and configure the callouts	

   Step 1 : To create the s3 bucket, refer ([here](https://aws.amazon.com/getting-started/tutorials/backup-files-to-amazon-s3/?nc2=type_a)
   
   Step 2 : Create .csv file with ipaddresses , status with below format.
             
			| your ip | available |
		        | your ip | available |	
             
			Note: "available" is the only keyword to show the status of Ipaddress is free. 
	
   Step 3 : Upload a .csv file to S3 repository in AWS.
			
   Step 4 : Download the Callout script from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Networking/FileBasedIPAM/FileBasedIPAddr_S3.zip)
   
   Step 5 : Extract the above bundle on any linux based machine and navigate to extracted folder. 
   
   Step 6 : Open Ipam folder, Open config.json file and change the below settings.
  
            
             - "domain"                : Domain name
			 
             - "linux_time_zone"       : Set the timezone,
                 For example: "Etc/UTC"
                   
             - "dns_suffix_list"       : Set the Dns suffix List.
             - "dns_server_list"       : Set the Dns Server List.
             - "gateway"               : Gateway of the using network,
             - "netmask"               : Netmask of the using network,
             - "osHostname"            : Hostname,
             - "nicCount"              : Count of nic's,
			 
             - "HwClockUTC"            : UTC Clock or not
	     	     For example: "true"
			 
             - "ACCESS_KEY"            : AWS Access key,
             - "SECRET_KEY"            : AWS Secret key,
             - "region"                : AWS Region ,
             - "bucketName"            : AWS S3 Bucket Name,
             - "filePath"              : File path of uploaded file in AWS S3
   
   Step 7 : Open  ipamdealloc folder.   
            
   Step 8 : Open config.json file and change the below settings based on infoblox ipam setup configuration settings,
   
             - "ACCESS_KEY"             : AWS Access key,
             - "SECRET_KEY"             : AWS Secret key,
             - "region"                 : AWS Region ,
             - "bucketName"             : AWS S3 Bucket Name,
	         - "filePath"               : File path of uploaded file in AWS S3
			 
   Step 9 : Provide executable permissions to the extracted files. Navigate to the directory where all the files are placed and run the below command:
   
                       chmod 755 <your file>
              
   Step 10: Zip the ipam and ipamdealloc folder , as below , from the extracted folder as in step 5.
			
	             Example : zip -r FileIPAM_S3.zip ipam/* ipamdealloc/*
   
   Step 11: Place the modified callout bundle in your file repository
				
		       
		     http://<Your_REPO_Server_IP>/<PATH TO ZIP BUNDLE>
                           
               Example : http://XX.XX.XX.XX/callouts/FileBasedIPAddr_S3.zip 


## Callout Script Bundle

The Packer Service bundle consists of the following files:

IP Allocation :
	Shell Script  : This script will initiate python script.
	Python script : Using API Calls,it allocates the ipv4 address in .csv file and get the details of IPv4 address.


IP De-allocation :
	Shell Script  : This script will initiate python script.
	Python script : Using API Calls,it De-allocates the ipv4 address in .csv file.

		
## Cloud Region parameters 

| Action | Value |
|  ------ |------ |
| Strategy Bundle|callouts/FileBasedIPAddr_S3.zip 
| Instance Naming Strategy|Hostname callout
| Custom VM Name|default
| Instance Ipam Strategy|Ipam Callout
| Ipam alloc rule|ipam/run.sh
| Ipam dealloc rule |ipamdealloc/run.sh


##### Detailed steps for configuring a Callout 

Step 1 : Please refer to cisco workload manager documentation for configuring callout bundles in strategy
           [here](https://docs.cloudcenter.cisco.com/display/SHARED/VM+Naming+and+IPAM+Strategies).
           
           
Step 2 : Deploy an application.

Step 3 : After allocation of the ipaddress to a vm, an extra column to identify ip adress with its vmname will be added in .csv file.

        For Example:
		   | 10.x.x.x | available |
		   | 10.x.x.x | used      | ipam-xxxxxxx
		   
Step 4 : When the deployment is terminated, the ipaddress which is allocated will deallocate and the status of that ipaddress will be changed as "available".

