# Agent Installation on Client
#!/usr/bin/env python

import os
import sys
from subprocess import check_call
import xml.etree.ElementTree as ET
import base64

try:
    import requests
except:
    check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    s = check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
    print(s)
    import requests

try:
     instanceName = os.getenv('instanceName')
     clientName   = os.getenv('cliqrNodeHostname')
     commCellId   = os.getenv('commCellId')
     commserveName = os.getenv('commserveName')
except:
    print("No Deployment Parameters to Install Agent")
    sys.exit(0)
# Connect to Commvault using Python REST API

def loginParam():

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

    dic={'userName':user,'password':pwd,'loginReq':loginReq,'service':service,'server':server}

    return dic

import requests
def getToken(loginDic):

    # Login request built. Send the request now:
    r = requests.post(loginDic['service'], data=loginDic['loginReq'])

    # Check response code and check if the response has an attribute "token" set
    if r.status_code == 200:
        root = ET.fromstring(r.text)
        if 'token' in root.attrib:
            token = root.attrib['token']
            print("Login Successful")
            loginDic.update({'token': token})
            return loginDic
        else:
            print("Login Failed")
            sys.exit(0)
    else:
        print(r.status_code)
        print('Error logging into Commvault ',r.status_code)
        sys.exit(0)

def loginCommvault():
    dic = loginParam()
    return getToken(dic)


def clientParams(params,clientName):

    clientid_url = "http://<<server>>/webconsole/api/Client/byName(clientName="+"'"+clientName+"'" +")"

    clientid_url = clientid_url.replace("<<server>>", params['server'])

    #build headers with the received token
    headers = {'Authtoken': params['token']}

    clientdetailres = requests.get(clientid_url, headers=headers)
    clientres = clientdetailres.text
    clientres = ET.fromstring(clientres)

    try:
        clientEle = clientres.findall(".//clientEntity")
        client = clientEle[0].attrib['clientId']
        print("Got Client detail successfully")
        return client
    except Exception as e:
        print('No clientId Found For The Given ClientName ',clientName ,e)
        sys.exit(0)

def getClientDetails(clientName):
    return clientParams(loginCommvault(),clientName)

def installAgentParams(params,envDic):

    try:
        headers = {'Authtoken': params['token']}
        agent_install_url = "http://<<server>>/webconsole/api/CreateTask"
        agent_install_url = agent_install_url.replace("<<server>>", params['server'])
        agent_install_req_body=''
        with open('/opt/remoteFiles/appPackage/commvault-agent/agent.xml', 'r') as file:
            agent_install_req_body = file.read()
        agent_install_req_body = agent_install_req_body.replace("%cliqrNodeHostname%", envDic['clientName'])
        agent_install_req_body = agent_install_req_body.replace("%clientId%", envDic['clientId'])
        agent_install_req_body = agent_install_req_body.replace("%commserveName%", commserveName)
        agent_install_req_body = agent_install_req_body.replace("%commvaultUserName%", params['userName'])
        agent_install_req_body = agent_install_req_body.replace("%commCellId%", commCellId)

        r1 = requests.post(agent_install_url,data=agent_install_req_body, headers=headers)
        resp = r1.content
        print("Agent Installation Response",resp)

        if r1.status_code == 200:
          resp = r1.content
          respRoot = ET.fromstring(resp)
          respEle = respRoot.findall(".//jobIds")
          jobId = respEle[0].attrib["val"]
          if jobId:
            print ("Additional Agent Installation Completed Successfully")
            return jobId
          else:
            print ("Additional Agent Installation Failed as there is no Job ID  ")
            return 0
        else:
          respRoot = ET.fromstring(resp)
          print (" Additional Agent Installation Failed as HTTP Status is not 200 ", r1.errorMessage)
          return 0

    except Exception as e:
        print ("Additional Agent Installation got Failed.Exception"  ,e )
        sys.exit(0)


def installAdditionalAgents():
    envDic = {}
    try:
        clientId = getClientDetails(clientName)
        envDic = {'instanceName': instanceName, 'clientName': clientName, 'clientId': clientId}
        print ("Env Dictionay" , envDic)
        print ("ClientId  ", clientId)
        print ("Client Name ", clientName )
        jobId = installAgentParams(loginCommvault(),envDic)
        print ("Job Id" , jobId)
    except Exception as e:
        print("Additional Agent Installation got Failed ", e)
        sys.exit(0)

if __name__ == '__main__':
    installAdditionalAgents()
