# Infoblox IPAM

## Introduction
    The  Workload Manager platform supports integration to Infoblox IPAM (IP address management).
    This document provides information on Infoblox Nios (IPAM) 2.3.1 integration with Cisco Workload Manager.

    Infoblox is an IP address and DNS management tool that is commonly deployed in large IT departments.Often,it is used in conjunction with Vmware or other private clouds for ip allocationa and de allocation.
    
    Please refer the below link for more details.
    https://docs.infoblox.com/display/ILP/NIOS
	
	
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager
- Knowledge on Installation and Configuration of Infoblox IPAM.

# Download and configure the callouts	

   Step 1 : To Install Infoblox server,follow the guide [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/Infoblox/Infoblox-Ipam%20Setup%20Guide.docx)
   
   Step 2 : Download the Callout script from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/Infoblox/InfobloxIPAM.zip)
   
   Step 3 : Extract the above bundle on any linux based machine and navigate to extracted folder. 
   
   Step 4 : Open Ipam folder, Open infoipam.py file and change the below settings based on infoblox ipam setup configuration settings.
  
             - "wapi_version" : Infoblox Version
                     For example: 2.3.1
             - "ib_hostname": Infoblox ipam application ip address with the controller 'api'.
                    For example: "10.193.79.250",
                    
             - "ib_user": Username to login in to infoblox ipam application. By default 'admin' is the username.
             - "ib_pass": Password to login in to infoblox application. By default 'infoblox' is the password.
             - "domain": Domain name which is created while configuring dns in infoblox application.
             - "linux_time_zone" : Set the timezone,
                   For example: "Etc/UTC"
                   
             - "dns_suffix_list" : Set the Dns suffix List.
             - "dns_server_list": Set the Dns Server List.
             - "exclude_from_ipam" : To Exclude these given networks from ipam. Must match the networkId
                   For example: ['apps-201', 'apps-202', 'VM Network']
            
   Step 4 : Open deallocinfoipam.py file in ipamdealloc folder and change the below settings based on infoblox ipam setup configuration settings,
   
             - "wapi_version" : Infoblox Version
                     For example: 2.3.1
             - "ib_hostname": Infoblox ipam application ip address with the controller 'api'.
                    For example: "10.193.79.250",
                    
             - "ib_user": Username to login in to infoblox ipam application. By default 'admin' is the username.
             - "ib_pass": Password to login in to infoblox application. By default 'infoblox' is the password.
             
   Step 6 : Provide executable permissions to the extracted files. Navigate to the directory where all the files are placed and run the below command:
   
              chmod 755 <your file>
              
   Step 7 : Zip the folder with out creating a new folder for all the extracted folders.
   
   Step 9 : Place the modified callout bundle in callouts/<calloutbundle.zip>
   
              - Callout Bundle under callouts/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/callouts/infoblox-ipam.zip 
   
   Step 10: Open the infoblox server application and add required external attributes(Gateway,NetworkId) in the network. 
   Refer the link on how to create external attributes [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/Infoblox/Infoblox-Ipam%20Setup%20Guide.docx)
            
	    For example:
            
                Gateway - 10.193.72.1
                NetworkId - VM Network
  
   Step 11: Configure the external attribute values by modifying each network.

## Callout Script Bundle

The Packer Service bundle consists of the following files:

IP Allocation :
	Shell Script  : This script will initiate python script.
	Python script : Using API Calls,it allocates the ipv4 address in infoblox setup and get the details of IPv4 address.


IP De-allocation :
	Shell Script  : This script will initiate python script.
	Python script : Using API Calls,it De-allocates the ipv4 address in infoblox setup.

		
## Cloud Region parameters 

| Action | Value |
|  ------ |------ |
| Strategy Bundle|callouts/infoblox-ipam.zip
| Instance Naming Strategy|Hostname callout
| Custom VM Name|vmnaming/run.sh
| Instance Ipam Strategy|Ipam Callout
| Ipam alloc rule|ipam/run.sh
| Ipam dealloc rule |ipamdealloc/run.sh


##### Detailed steps for configuring a Callout 

Step 1 : Please refer the documentation on how to configure call out scripts [here](https://docs.cloudcenter.cisco.com/display/SHARED/VM+Naming+and+IPAM+Strategies)

Step 2 : Deploy an application.



