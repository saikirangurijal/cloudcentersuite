#!/bin/bash

PWD=`pwd`

##### STEP 1 : CHECK DOCKER INSTALLED ELSE EXIT #####
echo "________________________________________________________________________"
echo " This script will create a docker image using Dockerfile , creates the "
echo " container and import the services on to workload manager."
echo "________________________________________________________________________"
which docker

if [ $? -eq 0 ]
then
    docker --version | grep "Docker version"
    if [ $? -eq 0 ]
    then
        echo "The docker client is avilable..." > /dev/null 2>&1
    else
        echo "There is no docker client available. Please install docker and run the script again." 
	exit
    fi
else
    echo "There is no docker client available. Please install docker and run the script again." 
    exit
fi

##### STEP 2 : CHECK IF DOCKER IMAGE IS ALREADY AVAILABLE #####

if [ ! -d "$PWD/ccsworker" ]; then
	mkdir ccsworker
fi
cd ccsworker

if [[ "$(docker images -q ccs_service_import:v1 2> /dev/null)" != "" ]]; then
	  
	echo "Docker image available. skipping  install..." > /dev/null 2>&1
	#docker stop $(docker container ps -a --filter status=exited | grep ccs_service_import:v1 | awk '{ print $1 }')
	#docker rm $(docker container ps -a --filter status=exited | grep ccs_service_import:v1 | awk '{ print $1 }')
	if [[ "$(docker container ps -a --filter status=exited | grep ccs_service_import:v1 2> /dev/null)" != "" ]]; then

        	docker stop $(docker container ps -a --filter status=exited | grep ccs_service_import:v1 | awk '{ print $1 }')
       		docker rm $(docker container ps -a --filter status=exited | grep ccs_service_import:v1 | awk '{ print $1 }')
	else

        	echo "there is no containers in exit status" > /dev/null 2>&1
	fi
else
 	echo "Creating docker image ccs_service_import:v1 using Dockerfile..." 
	wget https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/dockerimages/Dockerfile -q -O Dockerfile
	docker build --no-cache -t ccs_service_import:v1 . >>$PWD/serviceimport.log 
	echo "Docker Image is created successfully..."
fi


##### STEP 3: COPY THE SERVICE IMPORT AND SERVICE LIBRARY BUNDLE on to ccsworker 

	echo "Downloading the files for service import..." >>$PWD/serviceimport.log 
	wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport_master.zip -q -O serviceimport_master.zip
	unzip -o serviceimport_master.zip -d $PWD > /dev/null 2>&1
	
	#wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/categoryList.py -q -O categoryList.py
	wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/ServiceList.json -q -O ServiceList.json
	echo "File downloading complete ..." >>$PWD/serviceimport.log 

##### STEP 4: Run the Docker 
	echo "Initiating the docker run ..."
	echo "Invoking entrypoint script ..."
        echo "____________________________________________________________________________"
        echo "Please wait while the service import is in progress..."
        echo "____________________________________________________________________________"

	docker run -v $PWD:/ccsworker -w /ccsworker -it  ccs_service_import:v1 /bin/bash
	
