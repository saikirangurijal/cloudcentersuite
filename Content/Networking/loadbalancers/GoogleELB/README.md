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
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager  

# Download the service bundles

Step 1 : Download the service bundle from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/loadbalancers/GoogleELB/WorkloadManager/ServiceBundle/gelb.zip).
   
Step 2 : Download the application bundle to be used with application profile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/loadbalancers/GoogleELB/WorkloadManager/ApplicationProfiles/artifacts/petclinic.war).

Step 3 : Place the service bundle from Step 1 under services/<bundle.zip> and application bundle from Step 2 under apps/<your_package_name> in your file repository.
          
            - Service Bundle under services/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/services/gelb.zip 
    
            - Application Bundle under apps/<your_package_name>
            
                    Example : http://<Your_REPO_Server_IP>/apps/petclinic.war

Step 4 : Download the integration unit bundle (that contains logo, service json and application profile) from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/loadbalancers/GoogleELB/WorkloadManager/googleelb_iu.zip)
																													
Step 5: Extract the above bundle on any linux based machine and navigate to extracted folder

Step 6 : Download the Service Import script zip file from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip) 
 
Step 7: Copy the Service Import script zip file to the directory extracted above in Step 5 and Unzip the service import script bundle.

Step 8 : Download the Dockerfile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Dockerfile) and copy to the extracted folder in Step 5

NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier

Ensure your directory in the linux based client machine contains :

- Service import json file (named as google_elb.json)
- Service import script zip file (named as serviceimport.zip)
- main.py file
- serviceimport.sh
- Google ELB logo (named as logo.png)
- Modelled application profile(named as GoogleElb_app_profile.zip)
- Dockerfile (named as Dockerfile) , **Only needed if you wish to create a Docker image for the first time**

## How to Create a Service in Cisco Workload Manager

User can create the service by using **Import Service** functionality using script.

#### Prerequisite for creating a service through service import script:

Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx) on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running docker -v
- You can check , if docker is running , by executing the command "systemctl status docker"
  
#### Detailed steps for creating a service through the service import script:

##### Step 1 :Provide executable permissions to the above files. Navigate to the directory where all the files are placed and run the below command:
   
   chmod 755 <your file>

Example : 
    [root@ip-172-31-27-127 googleelb]# chmod 755 google_elb.json serviceimport.zip logo.png GoogleElb_app_profile.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

###### [root@ip-172-31-27-127 googleelb]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

[root@ip-172-31-27-127 googleelb]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

    docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it 
    **[Your IMAGE ID]** /bin/bash

Example:  

[root@ip-172-31-27-127 googleelb]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Where to Download The Service Bundles". 

    - Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"Google ELB Service imported successfully. Imported Application Profile Successfully"**


### The Packer Service bundle consists of the following files:

Shell script:

service: Initiates the python script to start integration.

Python script :

install_setup.py: The script will installs necessary python packages also invokes external life cycle action.

google_load_balancer.py : Script will invoke the all type of loadbalancer using user required like TCP/UDP/HTTP

google_management.py : Script will invoke the main method of google load balancer.

common.py: This script contains common functionalities which is required for other script files.

util.py: utility file.

error_messages.json : Json file contails error messages.

error_utils.py: A script that handles error functionality.

# External Lifecycle Actions as below
    - External Action Bundle:  http://YourIP/services/gelb.zip - Location where your external action bundle zip is found.
    - External Lifecycle Actions:
        Start:
            Script from bundle: service start
        Stop:
            Script from bundle: service stop

# Deployment Parameters:

| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| gelbLoadBalancerType |	List |	Type of Load Balancer. For more details on the type of load balancer to choose, check Google cloud documentation | TCP / HTTP / UDP | 
| gelbLoadBalancerName|string  | Give google load balancer name in small case. | <googleloadbalncer> |
| gelbHealthCheck |	String |	The health check name to be configured for the service. | 