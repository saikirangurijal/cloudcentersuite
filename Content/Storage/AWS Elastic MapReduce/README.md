# AWS Elastic MapReduce
## Introduction
    Amazon EMR is the industry leading cloud-native big data platform, 
	allowing teams to process vast amounts of data quickly, and cost-effectively 
	at scale. 
	
	Using open source tools such as Apache Spark, Apache Hive, Apache HBase, 
	Apache Flink, and Presto, coupled with the dynamic scalability of Amazon EC2 
	and scalable storage of Amazon S3, EMR gives analytical teams the engines and 
	elasticity to run Petabyte-scale analysis for a fraction of the cost of 
	traditional on-premise clusters. 
	
	Developers and analysts can use Jupyter-based EMR Notebooks for iterative development, 
	collaboration, and access to data stored across AWS data products such as 
	Amazon S3, Amazon DynamoDB, and Amazon Redshift to reduce time to insight and 
	quickly operationalize analytics.

    
    Please refer the below link for more details.
	https://aws.amazon.com/emr/
	
## Pre-Requisites
#### CloudCenter
- CloudCenter 5.0.1 and above
- Knowledge on how to use Workload Manager 
	

#### Before you start
Before you start with service import, Install Docker by following the steps provided [here](https://github.com/datacenter/cloudcentersuite/raw/master/Content/dockerimages/Steps%20for%20Installation%20of%20Docker%20CE%20on%20CentOS7_V2.docx), on any linux based client machine.

**NOTE** : You can skip the above step, if Docker Client is already installed and running in your machine. 
- You can check , if docker is installed , by running "docker -v"
- You can check , if docker is running , by executing the command "systemctl status docker"

## Importing the service

Step 1 : Download the service import utility file  from [here](https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/Scripts/ServiceImportMaster.sh), and save the file on to your linux machine.
- wget command may not be installed. Need to execute "yum install wget -y" in case of centos7.

	    Example: 
      wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/ServiceImportMaster.sh
				
- After downloading ServiceImportMaster.sh, provide file permissions by executing "chmod 755 ServiceImportMaster.sh".

Step 2 : Execute the script from Step 1 using the following command.

        sh ServiceImportMaster.sh

Once the script is run, please follow the prompts to import the service or the corresponding application profile.

##### PLEASE NOTE : You be prompted with location of service bundle zip, application bundle zip on client machine. The files must be copied on to the repository before proceeding to deploy.

         - Service Zip file under <service_path>/<your_bundle_name>
                    
             Example : http://<Your_REPO_Server_IP>/<service_path>/awsemr.zip 


## Service Package Bundle

The Packer Service bundle consists of the following files:

Shell script:

service: Initiates the python script to start integration.

Python script :

createCluster.py : This Script will create the cluster with step execution or without step execution in aws elastic map reduce depends on given input while deployment.
 
 

# External Lifecycle Actions as below
    - External Action Bundle:  http://YourIP/services/awsemr.zip - Location where your external action bundle zip is found.
    - External Lifecycle Actions:
        Start:
            Script from bundle: service start
		
# Deployment Parameters:

| Parameter Name	| Type	 | Description | Allowed Value |Default Value |
| ------ | ------ | ------ |------ | ------ |
| AwsEc2KeyName |	string |	Keypair name in AWS Ec2 service from given region | 
| EMRClusterName|string  | Cluster Name To Create A Cluster In Elastic MapReduce | 
| S3ClusterLogPath |	String |	S3 location of log folder to store cluster logs | bucketname/folder name |
| NumberOfNodes | number | On how many nodes that hadoop can run in a cluster | 0 - 999999 | 2 |
| InstallApplications | list | Select which applicantion wants to  be installed  on hadoop cluster | Hive / Pig / spark |
| StepType | list | Type Of The Step To Exceute In The Cluster | Streaming Program / Hive Program / Pig Program / Spark Application / Custom JAR |
| StreamingTypeInputs | textarea | s3location of map function,reduce function,input file,new  folder name to store output results | bucketname/foldername/filename |
| HiveTypeInputs | textarea | s3location of hive script, folder name for input, folder name to store output result | bucketname/foldername/filename |
| PigTypeInputs | textarea | s3location of pig script, folder name for input, folder name to store output result | bucketname/foldername/filename |
| SparkDeployMode | list | Run your driver on a slave node (cluster mode) or on the master node as an external client (client mode) | Cluster / Client | Cluster |
| SparkSubmitOptions | string | Specify other options for spark-submit | 
| SparkApplicationLocation | string | S3 Path to a JAR with your application and dependencies if cluster mode otherwise client deploy mode only supports a local path | bucketname/spark.jar / localpath |
| CustomJarTypeJarlocation | string | JAR location maybe a path into S3 or a fully qualified java class in the classpath | s3://bucketname/custom.jar / fully qualified java class | s3:// |
| CustomJarTypeArguments | string | These are passed to the main function in the JAR. If the JAR does not specify a main class in its manifest file you can specify another class name as the first argument |




