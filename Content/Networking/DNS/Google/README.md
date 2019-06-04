# Google DNS
## Introduction

	Publish your domain names using Google's infrastructure for production-quality, high-volume DNS services

Please refer the below link for more details.
	For your reference : https://cloud.google.com/dns/docs/	

# Pre-Requisites
 CloudCenter
   - CloudCenter 5.x.x and above
   - Knowledge on how to use Workload Manager

Before you start with service import, Install Docker by following the steps provided here, on any linux based client machine.

NOTE : You can skip the above step, if Docker Client is already installed and running in your machine.

- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"
- Importing the service
- Step 1 : Download the service import utility file from here, and save the file on to your linux machine.

    wget command may not be installed. Need to execute "yum install wget -y" in case of centos7.

        Example:  wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
    After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

- Step 2 : Execute the script from Step 1 using the following command.

    sh ServiceImportMaster.sh
    Once the script is run, please follow the prompts to import the service or the corresponding application profile.

PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.
     - Service Zip file under <service_path>/<your_bundle_name>
                
         Example : http://<Your_REPO_Server_IP>/<service_path>/googledns.zip 

     - Application Zip file under <app_path>/<your_package_name>
        
         Example: http://<Your_REPO_Server_IP>/<app_path>/petclinic.war
# Service Package Bundle
    The Package Service bundle consists of the following files:
	
Shell script:

   - service: Initiates the python script to start integration.
   
Python Script :

- install_setup.py: The script will check all mandatory parameters available and installs necessary - python packages also invokes external life cycle action.
- google_dns_client.py: script that invokes the api for google dns functions like create record set DNS configuration.
- main.py : Script will invoke lifecycle actions
- util.py: utility file
- error_utils.py: A script that handles error functionalities

# External Lifecycle Actions as below
- External Action Bundle:  services/googledns.zip
- External Lifecycle Actions:

            Start:
			
                Script from bundle: service start
            Stop:
			
                Script from bundle: service stop
# Deployment Parameters:

| Parameter Name | Type | Mandotory | Description | Allowed Value | Default Value | 
| ---- |----| ----| ---- | ---- | ----|
| domainName |	String | Yes|	Mention Existing Registered Domain, Service Eg : <SampleDomainName.com>|
|subDomainName | Sting | Yes | Mention new  valid subdomain Eg : SubDomainName| | |
|ipAddress |String |Yes| Mention IpAddress of your Webapplication or Application Ip | | 