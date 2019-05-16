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
        echo "The docker client is avilable..." >> $PWD/serviceimport.log
    else
        echo "There is no docker client available. Please install docker and run the script again." >> $PWD/serviceimport.log
	exit
    fi
else
    echo "There is no docker client available. Please install docker and run the script again." >&2 >> $PWD/serviceimport.log
    exit
fi

##### STEP 2 : CHECK IF DOCKER IMAGE IS ALREADY AVAILABLE #####

if [ ! -d "$PWD/ccsworker" ]; then
	mkdir ccsworker
fi
cd ccsworker

if [[ "$(docker images -q ccs_service_import:v1 2> /dev/null)" != "" ]]; then
	  
	echo "Docker image available. skipping  install..." >> $PWD/serviceimport.log
	
else
 	echo "Creating docker image ccs_service_import:v1 using Dockerfile..." 
	wget https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/dockerimages/Dockerfile -q -O Dockerfile
	docker build --no-cache -t ccs_service_import:v1 . >>$PWD/serviceimport.log 
	echo "Docker Image is created successfully..."
fi


##### STEP 3: COPY THE SERVICE IMPORT AND SERVICE LIBRARY BUNDLE on to ccsworker 

	echo " Downloading the files for service import..."
	wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip -q -O serviceimport.zip
	unzip -o serviceimport.zip -d $PWD
	
	wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/categoryList.py -q -O categoryList.py
	wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/ServiceList.json -q -O ServiceList.json
	echo " File downloading complete ..."
##### STEP 4: Run the Docker 
	echo "Initiating the docker run ..."
	docker run -v $PWD:/ccsworker -w /ccsworker -it  ccs_service_import:v1 /bin/bash
	echo "Invokes the Entrypoint script ..."
	echo "____________________________________________________________________________"
	echo "Please wait while the service import is in progress..." 
	echo "____________________________________________________________________________"
