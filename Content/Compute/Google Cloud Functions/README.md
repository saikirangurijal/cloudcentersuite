# Google Cloud Functions
## Introduction

	Google Cloud Functions is a serverless execution environment for building and connecting cloud services.
	Your code executes in a fully managed environment.
	There is no need to provision any infrastructure or worry about managing any servers. 
	
	Cloud Functions can be written using JavaScript, Python 3, or Go runtimes on Google Cloud Platform. 
	You can run your function in any standard Node.js (Node.js 6, 8 or 10), Python 3 (Python 3.7) or 
	Go (Go 1.11) environment.
	
	Please refer the below link for more details.
	For your reference : https://cloud.google.com/functions/docs/concepts/overview
	
## Before you start	
Before importing the Google cloud functions service, user must import Google SQL service in workload manager 'cause google cloud functions function will be invoked on google sql table events (Any CRUD operation).
      
Refer Readme on how to import Google SQL Service from [here](https://github.com/datacenter/cloudcentersuite/blob/master/Content/Databases/DBaaS/GoogleSQL/README1.md).
      


How it works :
- Once application deployed successfully user can access sample Quiz application(which writes data into the google sql). 
- When user triggers the application the inputs of user writes  into a table(dataans)
- After your successful deployment, you can find the URL under Task logs to access your application.

    https://<"Region Name"> - <"Project ID">.cloudfunctions.net/<"Function_Name">

## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above.
- Knowledge on how to use Workload Manager. 
- Deployment Package(appPackage)-Google cloud function package in your apps repository.
 

## Download the service bundles

Step 1 : Download the service bundle from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Compute/Google%20Cloud%20Functions/WorkloadManager/ServiceBundle/googlecloudfunction.zip).

Step 2 : Download the application bundles to be used with application profile
         for google cloud function from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Compute/Google%20Cloud%20Functions/WorkloadManager/ApplicationProfiles/artifacts/quiz-app.zip).

Step 3 : Place the service bundle from Step 1 under services/<bundle.zip> and application bundles from Step 2 under apps/<your_package_name> in your file repository.
          
           - Service Bundle under services/<bundle.zip>
                    
                    Example : http://<Your_REPO_Server_IP>/services/googlecloudfunction.zip 
    
            - Application Bundle under apps/<your_package_name>
              
                    Example : http://<Your_REPO_Server_IP>/quiz-app.zip
                                        
		
Step 4 : Download the integration unit bundle (that contains logo, service json and application profile) from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Compute/Google%20Cloud%20Functions/WorkloadManager/googlecloudfunctions_iu.zip)

Step 5 : Extract the above bundle on any linux based machine and navigate to extracted folder

Step 6 : Download the Service Import script zip file from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip) 

Step 7: Copy the Service Import script zip file to the directory extracted above in Step 5 and Unzip the service import script bundle.

Step 8 : Download the Dockerfile from [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Dockerfile) and copy to the extracted folder in Step 5
 
##### NOTE : Download the "Dockerfile" only if Docker image for service import is not created earlier
   
 Ensure your directory in the linux based client machine contains :

- Service import json file (named as googlecloudfunctions_service.json.json)
- Service import script zip file (named as serviceimport.zip)
- main.py file
- serviceimport.sh
-  logo (named as logo.png)
- Modelled application profile(named as googlecloudfunctions_sample_app.zip)
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
   
   chmod 755 <your file> or chmod 755 *
	
Example : 
    [root@ip-172-31-28-215 Google cloud function]# chmod 755 googlecloudfunctions_service.json serviceimport.zip logo.png googlecloudfunctions_sample_app.zip Dockerfile

##### Step 2: Build a docker image from the same directory where the docker file and other service files are placed. A docker image tagged "ccs_service_import:v1" will be built.

**NOTE BEFORE YOU RUN: Please do not build a new docker image if an image "ccs_service_import:v1" is already created any time before. In such cases , Skip to Step 5.**

###### [root@ip-172-31-28-215 googlecloudfunction]# docker build --no-cache -t ccs_service_import:v1 .

##### Step 3: List the docker images by using "docker images" command

[root@ip-172-31-28-215 googlecloudfunction]# docker images

##### Step 4 : Copy the Image ID of the "ccs_service_import:v1" image, and execute the following command to run the docker image.

    docker run -v **[DIRECTORY WHERE DOWNLOADED FILES ARE PLACED]**:/ccsworker -w /ccsworker -it 
    **[Your IMAGE ID]** /bin/bash

Example:  

[root@ip-172-31-28-215 googlecloudfunction]# docker run -v **[Your directory]**:/ccsworker -w /ccsworker -it **[Your IMAGE ID]** /bin/bash

##### Step 5: User will be requested for the following inputs namely the IP address, Email address, password & the tenant ID of the cloud center suite.

Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

Enter Cloud Center Suite Email Address : YourEmail@XXX.com

Enter the password: ***********

Enter the Tenant ID  : YourTenant

**Note : Logo, Service Json, App profile zip bundle are implicitly read by the script. However, Please ensure that the above mentioned directory contains only above listed files.**

Step 6: You will be prompted to select the file repository in which you have previously added the downloaded service bundle zip file as per section "Where to Download The Service Bundles". 

    - Select the corresponding Repository ID and Hit Enter.

If service creation is successful, You will be presented with a message **"Google cloud function Service imported successfully. Imported Application Profile Successfully"**


### The Packer Service bundle consists of the following files:

Shell script:
 - service: Initiates the python script to start integration.

Python script :
 - install_setup.py: The script will check all mandatory parameters available and installs necessary python packages also invokes external life cycle action.
 - main.py:script will get required environment variables and execute the required functionalities. 
 - googlefunction.py: script that invokes the api for google cloud functions and creates the google cloud function with provided deployment package.
 - util.py: utility file.

## External Lifecycle Actions
    - External Action Bundle:  services/googlecloudfunction.zip
    - External Lifecycle Actions:
        Start:
            Script from bundle: service start
        Stop:
            Script from bundle: service stop

# Service Parameters:
| Parameter Name| Type	 | Mandatory |Description | 
| ------ | ------ | ------ | ------ 
| AppPackage | Path |	Yes |Path of the Deployment Package(.zip). | 
| EntryPoint | String | Yes | Function where google cloud functions starts execution. |  
| Runtime | List | Yes | Need to select required run time for the google cloud functions. | 



# Deployment Parameters:
| Parameter Name| Type	 | Mandatory |Description |  
| ------ | ------ | ------ | ------ 
| functionName |	String | Yes | Name of the google cloud function to be created. |
| Region |	List | Yes | Need to select cloud region for the google cloud functions. | 
| Storage |	String | Yes | To store application in Cloud Storage bucket |  


