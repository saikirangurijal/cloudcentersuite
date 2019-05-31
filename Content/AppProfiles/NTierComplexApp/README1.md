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
    


# Download the Application Profile and Package Bundle

   Tomcat without Sensu:
    
Download the Modeled Application Profile with Tomcat from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/AppProfiles/NTierComplexApp/NTierComplexAppWithoutSensu.zip)
   
   Tomcat with Sensu:
  
Download the Modeled Application Profile with Tomcat from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/AppProfiles/NTierComplexApp/NTierComplexAppTomcat.zip)
 
   WebLogic without Sensu:
  
Download the Modeled Application Profile with Weblogic from [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/AppProfiles/NTierComplexApp/NTierComplexAppWeblogic.zip)
	  
	  

# How to create a App Profile in Cisco Workload Manager
   User can create the App Profile by importing the downloaded zip file in
   WorkLoad Manager -> Application Profile -> Import --> Select  App Profile zip file

# How to configure Sensu agent
   
   - By Default it is pre-configured for all tiers except Front-end cache, LB.
        - No other action required . Just go ahead with Deployment 
   
# Note :
  - App Can be viewed in Front-End cache Public ip : 80 port 
  - Sensu dashboard can be viewed in Public IP of Sensu server with port 80 or 3000
  - Tomcat APP only enabled with Sensu. 
  - Weblogic - Single node cluster by default. For multi-node cluster, Please select Persist Private Key under SSH Options during deployment.
  
