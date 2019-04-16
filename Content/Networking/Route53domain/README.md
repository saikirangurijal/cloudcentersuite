# AWS Route53Domain
## Introduction

	Amazon Route 53 is a highly available and scalable Domain Name System (DNS) web service.
    Amazon Route 53 console to register a domain name and configure Route 53 to route with unique domain name.

Please refer the below link for more details.
	For your reference : https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/

## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager 

# Download the service bundles

Step 1 : Download the service bundle from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/Route53domain/WorkloadManager/ServiceBundle/awsroute53domain.zip).
   
Step 2 : Place the service bundle from Step 1 under services/<bundle.zip> and application bundle in your file repository.
          

 - Service Bundle under services/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/services/awsroute53domain.zip
					
Step 3 : Download the integration unit bundle (that contains logo, service json and application profile) from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/Route53domain/WorkloadManager/awsroute53domain_iu.zip)

Step 4: Extract the above bundle on any linux based machine and navigate to extracted folder

Step 5 : Download the Service Import script zip file from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip) 
 
Step 6: Copy the Service Import script zip file to the directory extracted above in Step 5 and Unzip the service import script bundle.

Step 7 : Download the Dockerfile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Dockerfile) and copy to the extracted folder in Step 4

##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier
   
 Ensure your directory in the linux based client machine contains :

- Service import json file (named as awsroute53domain_service.json)
- Service import script zip file (named as serviceimport.zip)
- main.py file
- serviceimport.sh
- Route53domain logo (named as logo.png)
- Modelled application profile(named as awsroute53domain_sample_app.zip)
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
    [root@ip-172-31-27-127 route53]# chmod 755 awsroute53domain_service.json serviceimport.zip logo.png route53domain_app_profile.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

###### [root@ip-172-31-27-127 route53]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

[root@ip-172-31-27-127 route53]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

    docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it 
    **[Your IMAGE ID]** /bin/bash

Example:  

[root@ip-172-31-27-127 route53]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Download The Service Bundles". 

    - Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"Route53domain Service imported successfully. Imported Application Profile Successfully"**


## Service Package Bundle
The Packer Service bundle consists of the following files:

Shell script:
 - service: Initiates the python script to start integration.

Python script :
 - install_setup.py: The script will check all mandatory parameters available and installs necessary python packages also invokes external life cycle action.
 - amazon_domain_creation.py: script that invokes the api for route53 functions will domain availability and creatoing domain.
 - prerequiste_environments.py : Script will check required parameter for route53 management
 - domaincreation.json : input template json for route53 domain creation
 - util.py: utility file
 - error_utils.py: A script that handles error functionality

# External Lifecycle Actions as below
    - External Action Bundle:  services/awsroute53.zip
    - External Lifecycle Actions:
        Start:
            Script from bundle: service start

# Deployment Parameters:
| Parameter Name| Type	 | Mandatory |Description | Allowed Value |Default Value |
| ------ | ------ | ------ | ------ |------ | ------ |
| DomainName |	String | Yes | Mention Unique Domain Name for creating domain in AWS  |  |   |
| FirstName | String | Yes	| Mention First Name |  | |
| LastName | String |	Yes | Mention Last Name | | |
| ContactType | String | Yes | Mention Contact type of Person | <PERSON','COMPANY','ASSOCIATION','PUBLIC_BODY','RESELLER'> | |
| Organization | String | Yes | Mention Organization Name |  | |
| AddressLine1 | String | Yes | Mention first line of address  |  | |
|AddressLine2| String | Yes | Mention second line of address  |  | |
|City|String | Yes | Mention city name  |  | |
|PhoneNumber|String | Yes | Mention Phonenumber in format of <+01>.<123456789>  |  | |
|StateCode| String | Yes | Mention statecode in length of 2 char   | <TN,BG,AP,KL etc,.> | |
|CountryCode| String | Yes | Mention Country code in length of 2 char  |<IN,US,UK,AS,ML,SA etc,.>  | |
|zipcode| String | Yes | Mention Zip code of city  |  | |
|Email| String | Yes | Mention Valid Email Address   |  | |
