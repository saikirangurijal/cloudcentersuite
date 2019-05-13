#!/bin/bash

PWD=`pwd`

##### STEP 1 : CHECK DOCKER INSTALLED ELSE EXIT #####
which docker

if [ $? -eq 0 ]
then
    docker --version | grep "Docker version"
    if [ $? -eq 0 ]
    then
        echo "The docker client is avilable..."
    else
        echo "There is no docker client available. Please install docker and run the script again."
	exit
    fi
else
    echo "There is no docker client available. Please install docker and run the script again." >&2
    exit
fi

##### STEP 2 : CHECK IF DOCKER IMAGE IS ALREADY AVAILABLE #####

if [ ! -d "$PWD/ccsworker" ]; then
	mkdir ccsworker
fi
cd ccsworker

if [[ "$(docker images -q ccs_service_import:v1 2> /dev/null)" != "" ]]; then
	  
	echo "Docker image available. skipping  install..."
	
else
 	echo "creating ccs service import:v1"
	echo "PWDD: $PWD"
	#if [ ! -d "$PWD/ccsworker" ]; then
	#	mkdir ccsworker
	#fi

	#cd ccsworker
	wget https://raw.githubusercontent.com/datacenter/cloudcentersuite/master/Content/dockerimages/Dockerfile -q -O Dockerfile
	docker build --no-cache -t ccs_service_import:v1 .
fi


##### STEP 3: COPY THE SERVICE IMPORT AND SERVICE LIBRARY BUNDLE on to ccsworker 


	wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Databases/GoogleSQL/WorkloadManager/googlesql_iu.zip -q -O googlesql_iu.zip
	echo "PWDeeee : $PWD"
	unzip -o googlesql_iu.zip -d $PWD

	wget https://github.com/datacenter/cloudcentersuite/raw/master/Content/Scripts/serviceimport.zip -q -O serviceimport.zip
	unzip -o serviceimport.zip -d $PWD

##### STEP 4: Run the Docker 

	docker run -v $PWD:/ccsworker -w /ccsworker -it  ccs_service_import:v1 /bin/bash
 
