import os
import requests
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def deletedbserver(AppDynamicsControllerHost,controlleruser, AppDynamicsAccountName,controllerpass,name):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    response = requests.get('https://%s/controller/rest/databases/collectors' % (AppDynamicsControllerHost),
                            headers=headers, verify=False,
                            auth=(controlleruser + "@" + AppDynamicsAccountName, controllerpass))
    if response.status_code == 200:
        print("Databse collector configured")
        ki = response.json()
        for data in ki:
            configdata = data['config']
            if configdata['name'] == name:
                print(configdata['id'])
                print(configdata['name'])
                response = requests.delete(
                    'https://%s/controller/rest/databases/collectors/' % (AppDynamicsControllerHost) + str(
                        configdata['id']), headers=headers,
                    verify=False, auth=(controlleruser + "@" + AppDynamicsAccountName, controllerpass))
                print(response.text)
    else:
        print(response.text)
        print(response.status_code)
try:
    AppdynamicsUsername = os.environ['AppdynamicsUsername']
    AppDynamicsControllerHost = os.environ['AppDynamicsControllerHost']
    AppDynamicsControllerPort = os.environ['AppDynamicsControllerPort']
    AppDynamicsAccountName = os.environ['AppDynamicsAccountName']
    AppDynamicsAccessKey = os.environ['AppDynamicsAccessKey']
    cliqrNodePublicIp = os.environ['cliqrNodePublicIp']
    type = os.environ['DbType']
    name = os.environ['DatabaseName']
    hostname = os.environ['cliqrNodePublicIp']
    username = os.environ['DatabaseUsername']
    controlleruser = os.environ['ControllerUsername']
    controllerpass = os.environ['ControllerPassword']
except Exception as e:
    print(e)
    print("Error while getting environment variables")
    sys.exit(127)

try:
    cliqrDatabaseType = os.environ['cliqrDatabaseType']
except:
    cliqrDatabaseType = ''

if cliqrDatabaseType:
    deletedbserver(AppDynamicsControllerHost, controlleruser, AppDynamicsAccountName, controllerpass, name)


