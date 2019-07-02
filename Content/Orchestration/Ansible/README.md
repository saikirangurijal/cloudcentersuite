# Ansible

## Introduction

    The Workload Manager platform supports integration to various Configuration Management tools as VM with agent 
    type of service.

    This document provides information on integrating Ansible with Cisco Workload Manager.

    Ansible is an open source automation platform that offers configuration management, application deployment, 
    along with infrastructure orchestration.

    Please refer the below link for more details.

    https://www.ansible.com/overview/how-ansible-works
## Pre-Requisites

#### CloudCenter
- CloudCenter 5.x.x and above
- Knowledge on how to use Workload Manager
- Supported OS : CentOS 7, Ubuntu 16.04 (xenial)
- Supported Clouds : Google, AWS

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker".

Upload your ansible Bundle zip file ( containing Ansible Roles & Playbook) into a file repository.

**NOTE**: During creation of Ansible Bundle zip file, Avoid creating a folder with the contents while zipping. 

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to execute "yum install wget -y" in case of centos7, and "apt install wget" in case of Ubuntu16.04.

	    Example: 
       wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.

##### PLEASE NOTE : 
You will be prompted with location of service bundle zip on linux machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/ansible.zip
             
Place your uploaded Ansible bundle zip file under the following path in the same repository.

         - Ansible Bundle Zip file under <app_path>/<your_package_name>
            
             Example: http://<Your_REPO_Server_IP>/<app_path>/my_ansible_bundle.zip
   
## Service Package Bundle

The Package Service bundle consists of the following file:

Shell script:

- service: Installs Ansible and Executes Ansible Roles.

## Agent Lifecycle Actions 

Agent Action Bundle:  
 - http://YourIP/services/ansible.zip - Location where your agent action bundle zip (service bundle zip file) is found.
 
Agent Lifecycle Actions: 
 - Start: Script from bundle: **service install**
 - Stop: Script from bundle: **service configure** 

#  Service Parameters:

| Parameter Name | Type | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| ansibleBundle | Path | Zipped file Path of ansible playbook and ansible Roles | User Defined Value |  |
| ansibleRole| String | One or more names of Ansible Roles to be executed separated by commas |

**NOTE** : 
- Parameter 'ansibleBundle' can be either the HTTP path URL or repository URL from which the ansible bundle will be downloaded.
