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
### Docker Installation
Before you start with service import, Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"
      
### Googlesql Import
Before importing the Google cloud functions service, user must import Googlesql service in workload manager because Google cloud functions will be invoked on Googlesql table events (Any CRUD operation).
      
Refer Readme on how to import Google cloud functions Service from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/tree/master/Databases/GoogleSQL).
      
The Google cloud function service will create a Cloud function with provided name in Google Cloud.

How it works :
- Once application deployed successfully user can access sample Quiz application(which writes data into the google sql). 
- When user triggers the application the inputs of user writes  into a table(dataans)
- To access the application after deployment trigger the url with required changes.

    https://<Region>-<Project - ID>.cloudfunctions.net/<Function_Name>

## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above.
- Knowledge on how to use Workload Manager. 
- Deployment Package(appPackage)-Google cloud function package in your apps repository.
 

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to execute "yum install wget -y" in case of centos7.

	    Example: 
      wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.


##### PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip(s) on client machine. The files must be copied on to the repository before proceeding to deploy.
          
           - Service Bundle under <service_path>/<your_bundle_name>
                    
                    Example : http://<Your_REPO_Server_IP>/<service_path>/googlecloudfunction.zip 
    
            - Application Bundle under <app_path>/<your_package_name>
            
                    Example : http://<Your_REPO_Server_IP>/<app_path>/quiz-app.zip
                                        
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


