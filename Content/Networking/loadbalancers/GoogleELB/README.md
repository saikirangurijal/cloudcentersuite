# Google Load Balancer Integration units:
## Introduction:
    The CloudCenter platform supports integration to various Load Balancers. This document provides information on Google Load Balancer integration with Cisco Cloud Center by creating an external service.
    
    Google Cloud Platform Load Balancing gives you the ability to distribute load-balanced compute resources.
    
    Please refer the below link for more details.
    https://cloud.google.com/load-balancing/
	
# Where to Download the service bundles
   Step 1 : Download the service bundle from [here](
https://github.com/datacenter/cloudcentersuite/blob/master/Content/Networking/loadbalancers/F5/WorkloadManager/bundle/f5lb_v3.zip)
   Step 2 : Download the Service Import Json file from [here](
https://github.com/datacenter/cloudcentersuite/tree/master/Content/)
   Step 3 : Download the service import script zip file from [here]()
   Step 4 : Download the [Image logo]() , used while creating the service.
   Step 5 : Download the Modelled Application Profiles from [here](), to be used in Cisco Cloud Center.
   Step 6 : Keep all the files downloaded from previous steps in a single directory 

# How to create a service in Cisco Cloud Center
   User can create the service in two ways.
    - UI
    - By Import Service functionality using script
   The Below Process is applicable for creating a service through UI.
   Step 1 : Login to CloudCenter as an administrator and click on Admin 
            --> Services 
            --> Click on "Add service"
    Step 2 : Provide the inputs as below
        - Service Type: External Service
        - Service logo: Downlad logo from : <location of logo path>
       -  Name: <Your ELB Name> Example : Google ELB 
       -  Service ID: gelb (Do not give different name)
        - Description: Service for Google Load Balancer
       -  Category: Load Balancer
       -  Under External Lifecycle Actions:
       -  External Action Bundle:  
        Select your repository type  on Left : URL / http / S3
        Location on right  : http://<Your IP>/gelb/gelb.zip
        External Lifecycle Actions:
        External Action Bundle: 
        URL : http://<Your IP>/gelb/gelb.zip
        Start:
            Script from bundle: service start
        Stop:
            Script from bundle: service stop
# Configure deployment parameters as below
Deployement Parameters:
| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| gelbProjectname | string | The project id where the service need to be deployed.| <samplename> |  |
| gelbLoadBalancerType |	List |	Type of Load Balancer. For more details on the type of load balancer to choose, check Google cloud documentation | TCP / HTTP / UDP | 
|gelbInstances | String | Comma separated instance names to be configured for the service. Ensure the configured health check path is  available and is responding in all the specified instances for the configured health check to pass
| gelbHealthCheck |	String |	The health check name to be configured for the service. | 

once the deployement parameters filled and save the service file.

The Below Process is applicable for creating a service through script.

Step 1 : unzip  service import script zip file on any Linux System.

Step 2 : Navigate to the extracted directory. Invoke the script as below 
            ./serviceimport.sh
Step 3 : User will be prompted to input the following 
        1) The repository URL where service bundle is placed.
        2) Cloud Center Suite IP Address
        3) User name , password for Cloud Center Suite
        4) Tenant name
        
    Once Authenticated , User will presented with the status of service import.    




 
 
