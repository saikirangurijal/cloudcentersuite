# Azure Cloud Functions
  ## Introduction
Azure Cloud Functions helps you develop and deploy serverless applications . The Serverless Framework is different 
than other application frameworks because it manages your code as well as your infrastructure and supports multiple 
languages (Node.js, Python and more).This can implemented by two ways.

1.Azure FunctionApp

2.Azure Web App


# 1.Azure FunctionApp

   ## Introduction
	Azure Functions is a solution for easily running small pieces of code, or "functions," in the cloud and 
	can use our development language of choices such as dotnet, node or Poweshell. 
	
	Please refer the below link for more details.
	For your reference : https://docs.microsoft.com/en-us/azure/azure-functions/
	
   ## How it works
       1. Import the service and applicaiton profile using Import service script. Refer 
	   section ## Importing the service.It creates an application profile Azure_Cloud_Functions.
       
       2. Deploy the function app using above profile and click on Access application to view static HTML page.
	   
	   3.After your successful deployment, you can find the access application link under Task logs 
	   to access your application.
		
		https://<"Function_Name">.azurewebsites.net/api
	
# 2.Azure WebApp

   ## Introduction
	Azure Web App Service is an HTTP-based service for hosting web applications and use our development 
	languages like dotnet, ruby and python. 
	
	Please refer the below link for more details.
	For your reference : https://docs.microsoft.com/en-us/azure/app-service/
	
   ## How it works
    
       1. Import the service and applicaiton profile using Import service script. Refer 
	   section ## Importing the service.It creates an application profile Azure_Web_App.
      	   
       2.Deploy the Web app using above profile and click on Access application access sample 
	   flask application(which writes data into the MySQL).
	   
       3. Data is written to table When user triggers the application with the inputs .
	   
       4.User can view the details of his entry in search feature through sample flask application.	
	   
	   5.After your successful deployment, you can find the URL under Task logs to access your webapplication.
		
		https://<"Wep_App_Name">.azurewebsites.net/
	

   ## Docker Install

1. Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"	
 	

## Pre-Requisites
#### CloudCenter
- CloudCenter 5.x.x and above.
- Knowledge on how to use Workload Manager. 
- Deployment Package(appPackage)-Azure cloud function package in your apps repository.
 

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to execute "yum install wget -y" in case of centos7.

	    Example: 
      wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.

##### PLEASE NOTE : You be prompted with location of service bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/azurecloudfunctions.zip
			 
          - Application Bundle under <app_path>/<your_package_name>
        
                Example(Azure WebApp) : http://<Your_REPO_Server_IP>/<app_path>/azure_webapp_mysql_sample_app.zip
          
                Example(Azure FunctionApp) : http://<Your_REPO_Server_IP>/<app_path>/node-app.zip


## Service Package Bundle

The Packer Service bundle consists of the following files:

Shell script:
 - service: Initiates the python script to start integration.

Python script :
 - azure_cloud_function.py: script that invokes the azure-cli commands for creating azure cloud functions and 
    creates the azure cloud function with provided deployment package.
 - azure_webapp.py : script that invokes the azure-cli commands for creating azure web application 
 - main.py - calling functions based on operations like login,deploy
 - webapp_main.py - calling functions based on operations like login,createwebapp
 - util.py: utility file
 - error_messages.json : Json file contains error messages.
 - error_utils.py: The script that handles error functionality.
  

## External Lifecycle Actions
    - External Action Bundle:   http://YourIP/services/azurecloudfunctions.zip
    - External Lifecycle Actions:
        Start:
            Script from bundle: service start
        Stop:
            Script from bundle: service stop

## Service Parameters:
| Parameter Name| Type	 | Mandatory |Description | 
| ------ | ------ | ------ | ------ 
| AppPackage | Path |	Yes |Path of the Deployment Package(.zip). | 


## Deployment Parameters(Azure FunctionApp):
| Parameter Name| Type	 | Mandatory |Description |  
| ------ | ------ | ------ | ------   
| app_name |	String | Yes | Name of the azure cloud function to be created. |
| runtime | List | Yes | Need to select required run time for the azure cloud functions. | 

## Deployment Parameters(Azure WebApp):
| Parameter Name| Type	 | Mandatory |Description |  
| ------ | ------ | ------ | ------   
| app_name |	String | Yes | Name of the azure web app to be created. |


