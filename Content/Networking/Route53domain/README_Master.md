# AWS Route53Domain
## Introduction

	Amazon Route 53 is a highly available and scalable Domain Name System (DNS) web service.
    Amazon Route 53 console to register a domain name and configure Route 53 to route with unique domain name.

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
- wget command may not be installed. Need to add "yum install wget -y" in case of centos7.

	    Example: 
      wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.


##### PLEASE NOTE : You will be prompted with location of service bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

             - Service Bundle under <service_path>/<your_bundle_name>
                    
                    Example : http://<Your_REPO_Server_IP>/<service_path>/awsroute53domain.zip


## Service Package Bundle
The Package Service bundle consists of the following files:

Shell script:
 - service: Initiates the python script to start integration.

Python script :
 - install_setup.py: This script will check all mandatory parameters available and installs necessary python packages also invokes external life cycle action.
 - amazon_domain_creation.py: This script will invoke the api for route53 functions, will check domain availability and create domain.
 - prerequiste_environments.py : This Script will check required parameter for route53 management.
 - domaincreation.json : input template json for route53 domain creation.
 - util.py: utility file.
 - error_utils.py: The script will handle error functionality.

# External Lifecycle Actions as below
External Action Bundle:  services/awsroute53.zip

External Lifecycle Actions:
        Start:
            Script from bundle: **service start**

# Deployment Parameters:
| Parameter Name| Type	 | Mandatory |Description | Allowed Value |Default Value |
| ------ | ------ | ------ | ------ |------ | ------ |
| DomainName |	String | Yes | Mention Unique Domain Name for creating domain in AWS  |  |   |
| FirstName | String | Yes	| Mention First Name |  | |
| LastName | String |	Yes | Mention Last Name | | |
| ContactType | String | Yes | Mention Contact type of Person | <PERSON','COMPANY','ASSOCIATION','PUBLIC_BODY','RESELLER'> | |
| Organization | String | Yes | Mention Organization Name |  | |
| AddressLine1 | String | Yes | Mention first line of address  |  | |
|AddressLine2| String | Yes | Mention second line of address  |  | |
|City|String | Yes | Mention city name  |  | |
|PhoneNumber|String | Yes | Mention Phonenumber in format of <+01>.<123456789>  |  | |
|StateCode| String | Yes | Mention statecode in length of 2 char   | <TN,BG,AP,KL etc,.> | |
|CountryCode| String | Yes | Mention Country code in length of 2 char  |<IN,US,UK,AS,ML,SA etc,.>  | |
|zipcode| String | Yes | Mention Zip code of city  |  | |
|Email| String | Yes | Mention Valid Email Address   |  | |