## Azure DNS zones  


# Introduction
    Azure DNS is a hosting service for DNS domains that provides name resolution by using Microsoft Azure 
    infrastructure. By hosting your domains in Azure, you can manage your DNS records
    to your website or web application

Please refer the below link for more details.
For your reference : https://docs.microsoft.com/en-us/azure/dns/dns-overview

# Pre-Requisites
 CloudCenter
   - CloudCenter 5.x.x and above
   - Knowledge on how to use Workload Manager

Before you start with service import, Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

NOTE : You can skip the above step, if Docker Client is already installed and running in your machine.

- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

# Importing the service

- Step 1 : Download the service import utility file from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.

    wget command may not be installed. Need to execute "yum install wget -y" in case of centos7.

        Example:  
        wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
        
    After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

- Step 2 : Execute the script from Step 1 using the following command.

    sh ServiceImportMaster.sh
    Once the script is run, please follow the prompts to import the service or the corresponding application profile.

PLEASE NOTE : You be prompted with location of service bundle zip and/or application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.
     - Service Zip file under <service_path>/<your_bundle_name>
                
         Example : http://<Your_REPO_Server_IP>/<service_path>/Azure_dns_zones.zip 

     - Application Zip file under <app_path>/<your_package_name>
        
         Example: http://<Your_REPO_Server_IP>/<app_path>/petclinic.war
# Service Package Bundle
    The Package Service bundle consists of the following files:

Shell script:

   - service: Initiates the python script to start integration.

Python script:

- install_setup.py: The script will check all mandatory parameters available and installs necessary - 
- python packages also invokes external life cycle action.
- azure_dns_management.py: script that invokes the api for Azure functions like create record set DNS configuration .
- prerequiste_environments.py : Script will check required parameter for Azure DNS management
- util.py: utility file
- error_utils.py: A script that handles error functionalities
# External Lifecycle Actions as below
- External Action Bundle:  services/Azure_dns_zones.zip
- External Lifecycle Actions:

            Start:
			
                Script from bundle: service start
            Stop:
			
                Script from bundle: service stop
# Deployment Parameters:

| Parameter Name | Type | Mandotory | Description | Allowed Value | Default Value | 
| ---- |----| ----| ---- | ---- | ----|
| DomainName |	String | Yes|	Mention Existing Registered Domain Name in Azure,If DomainName is not registered Please create a DomainName in Azure App Service Eg : <SampleDomainName.com>|
|SubDomainName | Sting | Yes | Mention new  valid subdomain Eg : SubDomainName| | |
|IpAddress |String |No| Mention IpAddress of your Webapplication or Application Ip | | 
