PetClinic Demo App - Typical J2EE Web App

## Introduction

    The Workload Manager platform supports to create and deploy N-Tier complex application profiles
        using  various servies already onboarded on it.

    This document provides information to create  JAVA/J2EE Based Web Application Profile
        with multiple Service Integration.

    This J2EE Typical web app contains following components
	  - HA-Proxy
	  - MySQL Database
	  - WebServer/Tomcat
	    

## Feature of the Application

    It is Spring Framework demo application
	
	
# Pre-requisite

   1. CloudCenter 5.x.x and above
   
   2. Knowledge on how to use CloudCenter

   3. Make sure that you keep the  Artifacts/Application Package Bundle for the Profiles in your repository under '<repoistory>/apps/' folder. Download the Artificat from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/blob/master/AppProfiles/PetClinicDemoApp/artifacts/demo-app.zip) 
    
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

    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/demo-app.zip
