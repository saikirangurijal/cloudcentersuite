#!/bin/sh

########## SCRIPT WHICH IS GOING TO BE Executed in REMOTE 

. /usr/local/osmosix/etc/userenv
ls -la /home/cliqruser

## COPY DOMAIN FOLDERS
cp /home/cliqruser/basicWLSDomain  /home/cliqruser/wls/oracle/product/fmw12/user_projects/domains/ -rf
## Read Listner Address Property in Admin Server's Node Manager Property file and Remove it. 
sed -i '/^ListenAddress/d' /home/cliqruser/wls/oracle/product/fmw12/user_projects/domains/basicWLSDomain/nodemanager/nodemanager.properties
## ADD ListenAddress Address Property in Node Manager property FILE FOR REMOTE MACHINE 1 .... REMOTE MACHINE ....N 	
echo "ListenAddress=$cliqrNodePrivateIp" >> /home/cliqruser/wls/oracle/product/fmw12/user_projects/domains/basicWLSDomain/nodemanager/nodemanager.properties
## CHANGE OWNER FROM CLIQRUSER TO weblogic 
chown -R cliqruser:cliqruser /home/cliqruser/wls/oracle/product/fmw12/user_projects/domains/basicWLSDomain -f 
chown -R cliqruser:cliqruser /home/cliqruser/wls/oracle/product/fmw12/user_projects/domains/basicWLSDomain/nodemanager/nodemanager.properties  -f 

# Start child nodes Node Manager
/bin/sh /home/cliqruser/wls/oracle/product/fmw12/user_projects/domains/basicWLSDomain/bin/startNodeManager.sh
	