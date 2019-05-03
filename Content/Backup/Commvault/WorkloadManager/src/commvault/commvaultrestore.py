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
        print (stderr)
    print (command + "upgrade pip successfully")

    command = 'pip install requests'
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return_code = process.returncode
    if return_code != 0:
        print ("Installation Failed " + command)
    else:
        print( stderr)
    print (command + "Installation successfully")

try:
    sourceClientName = os.getenv('sourceClient')
    destClientName = os.getenv('destinationClient')
    commCellId = os.getenv('commCellId')
    restoreType = os.getenv('restoreType')

    print("Restore Type",restoreType)

    if restoreType == "Database":
        appName = 'MYSQL'
        dbName = os.getenv('dbName')
        if dbName == '':
            dbName = '/'
        if dbName[0] != '/':
            dbName = '/'+dbName
        appId ="104"
    elif restoreType == "File System":
        appName = 'File System'
        path = os.getenv('path')
        if path == '':
            path = '/'
        if path[0] != '/':
            path = '/'+path
        appId = "29"
        inPlace = "0"
    else:
        print("Invalid Restore Type")
        sys.exit(0)


except Exception as e:
    print("Failed To Get Deployment Parameters ",e)
    sys.exit(0)

# Connect to Commvault using Python REST API

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



def clientParams(params,clientName):

    clientid_url = "http://<<server>>/webconsole/api/Client/byName(clientName="+"'"+clientName+"'" +")"

    clientid_url = clientid_url.replace("<<server>>", params['server'])

    #build headers with the received token
    headers = {'Authtoken': params['token']}

    try:
        clientdetailres = requests.get(clientid_url, headers=headers)

        clientres = clientdetailres.text
        clientres = ET.fromstring(clientres)

        clientEle = clientres.findall(".//clientEntity")
        client = clientEle[0].attrib['clientId']

        return client
    except Exception as e:
        print('No clientId Found For The Given ClientName ',clientName ,e)
        sys.exit(0)

def getClientDetails(clientName):
    return clientParams(loginCommvault(),clientName)


#Get SubClient Parameters

def subclientParams(params,clientDic):


    clientid_url = "http://<<server>>/webconsole/api/Subclient?clientId="+clientDic['clientId']

    clientid_url = clientid_url.replace("<<server>>", params['server'])

    #build header with the received token
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
                clientDic.update({'instanceName':name,'instanceId':instanceId,'subclientName':subclientName,'subclientId':subclientId,
                               'backupsetName':backupsetName,'backupsetId':backupsetId,'clientId':clientId,'clientName':clientName,
                               'displayName':displayName,'subclientGUID':subclientGUID,'commCellId':commCellId})
                break
        return clientDic
    except Exception as e:
        print('No Subclients Found For The Given ClientId',clientDic['clientId'],e)

def getSubClientList(clientDic):
    return subclientParams(loginCommvault(),clientDic)


#Browse Backup To Restore

def browseParams(params,clientDic):


    browsebackup_url = "http://<<server>>/webconsole/api/Subclient/"+clientDic['subclientId']+"/Browse"

    browsebackup_url = browsebackup_url.replace("<<server>>", params['server'])

    #build header with the received token
    headers = {'Authtoken': params['token']}

    try:

        backupResult = requests.get(browsebackup_url, headers=headers)
        backupRes = backupResult.text
        backupRes = ET.fromstring(backupRes)
        backupEle = backupRes.findall(".//advancedData")
        for ele in backupEle:
            backupJobId = ele.attrib['backupJobId']
            break
        return backupJobId
    except Exception as e:
        print('No Subclients Found For The Given ClientId',clientDic['clientId'],e)

def checkBackupExist(clientDic):
    return browseParams(loginCommvault(),clientDic)


#Create DbRestore

def dbRestoreParams(params,subData):

    db_restore_url = "http://<<server>>/webconsole/api/CreateTask"

    db_restore_url = db_restore_url.replace("<<server>>", params['server'])

    #build header with the received token
    headers = {'Authtoken': params['token']}


    db_restore_request_payload =  '<TMMsg_CreateTaskReq> \
                                       <taskInfo> \
                                          <task taskType="1" initiatedFrom="1" /> \
                                          <associations applicationId='+ "'"+appId+"'"+' clientName='+ "'"+subData[0]['clientName']+"'"+' backupsetId='+ "'"+subData[0]['backupsetId']+"'"+' instanceId='+ "'"+subData[0]['instanceId']+"'"+' clientId='+ "'"+subData[0]['clientId']+"'"+' backupsetName='+ "'"+subData[0]['backupsetName']+"'"+' instanceName='+ "'"+subData[0]['instanceName']+"'"+' _type_="6" appName='+ "'"+appName+"'"+'> \
                                             <timeZone> \
                                                <flags /> \
                                             </timeZone> \
                                             <flags /> \
                                             <subtask> \
                                                <flags /> \
                                             </subtask> \
                                             <client> \
                                                <flags /> \
                                             </client> \
                                             <owner> \
                                                <flags /> \
                                             </owner> \
                                          </associations> \
                                          <subTasks> \
                                             <subTask subTaskType="3" operationType="1001" /> \
                                             <options> \
                                                <restoreOptions> \
                                                   <browseOption commCellId='+ "'"+subData[0]['commCellId']+"'"+'> \
                                                      <timeRange /> \
                                                   </browseOption> \
                                                   <destination> \
                                                      <destClient clientId='+ "'"+subData[1]['clientId']+"'"+' clientName='+ "'"+subData[1]['clientName']+"'"+' /> \
                                                      <destinationInstance clientId='+ "'"+subData[1]['clientId']+"'"+' clientName='+ "'"+subData[1]['clientName']+"'"+' applicationId='+ "'"+appId+"'"+' appName='+ "'"+appName+"'"+' instanceId='+ "'"+subData[1]['instanceId']+"'"+' instanceName='+ "'"+subData[1]['instanceName']+"'"+' > \
                                                         <flags /> \
                                                      </destinationInstance> \
                                                   </destination> \
                                                   <mySqlRstOption pointofTime="0" instanceRestore="0" data="1" log="1" recurringRestore="0" logRestoreType="0" destinationFolder="" temporaryStagingLocation="/opt/commvault3/iDataAgent/jobResults" dataStagingLocation="" tableLevelRestore="0" isCloneRestore="0"> \
                                                      <fromTime time="0" /> \
                                                      <refTime time="0" /> \
                                                      <destinationServer id='+ "'"+subData[1]['instanceId']+"'"+' name='+ "'"+subData[1]['instanceName']+"'"+' /> \
                                                      <pointInTime time="0" /> \
                                                   </mySqlRstOption> \
                                                   <fileOption> \
                                                      <sourceItem val='+ "'"+dbName+"'"+' /> \
                                                   </fileOption> \
                                                   <commonOptions /> \
                                                </restoreOptions> \
                                             </options> \
                                          </subTasks> \
                                       </taskInfo> \
                                    </TMMsg_CreateTaskReq>'

    dic = {'db_restore_url':db_restore_url,'headers':headers,'db_restore_request_payload':db_restore_request_payload}
    return dic

def fileRestoreParams(params,subData):

    restore_url = "http://<<server>>/webconsole/api/retrieveToClient"

    restore_url = restore_url.replace("<<server>>", params['server'])

    destPath =  path + '\\CommRestoredFiles'

    restoreTask_Payload = '<DM2ContentIndexing_RetrieveToClientReq mode="2" serviceType="1">' \
                          '       <userInfo userGuid="4C1C8327-233F-46F5-910B-E873FBEBE494"/>' \
                          '       <header>' \
                          '           <srcContent clientId='+'"'+ subData[0]['clientId'] +'"'+' appTypeId='+'"'+ appId +'"'+' instanceId='+'"'+ subData[0]['instanceId'] +'"'+' backupSetId='+'"'+ subData[0]['backupSetId'] +'"'+' subclientId='+'"'+ subData[0]['subclientId'] +'"'+'/>' \
                          '           <destination clientId='+'"'+ subData[1]['clientId'] +'"'+' clientName='+'"'+ subData[1]['clientName'] +'"'+' inPlace='+'"'+ inPlace +'"'+'>' \
                          '               <destPath val='+'"'+ destPath +'"'+' />' \
                          '           </destination>' \
                          '           <filePaths val='+'"'+ path +'"'+'/>' \
                          '       </header><advanced restoreDataAndACL="1" restoreDeletedFiles="1"/>' \
                          '</DM2ContentIndexing_RetrieveToClientReq>'
    # build header with the received token
    headers = {'Authtoken': params['token']}

    dic = {'db_restore_url': restore_url, 'headers': headers, 'restoreTask_Payload': restoreTask_Payload}
    return dic


def checkRestore(dic):
    #Fire the request and print output
    r1 = requests.post(dic['db_restore_url'],data=dic['db_restore_request_payload'], headers=dic['headers'])
    resp = r1.content

    respRoot = ET.fromstring(resp)
    try:
        respEle = respRoot.findall(".//jobIds")
        jobId = respEle[0].attrib["val"]
        if jobId:
            print (appName+" Restore is Successfully")
            return {'restoreJobId':jobId}
    except:
        errorCode = respRoot.attrib["errorCode"]
        print (appName+" DB Restore Failed. ErrorCode:" + errorCode)
        sys.exit(0)

def createInstanceRestore(subclientData):

    if restoreType == "Database":
        return checkRestore(dbRestoreParams(loginCommvault(),subclientData))
    else:
        return checkRestore(fileRestoreParams(loginCommvault(),subclientData))

def getClientProps(clientName):

        clientId = getClientDetails(clientName)

        envDic = {'clientName': clientName, 'clientId': clientId}

        envDic = getSubClientList(envDic)

        return envDic

def db_Restore():

    try:
        global inPlace
        srcClient = getClientProps(sourceClientName)

        if checkBackupExist(srcClient):

            if destClientName == "" or destClientName == 'current-system':
                ClientName = os.getenv('cliqrNodeHostname')
                destClient = getClientProps(ClientName)
                clientList = [srcClient,destClient]
                return  createInstanceRestore(clientList)
            else:
                destClient = getClientProps(destClientName)
                clientList = [srcClient, destClient]
                return createInstanceRestore(clientList)
        else:
            print("No"+appName+" BackUp Found For ",sourceClientName)
            sys.exit(0)

    except Exception as e:
        print("Db Restore Processing Failed", e)


if __name__ == '__main__':
    print(db_Restore())


