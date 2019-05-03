#!/bin/bash

exec > >(tee -a /usr/local/osmosix/logs/service.log) 2>&1

source /usr/local/osmosix/etc/userenv
OSSVC_HOME=/usr/local/osmosix/service
SVCNAME="Commvault Agent"

# Utility Shell Scripts
. /usr/local/osmosix/etc/.osmosix.sh
. /usr/local/osmosix/etc/userenv
. $OSSVC_HOME/utils/cfgutil.sh
. $OSSVC_HOME/utils/nosqlutil.sh
. $OSSVC_HOME/utils/install_util.sh
source /usr/local/osmosix/utils/agent_util.sh

commserveName=$commserveName
commvaultServerIp=$commvaultServerIp
commvaultUserName=$commvaultUserName
export commvaultPassword="$commvaultPassword"
export instanceName=Instance001
authcodevalue=
#export commvaultEncPassword="$(echo $commvaultPassword | base64 )"
export backupType=$backupType
export restoreType=$restoreType


commvaultEncPassword=$(python /opt/remoteFiles/appPackage/commvault/encrypt.py)
export $commvaultEncPassword
echo $commvaultEncPassword

echo "export instanceName=$instanceName" >> /usr/local/osmosix/etc/userenv
echo "export commvaultPassword=$commvaultPassword" >> /usr/local/osmosix/etc/userenv
echo "export commvaultEncPassword=$commvaultEncPassword" >> /usr/local/osmosix/etc/userenv
echo "export backupType=\"$backupType\"" >> /usr/local/osmosix/etc/userenv
echo "export destinationClient=\"$destinationClient\"" >> /usr/local/osmosix/etc/userenv

function ccmLog
{
  agentSendLogMessage "$*"
}

function empty
{
    local var="$1"

    # Return true if:
    # 1.    var is a null string ("" as empty string)
    # 2.    a non set variable is passed
    # 3.    a declared variable or array but without a value is passed
    # 4.    an empty array is passed
    if test -z "$var"
    then
        [[ $( echo "1" ) ]]
        return

    # Return true if var is zero (0 as an integer or "0" as a string)
    elif [ "$var" == 0 2> /dev/null ]
    then
        [[ $( echo "1" ) ]]
        return

    # Return true if var is 0.0 (0 as a float)
    elif [ "$var" == 0.0 2> /dev/null ]
    then
        [[ $( echo "1" ) ]]
        return
    fi

    [[ $( echo "" ) ]]
}




#Kill All Commvault related  Client Process
function removeCommVaultClientProcess
{
    processStr="$1"
    PID=`ps -eaf | grep $processStr | grep -v grep | awk '{print $2}'`
    if [[ "" !=  "$PID" ]]; then
        echo "Shutting down $PID for the Process $processStr"
		log "[INSTALL] Started - Clean up  existing Installation of  $SVCNAME"
        kill -9 $PID
	else 
        echo "There is no such process Exist  $processStr"	
		log "[INSTALL] There is no existing Installation of  $SVCNAME"
 	    log "[INSTALL] Skip - Clean up - $SVCNAME"

    fi
    installWget
    installUnzip
    #yum -y install wget
    #yum -y install unzip
}

#Clean up all previous CommVault Installation 
function uninstall_commvault
{
   removeCommVaultClientProcess  cvlaunchd
   removeCommVaultClientProcess  cvfwd
   removeCommVaultClientProcess  ClMgrS
   removeCommVaultClientProcess  cvd
   
   echo "Removing output file... if any from tmp folder"
   log "[INSTALL] Clean up /tmp/output.xml  for $SVCNAME"
   rm -rf /tmp/output.xml
   echo "Cleaning Registry if any entries exists"
   log "[INSTALL] Clean up Registry Entry  for $SVCNAME"
   rm -rf /etc/CommVaultRegistry/
   echo "Cleaning Log files  if any log file  exists for Commvault"
   log "[INSTALL] Clean up Log files entry of $SVCNAME"
   rm -rf /var/log/commvaul*
   echo "Cleaning up previous Installation directory if exists"
   log "[INSTALL] Clean up previous Installation directory of $SVCNAME"
   rm -rf /opt/commvaul*
   echo "Clean up done for CommVault"
   log "[INSTALL] Completed - Clean up - $SVCNAME"
   rm -rf /tmp/output.xml 
   echo "" >> /tmp/output.xml
   chmod -R 755 /tmp/output.xml 
}

#Prepare Installation Answer File for Installation
function prepareAnswerFile
{

   log "[INSTALL] Preparing Answer File before start Installation of  $SVCNAME"
   replaceToken default-final.xml "%commserveIP%" $commvaultServerIp
   replaceToken default-final.xml "%commserveUserName%" $commvaultUserName
   replaceToken default-final.xml "%commservePassword%" $commvaultPassword
   #replaceToken default-final.xml "%commvaultEncPassword%" $commvaultEncPassword
   replaceToken default-final.xml "%commserveName%" $commserveName
   replaceToken default-final.xml "%clientname%" $cliqrNodeHostname
   replaceToken default-final.xml "%clientHostName%" $cliqrNodePublicIp
   export COMMVAULT_CLIENT_ID=$cliqrNodeHostname
   replaceToken default-final.xml "%instance_name%" $instanceName
   replaceToken default-final.xml "%authcodevalue%" $authcodevalue
   log "[INSTALL] Completed - Preparing Answer file for Installation of  $SVCNAME"
}

#Download and Install Commvault Client and Agents 
function install_commvault
{

    log "[INSTALL] Started Installation of  $SVCNAME"
    cd  /opt/remoteFiles/appPackage/
    wget $commvaultCustomPackageURL 

    if [ $(ls -la  /opt/remoteFiles/appPackage/linux_pkg.tar | grep "linux_pkg" | wc -l) -ge 1 ]
    then
        echo "Moved Installation Bundle to commvault directory"
        log "[INSTALL] Installation Tar file exists   $SVCNAME"
        cp /opt/remoteFiles/appPackage/linux_pkg.tar  /opt/remoteFiles/appPackage/commvault/linux_pkg.tar
    else 	
        log "[INSTALL] Installation Tar file does not exist   $SVCNAME"
    fi 



    if [ $(ls -la  /opt/remoteFiles/appPackage/commvault/linux_pkg.tar | grep "linux_pkg" | wc -l) -ge 1 ]
    then
       echo "CommVault Custom Installation Package is avaialable."
	   chmod -R 755 /opt/remoteFiles/appPackage/commvault/linux_pkg.tar
	   cd /opt/remoteFiles/appPackage/commvault
       tar -xvf linux_pkg.tar
       prepareAnswerFile
	   mv ./pkg/default.xml  ./pkg/default-backup.xml
	   cp default-final.xml  ./pkg/default.xml 
	   
	   
        if empty "${authcodevalue}"
        then
           echo "Auth Code value is Empty "
           log "[INSTALL] Installation CMD Executed with out Auth code -    $SVCNAME"
		   ./pkg/silent_install -p ./pkg/default.xml
           log "[INSTALL] Installation Completed for   $SVCNAME"
        else
          echo "Auth Code value is Present "
          log "[INSTALL] Installation CMD Executed with Auth code - ${authcodevalue}   $SVCNAME"
		  ./pkg/silent_install -p ./pkg/default.xml -authcode $authcodevalue
          log "[INSTALL] Installation Completed for   $SVCNAME"
        fi
	   
	    
	else 
	   echo "There is no CommVault Installation Package is present " 
       log "[INSTALL] Installation Tar file does not exist.. Exit from Installation   $SVCNAME"
       log "[INSTALL] Installation Failed for   $SVCNAME"

    fi

}

function is_commvault_installed
{

    if [ $(cat /var/log/commvault/Log_Files/install.log | grep "Install completed successfully" | wc -l) -ge 1 ]
    then
	    log "[INSTALL]  $SVCNAME Client Installed Successfully  "
       echo "CommVault Client Installed Successfully"
	   
			if [ $(ls -la /opt/commvault/Base/SIMCallWrapper | grep "SIMCallWrapper" | wc -l) -ge 1 ]
			then
			    echo "Installed Succesfully. Base Directory exists"
                if empty "${authcodevalue}"
                then
                    echo "Auth Code value is Empty "
/opt/commvault/Base/SIMCallWrapper -OpType 1000 -instance $instanceName  -user $commvaultUserName -password $commvaultPassword  -CSName $commserveName -CSHost  $commvaultServerIp  -ClientName $cliqrNodeHostname  -ClientHostName $cliqrNodePublicIp    -overwriteClientInfo -output /tmp/output.xml -restartServices
                else
                    echo "Auth Code value is Present "
/opt/commvault/Base/SIMCallWrapper -OpType 1000 -instance $instanceName  -user $commvaultUserName -password $commvaultPassword   -CSName $commserveName -CSHost  $commvaultServerIp  -ClientName $cliqrNodeHostname  -ClientHostName $cliqrNodePublicIp    -overwriteClientInfo -authcode $authcodevalue -output /tmp/output.xml -restartServices
                fi
	            log "[INSTALL]  $SVCNAME Client is registred Successfully"
				echo "CommVault Client Registration is done Successfully"
				
			else 
	            log "[INSTALL]  $SVCNAME Client is not registred Successfully"
				echo "CommVault Client Registration got Failed" 
			fi
	else 
	   echo "CommVault Client Installation is not done properly" 
	   log "[INSTALL]  $SVCNAME Client is not installed Successfully  "
    fi


}


function install_client
{
source /usr/local/osmosix/etc/userenv
ccmLog "[Commvault] Client Installation STARTED"
uninstall_commvault
install_commvault
sleep 2m
ccmLog "[Commvault] Client Installation Completed"
is_commvault_installed
sleep 4m
source /usr/local/osmosix/etc/userenv
ccmLog "[Commvault] Agent Installation STARTED"
log "[INSTALL]  $SVCNAME MYSQL Agent is going to be installed "
python /opt/remoteFiles/appPackage/commvault/install_agent.py
log "[INSTALL]  $SVCNAME MYSQL Agent is installed Successfully"
ccmLog "[Commvault] Agent Installation Completed"
log "[INSTALL]  Backup Actions would be executed based on User Input in few seconds......"
sleep 6m

}

### This block  will be removed once all test is done 
#mysql < /opt/remoteFiles/appPackage/commvault/db_init.sql
### This block  will be removed once all test is done 


    if empty "${restoreType}"
    then
			if empty "${backupType}"
			then
				echo "Backuptype is empty"
			else
                ccmLog "[Commvault] Backup with Type : $backupType invoked "
				install_client
			fi
    else
        ccmLog "[Commvault] Restore with Type : $restoreType invoked"
		if empty "${destinationClient}"
		then
			echo "Destination Client is Empty "
			ccmLog "[Commvault] Destination Client is Empty. Source Client is ${sourceClient}  "
			echo "export destinationClient=\"$cliqrNodeHostname\"" >> /usr/local/osmosix/etc/userenv
			ccmLog "[Commvault] Client and Agent to be Installed in Current VM - $cliqrNodeHostname "
			install_client
		else
			if test "$destinationClient" = "current-system"
			then
				echo "Destination Client is ${destinationClient} "
				ccmLog "[Commvault] Restore - Destination Client is Current-System. Source Client is ${sourceClient}  "
				echo "export destinationClient=\"$cliqrNodeHostname\"" >> /usr/local/osmosix/etc/userenv
				ccmLog "[Commvault] Restore - Client and Agent to be Installed in Current VM - $cliqrNodeHostname "
				install_client
			else
				ccmLog "[Commvault] Restore - Destination Client variable has existing client  value - ${destinationClient}"
				ccmLog "[Commvault] Restore - Skip Client and Agent Installation..."
			fi		
		fi		
		
    fi
	  




