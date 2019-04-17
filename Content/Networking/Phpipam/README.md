
# Phpipam IPAM
## Introduction
    The  Workload Manager platform supports integration to PHP IPAM (IP address management).
    This document provides information on Phpipam (IPAM) integration with Cisco Workload Manager.

    Phpipam is an IP address and DNS management tool that is commonly deployed in large IT departments.Often,it is used in conjunction with Vmware or other private clouds for ip allocationa and de allocation.

## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager
- Knowledge on IP Address management and the purpose of the IPAM tools. 	
	
# Download and configure the callouts

   Step 1 : To Install Phpipam server,follow the guide [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Networking/Phpipam/Php-Ipam%20Setup%20Guide.docx)
   
   Step 2 : Download the Callout script from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Networking/Phpipam/php-ipam.zip)
   
   Step 3 :  Extract the above bundle on any linux based machine and navigate to extracted folder. 
   
   Step 4 : Open Ipam folder , Open config.json file in userauth folder  and change the below settings based on phpipam setup configuration settings ,
               
             - "base_url": Phpipam ipam application ip address with the controller 'api'.
                    For example: "http://35.200.172.156/api",
                    
             - "api_name": Api name which have created in API module in phpipam application. 
             - "user": Username to login in to phpipam application. By default 'admin' is the username.
             - "passwd": Password to login in to phpipam application.
             - "domain": Domain name which is created while configuring powerdns.
             - "timeZone" : Set the timezone,
                   For example: "Etc/UTC"
                   
             - "nicDnsServerList_0" : Set the Dns Server List.
             - "DnsServerList": Set the Dns Server List.
             - "exclude_from_ipam" : To Exclude these given networks from ipam. Must match the networkId
                   For example: ['apps-201', 'apps-202', 'VM Network']
    
   Step 5 : Open ipamdealloc folder.
   
   Step 6 : Open config.json file in userauth folder  and change the below settings based on phpipam setup configuration settings,
   
             - "base_url": Phpipam application ip address with the controller 'api'.
                    For example: "http://35.200.172.156/api",
                    
             - "api_name": Api name which have created in API module in phpipam application. 
             - "user": Username to login in to phpipam application. By default 'admin' is the username.
             - "passwd": Password to login in to phpipam application.
             
   Step 7 : Provide executable permissions to the extracted files. Navigate to the directory where all the files are placed and run the below command:
   
             chmod 755 <your file>
   
   Step 8 : Zip the folder with out creating a new folder for all the extracted folders.
     
   Step 9 : Place the modified callout bundle in callouts/<calloutbundle.zip>
   
              - Callout Bundle under callouts/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/callouts/php-ipam.zip 
   
   Step 10 : Open the phpipam server application and add two required subnet custom fields(custom_Gateway,custom_NetworkId).
             Prefer the link to create the custom fields [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Networking/Phpipam/Php-Ipam%20Setup%20Guide.docx)
             For example:
             
                Gateway - 10.193.72.1
                NetworkId - VM Network
                              
   Step 11 : Configure the custom field values by modifying each subnet.
   
## Callout Script Bundle

The Packer Service bundle consists of the following files:

IP Allocation :
	Shell Script  : This script will initiate python script.
	Python script : Using API Calls,it allocates the ipv4 address in phpipam setup and get the details of IPv4 address.


IP De-allocation :
	Shell Script  : This script will initiate python script.
	Python script : Using API Calls,it De-allocates the ipv4 address in phpipam setup.

		
## Cloud Region parameters 

| Action | Value |
|  ------ |------ |
| Strategy Bundle|callouts/php-ipam.zip
| Instance Naming Strategy|Hostname callout
| Custom VM Name|vmnaming/run.sh
| Instance Ipam Strategy|Ipam Callout
| Ipam alloc rule|ipam/run.sh
| Ipam dealloc rule |ipamdealloc/run.sh


##### Detailed steps for configuring a Callout 

Please follow the following procedure IPAM callout:

Step 1 : Please point to cisco cloud suite documentation for configuring callout bundles in strategy. 

Step 2 : Deploy an application.
