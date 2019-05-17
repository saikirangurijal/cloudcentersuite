# Google Cloud SQL

## Introduction

    The Workload Manager platform supports integration to various Database layers 
    as an external service.

    This document provides information on Google Cloud SQL integration with Cisco
    Workload Manager by creating an external service.

    Google Cloud SQL platform gives you the ability to manage the database.

    Please refer the below link for more details.

    https://cloud.google.com/sql/docs/
## Pre-Requisites

#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://wwwin-github.cisco.com/CloudCenterSuite/Content-Factory/raw/master/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

## Download the Files

Step 1 : Copy the contents of service import script file from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.

	    Example: 
        wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, a docker image tagged as "ccs_service_import:v1" will be built, if it is not already available.

Step 3 : User will be prompted to enter the following inputs.

	Enter IP Address for Cloud Center Suite: XXX.XXX.XXX.XXX

	Enter Cloud Center Suite Email Address : YourEmail@XXX.com

	Enter the password: ***********

	Enter the Tenant ID  : YourTenantID

Step 4 : User will be prompted to select the Service Category. Select the number against the category else select 0 to exit.

     - Select the Service Category ID from the list (press 0 to exit):
     1	Databases
     2	Compute
	 3	Networking

Step 5 : User will be prompted to select the service under category that was selected in Step 4. Select the number against the service that you wish to import else select 0 to exit.

     - Select the service ID  from the list (press 0 to exit):
     1	GoogleSQL
     2	Lambda
	 3	Route 53
	 
Step 6 : User will be prompted to select the file repository in which you wish to place the Service Bundle and application bundle zip files. 

     - Select the corresponding Repository ID and Hit Enter.
     1  content-repo
     2  sample-repo
     
 
Step 7 : User will be prompted to select the option for importing the combination of service and/or app profile.
 
    - Select the corresponding ID and Hit Enter
    1 Import Service Only
    2 Import Application Profile Only
    3 Import both Service & Application Profile
    
If service and/or app profile import is successful, You will be presented with a message **"<Service Name> Service imported successfully. Imported Application Profile Successfully"**.

##### PLEASE NOTE : User will be prompted with location of service bundle zip and application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under services/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/services/googlesql.zip 
    
         - Application Zip file under apps/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/apps/googlesql-petclinic-app.zip
   
## Service Package Bundle

The Package Service bundle consists of the following files:

Shell script:

- service: Initiates the python script to start integration.

Python script :

- install_setup.py: The script will installs necessary python packages also invokes external life cycle action.

- google_sql.py : The script will invoke the creation and deletion service based on user selection type (MYSQL/POSTGRESQL) using google management client.

- google_management_client.py : The script will invoke the main method of google cloud sql.

- common.py: The script contains common functionality which is required for other script files.

- util.py: utility file

- error_messages.json : Json file contails error messages.

- error_utils.py: The script that handles error functionality

## External Lifecycle Actions 

External Action Bundle:  
 - http://YourIP/services/googlesql.zip - Location where your external action bundle zip (service bundle zip file) is found.
 
External Lifecycle Actions: 
 - Start: Script from bundle: **service start**
 - Stop: Script from bundle: **service stop** 

#  Deployment Parameters:

| Parameter Name | Type | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| geSqlType | List | Type of Sql. For more details on the type of sql to choose, check Google cloud documentation | MYSQL, POSTGRESQL | MYSQL| 
| geInstanceName | String | Instance names to be configured for the service. Ensure the instance name is  not available in cloud and can't use the same instance name even though deleted in cloud until 2 months.|


#  Service Parameters:

| Parameter Name | Type | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| geDbUserName | String | Database username to be configured for the service. | User Defined Value | petclinic |
| geDbPassword| Password | Database password to be configured for the service. |
| geDbName | String | Database name to be configured for the service.| User Defined Value | petclinic |
| geDbHost | String | Database host to be configured for the service.| % | %



