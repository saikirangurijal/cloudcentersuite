J2EE-EcommerceApp - Typical J2EE Ecommerce Web Application using Shopizer

## Introduction

    The Workload Manager platform supports to create and deploy N-Tier complex application profiles
        using  various servies already onboarded on it.

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
	  
	It contains two application profiles in which, one app profile configured with sensu service
	and the other one is not using sensu service.

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

   1. CloudCenter 5.0.1 and above
   
   2. Knowledge on how to use CloudCenter
   
   3. Mongo DB Cluster Service should be created in Workload Manager for the NOSQL Database Tier 
      - How to Create Mongo DB Cluster Server - Refer from [here](https://github.com/datacenter/cloudcentersuite/tree/master/Content/NoSQL%20Databases/MongoDB%20Cluster)

   4. Make sure that you keep the  Application Package related pre/post scripts for the Profiles in your repository under '<repoistory>/apps/shopizer/' folder. Download the Artificat from [here](https://github.com/datacenter/cloudcentersuite/tree/master/Content/AppProfiles/J2EE-EcommerceApp/artifacts/shopizer.zip) 
   
   5. Make sure that you keep the  Application Package Bundles/WAR for the Profiles in your repository under '<repoistory>/apps/shopizer/' folder.
      Download the Artificat from [here](http://13.233.183.37/apps/shopizer/complexapp.war) 
   
   6. Optional: Make sure that Sensu Service is exist in Workload Manager if you are using App Profile with Sensu Service Enabled.  Refer the Sensu Server service creation steps [here](https://github.com/datacenter/cloudcentersuite/tree/master/Content/Monitoring/Sensu) 
   


# Download the Application Profile and Package Bundle

   Sensu Enabled :
      Download the Modeled Application Profile with Sensu Enabled from [here](https://github.com/datacenter/cloudcentersuite/tree/master/Content/AppProfiles/J2EE-EcommerceApp/j2ee-ecommerce_app_with_sensu.zip)

   Without Sensu :
      Download the Modeled Application Profile without Sensu from [here](https://github.com/datacenter/cloudcentersuite/tree/master/Content/AppProfiles/J2EE-EcommerceApp/j2ee-ecommerce_app_without_sensu.zip)

# How to create a App Profile in Cisco Workload Manager
   User can create the App Profile by importing the downloaded zip file in
   WorkLoad Manager -> Application Profile -> Import --> Select  App Profile zip file

# How to configure Sensu agent
   - By Default it is pre-configured with all Service tiers except Front-end cache, LB. No further action required.
# Note :
  - App Can be viewed in Front-End cache Public ip : 80 port 
  - Sensu dashboard can be viewed in Public IP of Sensu server with port 80 or 3000
