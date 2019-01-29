# Google Load Balancer Integration Units
## Introduction
    The CloudCenter platform supports integration to various Load Balancers as an external service.
    This document provides information on Google Load Balancer integration with Cisco Cloud Center 
    by creating an external service.
    
    Google Cloud Platform Load Balancing gives you the ability to distribute load-balanced compute resources.
    
    Please refer the below link for more details.
    https://cloud.google.com/load-balancing/
	
# Where to Download the service bundles
   Step 1 : Download the service bundle from [here](https://github.com/datacenter/cloudcentersuite/blob/master/Content/Networking/loadbalancers/GoogleELB/WorkloadManager/bundle/gelb.zip)
   
   Step 2 : Download the Service Import Json file from [here](https://github.com/datacenter/cloudcentersuite/blob/master/Content/Networking/loadbalancers/GoogleELB/WorkloadManager/google.json)
   
   Step 3 : Download the service import script zip file from [here](https://github.com/datacenter/cloudcentersuite/blob/master/Content/scripts/serviceimport.zip)
   
   Step 4 : Download the Load Balancer logo from [here](https://github.com/datacenter/cloudcentersuite/blob/master/Content/Networking/loadbalancers/GoogleELB/WorkloadManager/GoogleLB.png). It is used while creating the service and is mandatory. 
   
   Step 5 : Download the Modelled Application Profiles from [here](https://github.com/datacenter/cloudcentersuite/blob/master/Content/Networking/loadbalancers/GoogleELB/WorkloadManager/gelb_app_profile.zip)
   
   Step 6 : Keep all the files downloaded from steps 2-5 in a single directory on a Linux based client machine. The Next section explains on how to create a service using command line utility.
   
   Step 7 : Place the service bundle downloaded from Step 1 in to a file repository.

# How to create a service in Cisco Cloud Center
   User can create the service in two ways.
   - Using the **Add Service** from User Interface 
   - Using **Import Service** functionality using script  
 ##### Detailed steps for creating a service through UI
###### Step 1 : Login to CloudCenter as an administrator 
- Click on Admin Menu Item 
- Click on Services 
- Click on "Add service" link on top right corner
###### Step 2 : Provide the inputs as below
- Service Type: External Service
- Service logo: Downlad logo from [here](https://github.com/datacenter/cloudcentersuite/blob/master/Content/Networking/loadbalancers/GoogleELB/WorkloadManager/GoogleLB.png)
- Name: Your ELB Name  
- Service ID: gelb (Do not give different name)
- Description: Service for Google Load Balancer
- Category: Load Balancer
- ###### Configure External Lifecycle Actions as below
    - External Action Bundle:  http://YourIP/gelb/gelb.zip
    - External Lifecycle Actions:
        Start:
            Script from bundle: service start
        Stop:
            Script from bundle: service stop
###### Step 3 : Configure deployment parameters as below

Deployement Parameters

| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| gelbProjectname | string | The project id where the service need to be deployed.| <samplename> |  |
| gelbLoadBalancerType |	List |	Type of Load Balancer. For more details on the type of load balancer to choose, check Google cloud documentation | TCP / HTTP / UDP | 
|gelbInstances | String | Comma separated instance names to be configured for the service. Ensure the configured health check path is  available and is responding in all the specified instances for the configured health check to pass
| gelbHealthCheck |	String |	The health check name to be configured for the service. | 


###### Step 4 : Save the service

##### Detailed steps for creating a service through UI

Step 1 : unzip  service import script zip file on any Linux System.

Step 2 : Navigate to the extracted directory. Invoke the script as below 

./serviceimport.sh

Step 3 : User will be prompted to input the following.

- The repository URL where service bundle is placed.
- Cloud Center Suite IP Address
- User name for for Cloud Center Suite login 
- password for Cloud Center Suite
- Tenant name
- logo file

Once Authenticated , User will presented with the status of service import on the command Line.   