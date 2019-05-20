# Integrating with F5 BIG-IP

## Introduction
The CloudCenter platform supports integration to various Load Balancers. This document provides information on integration with F5 by creating an external service in CloudCenter.

F5 BIG-IP provides a wide range of application delivery services, such as server load balancing (SLB), L4-L7 firewall and SSL VPN. With the use of iApps and rich foundation of F5 API, Cisco Cloud Center can deploy F5 virtual servers to provide SLB, FW and SSL VPN services to the applications.

Cisco Cloud Center will maintain the application services catalog, provide consistent and agile L4-L7 services to application deployment in both private and public cloud environments.

## Pre-Requisites

### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use CloudCenter

### F5 BIG-IP
- Release 12.1.x
- Download App Services RPM package from https://github.com/F5Networks/f5-appsvcs-extension/tree/master/dist/latest
- Load it on the BIG-IP - https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/latest/userguide/installation.html#installgui-ref
- BIG-IP management interface must be configured and reachable by Cloud Center
- BIG-IP must be licensed

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to add "yum install wget -y" in case of centos7.

	    Example: 
      wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.

##### PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/f5lb.zip 
    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/opencartapppkg.zip

## Service Package Bundle


The Packer Service bundle consists of the following files:

- service: The main script that has the logic for the integration
- serviceDictionary.csv: The dictionary CSV file that has the list of all the parameters and their defaults. If you want to get addition input from the user, they need to be added to this file and also in the UI. The format of this file is as follows:
```
DisplayName,paramName,paramType,defaultValue
e.g. Root Volume Size,root_volume_size,10
      The parameter name is key here and should match the parameter name in the UI
```
- bigip_rest.py: script that calls the F5 APIs. This python script is called from the main service script.