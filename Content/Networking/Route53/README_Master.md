# AWS Route 53
## Introduction

	Amazon Route 53 is a highly available and scalable Domain Name System (DNS) web service.
    Amazon Route 53 console to register a domain name and configure Route 53 to route internet to your website or web application

    Please refer the below link for more details.
	For your reference : https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/

## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager 

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.

	    Example: 
       wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.

##### PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <services_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/awsroute53.zip 
    
         - Application Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/petclinic.war

## Service Package Bundle
The Package Service bundle consists of the following files:

Shell script:
 - service: Initiates the python script to start integration.

Python script :
 - install_setup.py: The script will check all mandatory parameters available and installs necessary python packages also invokes external life cycle action.
 - amazon_route53_management.py: script that invokes the api for route 53 functions like create record set DNS configuration and healthcheck.
 - prerequiste_environments.py : Script will check required parameter for route 53 management
 - createRecordSet.json : input template json for route 53 management 
 - util.py: utility file
 - error_utils.py: A script that handles error functionalities

# External Lifecycle Actions as below
    - External Action Bundle:  services/awsroute53.zip
    - External Lifecycle Actions:
        Start:
            Script from bundle: service start
        Stop:
            Script from bundle: service stop

# Deployment Parameters:
| Parameter Name| Type	 | Mandatory |Description | Allowed Value |Default Value |
| ------ | ------ | ------ | ------ |------ | ------ |
| DomainName |	String | Yes | Mention Existing Registered Domain Name in AWS,If DomainName is not there , click[here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/blob/master/Networking/Route53domain/README.md) to Refer another service for Domain creation |  |   |
| subDomainName | String | Yes	| Mention Unique Sub Domain Name for accessing your application |  | |
| IpAddress | String |	Yes |IpAddress of your web application or your website (Option)| | |
| healthCheckName | String | Yes | Mention unique healthcheck name for creating healthcheck |  | |
| healthCheckport | String | Yes | healthcheck port number for your webapplication or website |  | |
| healthCheckpath | String | Yes | Healthcheck path for your application |  | |
