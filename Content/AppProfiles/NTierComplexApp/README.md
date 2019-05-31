NTierComplexApp - Typical J2EE Web App

## Introduction

    The Workload Manager platform supports to create and deploy N-Tier complex application profiles
        using  various servies already onboarded on it.

    This document provides information to create  JAVA/J2EE Based Web Application Profile
        with multiple Service Integration.

    This J2EE Typical web app contains following components
	  - Front-End Cache
	  - Back-End Cache
	  - Relational Database 
	  - NoSQL Database
	  - Message Queue
	  - Load Balancer
	  - Monitoring
	  - WebServer/Tomcat OR Middleware/Weblogic Cluster
	  - Logging - Pluggable
	  
	It has two application profiles options., one with Tomcat and another one with Weblogic Server.   

## Feature of the Application

    It is a blogger kind of application. Admin user can login and create and view
 	new blog posts, new users in the Admin Panel. 
	
	User authentication and Management is happening through Relational Database.
	
	NOSQL Database is being used to persist Blog post content.
	
	Back-end Cache is tied on top of Relational Database 
	
	When Admin submits blog post, it queue up in Msg Bus and the same consumed by Mongo DB and persisted.
	
    Load Balancer expose the Application through Private End point of Web/Application Server
	
	Monitoring app is used to monitor WebServer disk Space, CPU usage
	
	Front-End Cache wrap up the entire application at Top Level
 
    **Default Login** : admin/admin 
	
	
# Pre-requisite

   1. CloudCenter 5.x.x and above
   
   2. Knowledge on how to use CloudCenter
   
   3. Mongo DB Cluster Service should be created in Workload Manager for the NOSQL Database Tier 
      - How to Create Mongo DB Cluster Server - Refer from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/tree/master/NoSQL%20Databases/MongoDB%20Cluster)

   4. Make sure that you keep the  Artifacts/Application Package Bundle for the Profiles in your repository under '<repoistory>/apps/complexapp/' folder. Download the Artificat from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/blob/master/AppProfiles/NTierComplexApp/artifacts/complexapp.zip) 
   
   5. Make sure that Sensu Service is exist in Workload Manager.  Refer the Sensu Server service creation steps [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/tree/master/Monitoring/Sensu) 
   
   6. For Weblogic: In addition to Step 4, Make sure that you keep the War for Weblogic in your repository under '<repoistory>/apps/complexapp/' folder. Download the war from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/blob/master/AppProfiles/NTierComplexApp/artifacts/multi-tier-app.war) 

   7. For Weblogic : App With Middleware/Weblogic Cluster option, after steps 4,  Refer the Weblogic Cluster service creation steps [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/tree/master/Middleware/Oracle%20Weblogic)
   
   8. For Weblogic : According to details steps in WebLogic, Make sure download Weblogic Installation Bundle from Oracle website and keept it in your repository under 'images' as 'images/fmw_12.2.1.3.0_wls.zip'.
      Please refer Weblogic pre-requisite.
    
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
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/complexapp/complexapp.zip
			 
# How to configure Sensu agent
   
   - By Default it is pre-configured for all tiers except Front-end cache, LB.
        - No other action required . Just go ahead with Deployment 
			 
# Note :
  - App Can be viewed in Front-End cache Public ip : 80 port 
  - Sensu dashboard can be viewed in Public IP of Sensu server with port 80 or 3000
