# Commvault Restore Python file Invocation
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





ccmLog " [RESTORE] task is going to be excuted in few minutes"
jobId=$(python /opt/remoteFiles/appPackage/commvault-agent/commvaultrestore.py)


if empty "${jobId}"
then
   ccmLog "$restoreType [RESTORE] task is Failed. Please refer service.log for detail info."
else
    if [ $(echo $jobId | grep "restoreJobId" | wc -l) -ge 1 ]
    then
        ccmLog "$restoreType [RESTORE] task is started successfully.... Restore Job details :$jobId "
        log "[RESTORE] - $restoreType  task is started successfully.... Job Id :$jobId "
    else 	
        ccmLog "$restoreType [RESTORE] task is Failed. ${jobId}, Please refer service.log for detail info "
        log "[RESTORE] Failed "
    fi 
fi


