# Commvault File System/MySQL DB Backup Operations
# for Linux client through REST APIs
#!/usr/bin/env python

import os
import sys
from subprocess import Popen, PIPE
import xml.etree.ElementTree as ET
import base64

try:
    import requests
except:
    command = 'pip install --upgrade pip'
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return_code = process.returncode
    if return_code != 0:
        print ("upgrade pip failed " + command)
    else:
        print( stderr )
        print ( command + "upgrade pip successful" )

    command = 'pip install requests'
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return_code = process.returncode
    if return_code != 0:
        print ( "Installation Failed " + command)
    else:
        print(stderr )
        print( command + "Installation successful" )

# Set Global Variables from User Environment
try:
    clientName = os.getenv('cliqrNodeHostname')
    commCellId = os.getenv('commCellId')
    backupType = os.getenv('backupType')
    storagePolicy = os.getenv('storagePolicy')
    commserveName = os.getenv('commserveName')
    storagePolicyId = ''

    if backupType == "Database":
        appName = 'MYSQL'
        appId = "104"
        dbName = os.getenv('dbName')
        if dbName == "":
           dbName = "/"

        dbpathlist = dbName.split(',')
        for pathpart in dbpathlist:
            if pathpart[0] != '/':
                pathpart = '/' + pathpart

    elif backupType == "File System":
        appName = 'File System'
        appId = "29"
        path = os.getenv('path')

        if path == "":
           path = "/"
        pathlist =  path.split(',')

        for pathpart in pathlist:
           if pathpart[0] != '/':
               pathpart = '/' + pathpart

           if pathpart[-1] == '/' and pathpart != '/':
               pathpart = pathpart[0:-1]

        appId = "29"

    else:
        print("Invalid Backup Type")
        sys.exit(0)

except Exception as e:
    print("Failed To Get Deployment Parameters ", e)
    sys.exit(0)


# Connect/Login To Commvault

def loginCommvault():
    try:
        server = os.environ['commvaultServerIp']
        user = os.environ['commvaultUserName']
        pwd = os.environ['commvaultPassword']

    except:
        print("No Login Parameters")
        sys.exit(0)

    service = 'http://<<server>>/webconsole/api/login'
    service = service.replace("<<server>>", server)

    loginReq = '<DM2ContentIndexing_CheckCredentialReq username="<<username>>" password="<<password>>" />'
    if user is None:
        print("Username is required")
        sys.exit(0)
    else:
        loginReq = loginReq.replace("<<username>>", user)

    if pwd is None:
        loginReq = loginReq.replace("<<password>>", "")
    else:
        loginReq = loginReq.replace("<<password>>", base64.b64encode(pwd))

    loginDic = {'userName': user, 'password': pwd, 'loginReq': loginReq, 'service': service, 'server': server}

    # Login request built. Send the request now:
    r = requests.post(loginDic['service'], data=loginDic['loginReq'])

    # Check response code and check if the response has an attribute "token" set
    if r.status_code == 200:
        root = ET.fromstring(r.text)
        if 'token' in root.attrib:
            token = root.attrib['token']
            loginDic.update({'token': token})
            return loginDic
        else:
            print("Login Failed")
            sys.exit(0)
    else:
        print('Error logging into Commvault ', r.status_code)
        sys.exit(0)

# Get Client Parameters

def clientParams(params, clientName):
    clientid_url = "http://<<server>>/webconsole/api/Client/byName(clientName=" + "'" + clientName + "'" + ")"

    clientid_url = clientid_url.replace("<<server>>", params['server'])

    # build headers with the received token
    headers = {'Authtoken': params['token']}

    try:
        clientdetailres = requests.get(clientid_url, headers=headers)

        clientres = clientdetailres.text
        clientres = ET.fromstring(clientres)

        clientEle = clientres.findall(".//clientEntity")
        client = clientEle[0].attrib['clientId']

        return client
    except Exception as e:
        print('No clientId Found For The Given ClientName ', clientName, e)
        sys.exit(0)


def getClientDetails(clientName):
    return clientParams(loginCommvault(), clientName)

# Get Commcell ID using Commcell Name(if not available from user)

def commcellParams(params):
    commcellid_url = "http://<<server>>/webconsole/api/CommServ"

    commcellid_url = commcellid_url.replace("<<server>>", params['server'])


    # build headers with the received token
    headers = {'Authtoken': params['token']}

    commcellidres = requests.get(commcellid_url, headers=headers)
    commcellres = commcellidres.text
    commcellres = ET.fromstring(commcellres)

    try:
        commcellEle = commcellres.findall(".//commcell")
        commcellname = commcellEle[0].attrib['commCellName']
        if commcellname == commserveName:
           commCellId = commcellEle[0].attrib['commCellId']
           return commCellId
    except Exception as e:
          print('No Commcell ID Found For This Commserver ', commserveName, e)
          sys.exit(0)


def getcommcellId():
    return commcellParams(loginCommvault())

# Get Storage Policy ID using Storage Policy Name

def storagePolicyParams(params):

    storagepolicyid_url = "http://<<server>>/webconsole/api/V2/StoragePolicy"

    storagepolicyid_url = storagepolicyid_url.replace("<<server>>", params['server'])

    # build headers with the received token
    headers = {'Authtoken': params['token']}

    policyidres = requests.get(storagepolicyid_url, headers=headers)
    policyres = policyidres.text
    policyres = ET.fromstring(policyres)

    try:
        policyEle = policyres.findall(".//storagePolicy")
        for elm in policyEle:
            storPolicyName = elm.attrib['storagePolicyName']
            if storPolicyName == storagePolicy:
                storagePolicyid = policyEle[0].attrib['storagePolicyId']
                return storagePolicyid
    except Exception as e:
        print('No Storage Policy ID Found For Storage policy Name', storagePolicy, e)
        sys.exit(0)


def getstorPolicyId():
    return storagePolicyParams(loginCommvault())

#Setting Storage Policy ID
storagePolicyId = getstorPolicyId()


# Get SubClient Parameters

def subclientParams(params, clientDic):
    clientid_url = "http://<<server>>/webconsole/api/Subclient?clientId=" + clientDic[
        'clientId'] + "&applicationId=" + appId

    clientid_url = clientid_url.replace("<<server>>", params['server'])

    # build header with the received token
    headers = {'Authtoken': params['token']}

    try:

        clientdetailres = requests.get(clientid_url, headers=headers)
        clientres = clientdetailres.text
        clientres = ET.fromstring(clientres)
        clientEle = clientres.findall(".//subClientEntity")
        for ele in clientEle:
            subclientName = ele.attrib['subclientName']
            if subclientName == 'default':
                name = ele.attrib['instanceName']
                subclientId = ele.attrib['subclientId']
                backupsetId = ele.attrib['backupsetId']
                backupsetName = ele.attrib['backupsetName']
                instanceId = ele.attrib['instanceId']
                clientId = ele.attrib['clientId']
                clientName = ele.attrib['clientName']
                displayName = ele.attrib['displayName']
                subclientGUID = ele.attrib['subclientGUID']
                clientDic.update({'instanceName': name, 'instanceId': instanceId, 'subclientName': subclientName,
                                  'subclientId': subclientId,
                                  'backupsetName': backupsetName, 'backupsetId': backupsetId, 'clientId': clientId,
                                  'clientName': clientName,
                                  'displayName': displayName, 'subclientGUID': subclientGUID, 'commCellId': commCellId})
                break
        return clientDic
    except Exception as e:
        print('No Subclients Found For The Given ClientId', clientDic['clientId'], e)


def getSubClientList(clientDic):
    return subclientParams(loginCommvault(), clientDic)


# Create BackupSet

def backupParams(params, subData):
    backup_url = "http://<<server>>/webconsole/api/CreateTask"

    backup_url = backup_url.replace("<<server>>", params['server'])

    # build header with the received token
    headers = {'Authtoken': params['token']}

    if appId == "29":
        backupOpts = '<backupOpts backupLevel="1"></backupOpts>'
    else:
        backupOpts = '<backupOpts backupLevel="FULL" doNotTruncateLog="false" isSpHasInLineCopy="false" runIncrementalBackup="true" runSILOBackup="false" sybaseSkipFullafterLogBkp="false" truncateLogsOnSource="false"> \
                                                    <dataOpt createNewIndex="false" enableIndexCheckPointing="false" enforceTransactionLogUsage="false" followMountPoints="true" skipCatalogPhaseForSnapBackup="false" skipConsistencyCheck="false" spaceReclamation="false" verifySynthFull="false" /> \
                                                    <dataPathOpt> \
                                                        <drive driveId="" /> \
                                                        <drivePool drivePoolId="" /> \
                                                        <library libraryId="1" /> \
                                                        <mediaAgent mediaAgentId="2" /> \
                                                        <spareGroup spareMediaGroupId="0" /> \
                                                    </dataPathOpt> \
                                                    <mediaOpt allowOtherSchedulesToUseMediaSet="true" markMediaFullOnSuccess="false" numberofDays="30" reserveResourcesBeforeScan="false" \
                                                    retentionJobType="2" startNewMedia="true" /> \
                                                </backupOpts>'

    backup_request_payload = '<TMMsg_CreateTaskReq> \
                                    <taskInfo> \
                                         <associations _type_="SUBCLIENT_ENTITY" subclientId=' + "'" + subData[
                                            'subclientId'] + "'" + ' subclientName=' + "'" + subData['subclientName'] + "'" + ' backupsetId=' + "'" + \
                                            subData['backupsetId'] + "'" + ' backupsetName=' + "'" + subData[
                                            'backupsetName'] + "'" + ' instanceId=' + "'" + subData[
                                            'instanceId'] + "'" + ' instanceName=' + "'" + subData[
                                            'instanceName'] + "'" + ' applicationId=' + "'" + appId + "'" + ' appName=' + "'" + appName + "'" + ' clientId=' + "'" + \
                                            subData['clientId'] + "'" + ' clientName=' + "'" + subData[
                                            'clientName'] + "'" + ' displayName=' + "'" + subData[
                                            'displayName'] + "'" + ' subclientGUID=' + "'" + subData[
                                            'subclientGUID'] + "'" + ' commCellId=' + "'" + subData['commCellId'] + "'" + ' /> \
                                         <subTasks> \
                                            <options> \ ' + backupOpts + '\
                                                 <commonOpts jobDescription=""> \
                                                    <jobRetryOpts enableNumberOfRetries="false" killRunningJobWhenTotalRunningTimeExpires="false" numberOfRetries="0"> \
                                                        <runningTime enableTotalRunningTime="false" totalRunningTime="3600" /> \
                                                     </jobRetryOpts> \
                                                    <startUpOpts priority="166" startInSuspendedState="false" useDefaultPriority="true" /> \
                                                 </commonOpts> \
                                            </options> \
                                            <subTask operationType="2" subTaskType="2" /> \
                                         </subTasks> \
                                         <task initiatedFrom="COMMANDLINE" policyType="DATA_PROTECTION" sequenceNumber="10" taskId="0" taskType="IMMEDIATE"> \
                                            <taskFlags disabled="false"/> \
                                         </task> \
                                    </taskInfo> \
                                </TMMsg_CreateTaskReq>'
    dic = {'backup_url': backup_url, 'headers': headers, 'backup_request_payload': backup_request_payload}
    return dic


def checkBackup(dic):
    # Fire the request and print output
    try:
        r1 = requests.post(dic['backup_url'], data=dic['backup_request_payload'], headers=dic['headers'])
        resp = r1.content
        respRoot = ET.fromstring(resp)
        respEle = respRoot.findall(".//jobIds")
        jobId = respEle[0].attrib["val"]
        if jobId:
            print(appName + " BackUp is Successful")
            return {'backupJobId':jobId}
    except Exception as e:
        errorCode = respRoot.attrib["errorCode"]
        print( appName + " BackUp Failed. ErrorCode:", errorCode, e)
        sys.exit(0)

# Create Instance (DB Backup)

def createInstanceBackUp(subData):
    return checkBackup(backupParams(loginCommvault(), subData))


def updateInstanceBackupParams(params, subData):
    instance_url = "http://<<server>>/webconsole/api/instance/" + subData['instanceId']

    instance_url = instance_url.replace("<<server>>", params['server'])

    # build header with the received token
    headers = {'Authtoken': params['token']}

    instance_request_payload = ''
    instance_request_payload = ''
    with open('/opt/remoteFiles/appPackage/commvault-agent/updateinstance.xml', 'r') as file:
        instance_request_payload = file.read()
    instance_request_payload = instance_request_payload.replace("%clientid%", subData['clientId'])
    instance_request_payload = instance_request_payload.replace("%appid%", appId)
    instance_request_payload = instance_request_payload.replace("%instanceid%", subData['instanceId'])
    instance_request_payload = instance_request_payload.replace("%dbpassword%", params['password'])
    instance_request_payload = instance_request_payload.replace("%clientname%", subData['clientName'])
    instance_request_payload = instance_request_payload.replace("%instancename%", subData['instanceName'])
    instance_request_payload = instance_request_payload.replace("%dbuser%", params['userName'])
    instance_request_payload = instance_request_payload.replace("%appName%", appName)
    instance_request_payload = instance_request_payload.replace("%storagePolicy%", storagePolicy)
    instance_request_payload = instance_request_payload.replace("%storagePolicyId%", storagePolicyId)

    dic = {'instance_url': instance_url, 'headers': headers, 'instance_request_payload': instance_request_payload}
    return dic

# Update Instance Details

def updateInstanceBackup(dic):
    # Fire the request and print output
    try:
        r1 = requests.post(dic['instance_url'], data=dic['instance_request_payload'], headers=dic['headers'])
        resp = r1.content
        respRoot = ET.fromstring(resp)
        respEle = respRoot.findall(".//response")
        if r1.status_code == 200:
            jobId = respEle[0].attrib["errorCode"]
            if jobId:
                print(appName + " Instance is updated Successfully")
    except Exception as e:
        errorCode = respRoot.attrib["errorCode"]
        print (appName + " BackUp Failed. ErrorCode:", errorCode,e)
        sys.exit(0)


def updateInstance(subData):
    updateInstanceBackup(updateInstanceBackupParams(loginCommvault(), subData))


# Update Db Content to be Backedup

def updateDbAndFileParams(params, subData):

    updateSubclient_url = "http://<<server>>/webconsole/api/Subclient/"+subData['subclientId']

    updateSubclient_url = updateSubclient_url.replace("<<server>>", params['server'])

    # build header with the received token
    headers = {'Authtoken': params['token']}
    conpath = ""

    if appId == "29":
        for pathpart in pathlist:
            conpath = conpath + '<path>'+pathpart+'</path>'
    else:
        for pathpart in dbpathlist:
            conpath = conpath +' <mySQLContent databaseName='+ "'" + pathpart  + "'" +' databaseSize="0" creationTime="0" discoverFlag="0" engineName="UNKNOWN"/>'

    updateSubclientPayload = '<App_UpdateSubClientPropertiesRequest>\
                            <subClientProperties>\
                                <dfsSubclientProp/>\
                                <cassandraProps/>\
                                <splunkProps/>\
                                <subClientEntity subclientId='+ "'" + subData['subclientId']  + "'" +' subclientName='+ "'" + subData['subclientName']  + "'" +' backupsetId='+ "'" + subData['backupsetId']  + "'" +' backupsetName='+ "'" + subData['backupsetName']  + "'" +' instanceId='+ "'" + subData['instanceId']  + "'" +' instanceName='+ "'" + subData['instanceName']  + "'" +' applicationId='+ "'" + appId  + "'" +' appName='+ "'" + appName + "'" +' clientId='+ "'" + subData['clientId']  + "'" +' clientName='+ "'" + subData['clientName']  + "'" +' displayName='+ "'" + subData['displayName']  + "'" +' subclientGUID='+ "'" + subData['subclientGUID']  + "'" +' _type_="7"/>\
                                <analyticsSubclientProp/>\
    	                        <contentOperationType>OVERWRITE</contentOperationType>\
                                <content>'+\
        	                       conpath \
                                +'</content>\
                                <proxyClient/>\
                                <planEntity/>\
                                <region/>\
                            </subClientProperties>\
                        </App_UpdateSubClientPropertiesRequest>'

    dic = {'backup_url': updateSubclient_url, 'headers': headers, 'backup_request_payload': updateSubclientPayload}
    return dic


def checkDbAndFileUpdate(dic):
    # Fire the request and print output

    r1 = requests.post(dic['backup_url'], data=dic['backup_request_payload'], headers=dic['headers'])
    resp = r1.content
    respRoot = ET.fromstring(resp)

    try:
        if r1.status_code == 200:
            respEle = respRoot.findall(".//response")
            errorCode = respEle[0].attrib["errorCode"]
            if errorCode == "0":
                print(appName + "Content Updated Successfully")
        else:
            errorMessage = respRoot.attrib["errorMessage"]
            print (appName + " Content Updation Failed. ErrorMessage:", errorMessage)
            sys.exit(0)

    except Exception as e:
        print (appName + " Content Updation Failed. Error:", e)
        sys.exit(0)


def updateDbAndFileContent(subData):
    checkDbAndFileUpdate(updateDbAndFileParams(loginCommvault(), subData))

#Perform Backup

def dbAndFileBackup():
    try:
        #commCellId = getcommcellId()
        clientId = getClientDetails(clientName)

        envDic = {'clientName': clientName, 'clientId': clientId}

        envDic = getSubClientList(envDic)

        if backupType == "Database":
            updateInstance(envDic)
            if dbName != '/':
                updateDbAndFileContent(envDic)
        else:
            if path != '/':
                updateDbAndFileContent(envDic)

        return createInstanceBackUp(envDic)

    except Exception as e:
        print(appName," Backup Processing Failed", e)


if __name__ == '__main__':
    print(dbAndFileBackup())
