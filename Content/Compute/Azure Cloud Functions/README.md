# 1.Azure Cloud Functions
## Introduction

	Azure Functions lets you develop serverless applications on Microsoft Azure.
	Azure Functions is a solution for easily running small pieces of code, or "functions," in the cloud. 
	You can write just the code you need for the problem at hand, without worrying about a whole application 
	or the infrastructure to run it. 
	
	Functions can make development even more productive, and you can use your development language of choice,
	such as C#, Node.js, Java, or Python. 
	
	Please refer the below link for more details.
	For your reference : https://docs.microsoft.com/en-us/azure/azure-functions/
	
	## How it works:
    
       1.Once application deployed successfully user can access sample flask
	   application(which writes data into the MySQL).
	   
       2.When user writes an item into a table(users), A new stream record is written to 
	   reflect that a new item has been added to the table.
	   
       3.The new stream record triggers an Azure CloudFunction.
	   
       4.If the stream record indicates that a new item is added to table then azure web app will 
	   add two fields(username, email) to the existing item of the table.
	   
       5.User can view the details of his entry through sample flask application.	
	   
	   6.After your successful deployment, you can find the URL by clicking Get function URL in your function 
	   present under Function App in AzurePortal(https://portal.azure.com) to access your application.
		
		https://<"Function_Name">.azurewebsites.net/
	
# 2.Azure WebApp
## Introduction

	Azure App Service is a fully managed compute platform that is optimized for hosting websites 
	and web applications. 
	
	Azure App Service is an HTTP-based service for hosting web applications, REST APIs, 
	and mobile back ends. 
	
	You can develop in your favorite language, be it .NET, .NET Core, Java, Ruby, Node.js, PHP, or Python. 
	Applications run and scale with ease on both Windows and Linux-based environments.  
	
	Please refer the below link for more details.
	For your reference : https://docs.microsoft.com/en-us/azure/azure-functions/
	
## Before you start	Azure WebApp
  
   ## MySQL Import
1. Before importing the azurewebapp service, user must import azurewebapp service in workload manager 
	  because Azure Web app will be invoked on MySQL db table events (Any CRUD operation).

2. Refer Readme on how to import MySQL Service from [here](https://github.com/datacenter/cloudcentersuite/blob/master/Content/Databases/Relational%20Databases/MSSQL/README.md).
      
3. The Azure Web app service will create a azure web app with provided name in Microsoft Azure.

   ## Docker Install

1. Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"	
  

   ## How it works:
    
       1.Once application deployed successfully user can access sample flask
	   application(which writes data into the MySQL).
	   
       2.When user writes an item into a table(users), A new stream record is written to 
	   reflect that a new item has been added to the table.
	   
       3.The new stream record triggers an Azure CloudFunction.
	   
       4.If the stream record indicates that a new item is added to table then azure web app will 
	   add two fields(username, email) to the existing item of the table.
	   
       5.User can view the details of his entry through sample flask application.	
	   
	   6.After your successful deployment, you can find the URL by clicking Get function URL in your function 
	   present under Function App in AzurePortal(https://portal.azure.com) to access your application.
		
		https://<"Function_Name">.azurewebsites.net/
	

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
    - External Action Bundle:   http://YourIP/services/azurecloudfunction.zip
    - External Lifecycle Actions:
        Start:
            Script from bundle: **service start**
        Stop:
            Script from bundle: **service stop**

# Service Parameters:
| Parameter Name| Type	 | Mandatory |Description | 
| ------ | ------ | ------ | ------ 
| AppPackage | Path |	Yes |Path of the Deployment Package(.zip). | 


# Deployment Parameters(Azure Cloud Function):
| Parameter Name| Type	 | Mandatory |Description |  
| ------ | ------ | ------ | ------   
| app_name |	String | Yes | Name of the azure cloud function to be created. |
| runtime | List | Yes | Need to select required run time for the azure cloud functions. | 

# Deployment Parameters(Azure WebApp):
| Parameter Name| Type	 | Mandatory |Description |  
| ------ | ------ | ------ | ------   
| app_name |	String | Yes | Name of the azure web app to be created. |


