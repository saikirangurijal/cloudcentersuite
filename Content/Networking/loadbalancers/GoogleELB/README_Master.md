#  Google Load Balancer
## Introduction
    The Workload Manager supports integration to various Load Balancers as an external service.
    This document provides information on Google Load Balancer integration with Workload Manager 
    by creating an external service.
    
    Google Cloud Platform Load Balancing gives you the ability to distribute load-balanced compute resources.
    
    Please refer the below link for more details.
    https://cloud.google.com/load-balancing/
	
# Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager  

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.

	    Example: 
       wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.


##### PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.


         - Service Zip file under <services_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/gelb.zip 
    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/petclinic.zip


## Service Package Bundle

Shell script:

- service: Initiates the python script to start integration.

Python script :

- install_setup.py: The script will installs necessary python packages also invokes external life cycle action.

- google_load_balancer.py : Script will invoke the all type of loadbalancer using user required like TCP/UDP/HTTP

- google_management.py : Script will invoke the main method of google load balancer.

- common.py: This script contains common functionalities which is required for other script files.

- util.py: utility file.

- error_messages.json : Json file contains error messages.

- error_utils.py: A script that handles error functionality.

# External Lifecycle Actions

External Action Bundle:  
 - http://YourIP/services/gelb.zip - Location where your external action bundle zip (service bundle zip file) is found.
 
External Lifecycle Actions: 
 - Start: Script from bundle: **service start**
 - Stop: Script from bundle: **service stop** 

# Deployment Parameters:

| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| gelbLoadBalancerType |	List |	Type of Load Balancer. For more details on the type of load balancer to choose, check Google cloud documentation | TCP / HTTP / UDP | 
| gelbLoadBalancerName|string  | Give google load balancer name in small case. | <googleloadbalncer> |
| gelbHealthCheck |	String |	The health check name to be configured for the service. | 