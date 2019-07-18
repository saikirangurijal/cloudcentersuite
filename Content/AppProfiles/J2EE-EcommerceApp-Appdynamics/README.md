J2EE-EcommerceApp - Typical J2EE Ecommerce Web Application using Shopizer

## Introduction

    The Workload Manager platform supports to create and deploy N-Tier complex application profiles
        using  various services already onboarded on it.

    This document provides information to create  JAVA/J2EE Based Web Application Profile
        with multiple Service Integration.

    This J2EE Ecommerce Web Application contains following components
	  - Front-End Cache
	  - Back-End Cache
	  - Relational Database 
	  - NoSQL Database
	  - Message Queue
	  - Load Balancer
	  - Monitoring 
	  - Web Server
	  
	 Application profile configured with Appdynamics.

## Feature of the Application

    It is a J2EE Ecommerce web application. Admin user can manage contents, configure catalogue, payments
	and schedule feature products. Guest users can add products to cart, checkout and submit the orders.
	
	User authentication and Management is happening through Relational Database.
	
	NOSQL Database is being used to persist application admin events 
	
	Back-end Cache is tied on top of Relational Database 
	
	When Admin submits product it queue up in Msg Bus and the same consumed by Releational Database.
	
    Load Balancer expose the Application through Private End point of Web/Application Server
	
	Monitoring app is used to monitor WebServer disk Space, CPU usage
	
	Front-End Cache wrap up the entire application at Top Level
 
    **Default Admin Login** : admin/password
	**Default Admin URL ** : /admin
	
# Pre-requisite

   1. CloudCenter 5.x.x and above
   
   2. Knowledge on how to use CloudCenter
   
   3. Mongo DB Cluster Service should be created in Workload Manager for the NOSQL Database Tier 
      - How to Create Mongo DB Cluster Server - Refer from [here](https://github.com/datacenter/cloudcentersuite/tree/master/Content/NoSQL%20Databases/MongoDB%20Cluster)

   4. Make sure that you keep the  Application Package related pre/post scripts for the Profiles in your repository under '<repoistory>/apps/shopizer/' folder. Download the Artifact from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/blob/master/AppProfiles/J2EE-EcommerceApp-Appdynamics/artifacts/shopizer.zip?raw=true) 
   
   5. Make sure that you keep the  Application Package Bundles/WAR for the Profiles in your repository under '<repoistory>/apps/shopizer/' folder.
      Download the Artifact from [here](https://s3.amazonaws.com/contentfactory/apps/shoppingcart/complexapp.war) 
   
   6. Tomcat9 Service should be created in Workload Manager for the webserver Tier  [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/tree/master/Web%20Server/Tomcat9) 
   
   7. Make sure that Appdynamics controller is running.
   
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
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/shopizer/shopizer.zip
			 
# Note :
  -  Before deployment get credntials of your Appdynamics controller to give inputs for deployment parameters. 
  -  App Can be viewed in Front-End cache Public ip : 80 port
