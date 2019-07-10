# BlueCat Address Manager

## Introduction
    The  Workload Manager platform supports integration to Bluecat Address Manager.
    This document provides information on BlueCat Address Manager 9.0.0 integration with Cisco Workload Manager.

    BlueCat Address Manager is a powerful IP Address Management software that lets you control your complex and dynamic network. 
    With integrated core services, workflow and automation, you can centrally manage every connected device on your network from a single pane of glass with BlueCat.
    
    Please refer the below link for more details.
    https://www.bluecatnetworks.com/platform/management/bluecat-address-manager/
	
	
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager
- Knowledge on Installation and Configuration of BlueCat Address Manager.

# Download and configure the callouts	

   Step 1 : To Install BlueCat Address Manager,follow the guide [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/BlueCat/BlueCat%20Setup%20Guide.docx)
   
   Step 2 : Download the Callout script from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/BlueCat/bluecat.zip)
   
   Step 3 : Extract the above bundle on any linux based machine and navigate to extracted folder. 
   
   Step 4 : Open bamalloc folder, Open config.json file and change the below settings based on Bluecat Address Manager setup configuration settings.
  
             - "bluecat_hostname": BlueCat Address Manager application ip address with the controller 'api'.
                    For example: "10.36.5.10",
                    
             - "bluecat_user": Username to login in to BlueCat Address Manager application. 
             - "bluecat_pass": Password to login in to BlueCat Address Manager application.
                (user should have the the API access) 
             - "configuration_name": Name of the configuration in which your network resides.
             - "linux_time_zone" : Set the timezone,
                   For example: "Etc/UTC"
             - "dns-view": DNS View created in the BlueCat Address Manager application.             
             - "dns-zone":DNS Zone created inthe BlueCat Address Manager application.   
             - "dns_server_list": Set the Dns Server List.
             - "exclude_from_ipam" : To Exclude these given networks from ipam. Must match the networkId
                   For example: ['apps-201', 'apps-202', 'VM Network']
   
   Step 5 : Open  bamdealloc folder.   
            
   Step 6 : Open config.json file and change the below settings based on BlueCat Address Manager setup configuration settings,
   
             - "bluecat_hostname": BlueCat Address Manager application ip address with the controller 'api'.
                    For example: "10.36.5.10",
                    
            - "bluecat_user": Username to login in to BlueCat Address Manager application. 
            - "bluecat_pass": Password to login in to BlueCat Address Manager application. 
                (user should have the the API access)
             
   Step 7 : Provide executable permissions to the extracted files. Navigate to the directory where all the files are placed and run the below command:
   
              chmod 755 <your file>
              
   Step 8 : Zip the folder with out creating a new folder for all the extracted folders.
   
   Step 9 : Place the modified callout bundle in callouts/<calloutbundle.zip>
   
              - Callout Bundle under callouts/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/callouts/bluecat.zip 
   
   Step 10: Open the BlueCat Address Manager application and add required external attributes-(Gateway) in the network.
            Refer the link to know how to create external attributes [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/BlueCat/BlueCat%20Setup%20Guide.docx)
            For example:
            
                Gateway - 10.36.0.0
          
   Step 11: Configure the external attribute values.
   

## Callout Script Bundle

The Packed Service bundle consists of the following files:

IP Allocation :
	Shell Script  : This script will initiate python script.
	Python script : Using API Calls,it allocates the ipv4 address in BlueCat Address Manager and get the details of IPv4 address.


IP De-allocation :
	Shell Script  : This script will initiate python script.
	Python script : Using API Calls,it De-allocates the ipv4 address in BlueCat Address Manager.

		
## Cloud Region parameters 

| Action | Value |
|  ------ |------ |
| Strategy Bundle|callouts/bluecat.zip
| Instance Naming Strategy|Hostname callout
| Custom VM Name|vmnaming/run.sh
| Instance Ipam Strategy|Ipam Callout
| Ipam alloc rule|bamalloc/run.sh
| Ipam dealloc rule |bamdealloc/run.sh


##### Detailed steps for configuring a Callout 

Step 1 : Please refer to cisco workload manager documentation for configuring callout bundles in strategy
           [here](https://docs.cloudcenter.cisco.com/display/SHARED/VM+Naming+and+IPAM+Strategies).
           
           
Step 2 : Deploy an application.



