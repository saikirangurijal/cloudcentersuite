# Integrating with F5 BIG-IP

## Introduction

The CloudCenter platform supports integration to various Load Balancers. This document provides information on integration with F5 by creating an external service in CloudCenter.

F5 BIG-IP provides a wide range of application delivery services, such as server load balancing (SLB), L4-L7 firewall and SSL VPN. With the use of iApps and rich foundation of F5 API, Cisco Cloud Center can deploy F5 virtual servers to provide SLB, FW and SSL VPN services to the applications.

Cisco Cloud Center will maintain the application services catalog, provide consistent and agile L4-L7 services to application deployment in both private and public cloud environments.


### CloudCenter
- CloudCenter 5.0 and above
- Knowledge on how to use CloudCenter

### F5 BIG-IP
- Release 12.1.x
- Download App Services iApps 2.0 from GitHub and import into BIG-IP
- BIG-IP management interface must be configured and reachable by Cloud Center
- BIG-IP must be licensed

## Download the service bundles

 **Step 1** : Download the Service Bundle zip from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/loadbalancers/F5/WorkloadManager/ServiceBundle/f5lb.zip).

 **Step 2** : Download the application bundle to be used with application profile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/loadbalancers/F5/WorkloadManager/ApplicationProfiles/artifacts/opencartapppkg.zip).

 **Step 3** : Place the service bundle from Step 1 under services/<bundle.zip> and application bundle from Step 2 under apps/<your_package_name> in your file repository.

            - Service Bundle under services/<bundle.zip>

                    Example : http://<Your_REPO_Server_IP>/services/f5lb.zip

            - Application Bundle under apps/<your_package_name>

                    Example : http://<Your_REPO_Server_IP>/apps/opencartapppkg.zip

 **Step 4** : Download the integration unit bundle (that conatins logo, service json and application profile) from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Networking/loadbalancers/F5/WorkloadManager/f5_iu.zip)

 **Step 5**: Extract the above bundle on any linux based machine and navigate to extracted folder

 **Step 6** : Download the Service Import script zip file from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/Scripts/serviceimport.zip)

 **Step 7**: Copy the Service Import script zip file to the directory extracted above in Step 5 and Unzip the service import script bundle.

 **Step 8** : Download the Dockerfile from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Dockerfile) and copy to the extracted folder in Step 5

 ##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier

 Ensure your directory in the linux based client machine contains :

- Service import json file (named as f5_service.json)
- Service import script zip file (named as serviceimport.zip)
- main.py file
- serviceimport.sh
- F5 logo (named as logo.png)
- Modelled application profile(named as f5.png)
- Dockerfile (named as Dockerfile) , **Only needed if you wish to create a Docker image for the first time**

## How to Create a Service in Cisco Workload Manager

User can create the service by using **Import Service** functionality using script.

#### Prerequisite for creating a service through service import script:

Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx) on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine.
- You can check , if docker is installed , by running docker -v
- You can check , if docker is running , by executing the command "systemctl status docker"

#### Detailed steps for creating a service through the service import script:

##### Step 1 :Provide executable permissions to the above files. Navigate to the directory where all the files are placed and run the below command:

    chmod 755 <your file>


Example :
    [root@ip-172-31-27-127 f5lb]# chmod 755 f5_Service.json serviceimport.zip logo.png f5_sample_app.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

    [root@ip-172-31-27-127 f5lb]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

    [root@ip-172-31-27-127 googlesql]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

    docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it
    **[Your IMAGE ID]** /bin/bash

Example:  

[root@ip-172-31-27-127 googlesql]# docker run -v /root/serviceimport/:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Where to Download The Service Bundles".

    - Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"F5-BIG-IP service  imported successfully. Imported Application Profile Successfully"**


## Service Package Bundle


The Packer Service bundle consists of the following files:

- service: The main script that has the logic for the integration
- serviceDictionary.csv: The dictionary CSV file that has the list of all the parameters and their defaults. If you want to get addition input from the user, they need to be added to this file and also in the UI. The format of this file is as follows:
```
DisplayName,paramName,paramType,defaultValue
e.g. Root Volume Size,root_volume_size,10
      The parameter name is key here and should match the parameter name in the UI
```
- bigip_rest.py: script that calls the F5 APIs. This python script is called from the main service script


```
