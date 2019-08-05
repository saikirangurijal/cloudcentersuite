# AWS Elastic BeanStalk

## Introduction

    AWS Elastic Beanstalk, can quickly deploy and manage applications in the AWS Cloud 
	without worrying about the infrastructure that runs those applications. 
	
	AWS Elastic Beanstalk reduces management complexity without restricting choice or control. 
	You simply upload your application, and AWS Elastic Beanstalk automatically handles 
	the details of capacity provisioning, load balancing, scaling, and application health monitoring.	 
    
    Please refer the below link for more details.
	https://docs.aws.amazon.com/elastic-beanstalk/ 
	
## Pre-Requisites

#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to execute "yum install wget -y" in case of centos7.

	    Example: 
      wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.


##### PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/elasticbeanstalk.zip 
    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/ebs-petclinic-app.zip
   
## Service Package Bundle

The Package Service bundle consists of the following files:

Shell script:

service: Initiates the python script to start integration.

Python script :

- install_setup.py: The script will install necessary python packages also invokes external life cycle action.

- main.py : The script will invoke the creation of application and environment and trigger the deployment and invoke the deletion of application and termination of deployment.
 
- common.py: The script contains common functionality which is required for other script files.

- util.py: utility file

- error_messages.json : Json file contains error messages.

- error_utils.py: The script that handles error functionality

## External Lifecycle Actions 

External Action Bundle:  
 - http://YourIP/services/elasticbeanstalk.zip - Location where your external action bundle zip (service bundle zip file) is found.
 
External Lifecycle Actions: 
 - Start: Script from bundle: **service start**
 - Stop: Script from bundle: **service stop** 

# Service Parameters:

| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| appPackage |	path |	Path of the Deployment Package(.zip). | ebs-petclinic-app.zip
| appFilePackage|string  | Name of the application file packag inside deployment package | eb_petclinic.zip
		
# Deployment Parameters:

| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| appName |	string |	Name of the application | User Defined Value | PetclinicApp |
| appNameDesc|string  | Application description | User Defined Value | Petclinic with tomcat application description |
| bucketName |	string |	S3 location for uploading application | User Defined Value | ebs-petclinic |
| environmentName|string  | Environment name for the application | User Defined Value | petclinic-env | 
| domainNamePrefix | string | DNS Name | User Defined Value | petclinicapp
| versionLabel | string | Application version label name | User Defined Value | v1.0.0
| platform | list | Run time platform | G0 / .NET / Java / Node Js / Ruby / PHP / Python / Tomcat | Tomcat


