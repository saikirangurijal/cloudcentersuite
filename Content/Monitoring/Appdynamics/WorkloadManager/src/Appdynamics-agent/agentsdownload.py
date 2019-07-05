import requests, sys, json, os, signal
from zipfile import ZipFile
import subprocess, shutil
import xml.etree.ElementTree as ET

#Get access token to download pacakage
def GetToken(AppdynamicsUsername,AppdynamicsPassword):
    data = r'{"username": "%s", "password": "%s" , "scopes": ["download"]}'%(AppdynamicsUsername,AppdynamicsPassword)
    response = requests.post('https://identity.msrv.saas.appdynamics.com/v2.0/oauth/token', data=data)
    if response.status_code in [200]:
        tok_dict = json.loads(response.text)
        print(tok_dict)
        access_token = tok_dict["access_token"]
        return access_token
    else:
        print("Please check your credentials")
        sys.exit(127)

#installing dbagent
def dbagent(access_token,AppDynamicsControllerHost, AppDynamicsControllerPort,AppDynamicsAccountName,AppDynamicsAccessKey):
    headers = {"Authorization": "Bearer %s" % (access_token)}
    url = 'https://download.appdynamics.com/download/prox/download-file/db/4.5.4.885/dbagent-4.5.4.885.zip' #Download link for dbagaent
    response = requests.get(url,
                            headers=headers)
    if response.status_code in [200]:
        print("File downloaded")
        with open("dbagent.zip", "wb") as code:
            code.write(response.content)
    else:
        sys.exit(127)
    size = os.path.getsize("dbagent.zip") >> 20
    if size > 60:
        print("File downloaded")
    else:
        print("Please check your credentials")
    try:
        os.mkdir("/opt/dbagent")
        with ZipFile("dbagent.zip", 'r') as zipObj:
            zipObj.extractall('/opt/dbagent')
    except Exception as e:
        print(e)
        sys.exit(127)
    subprocess.call(['chmod', '755', '-R ', r'/opt/dbagent'])

    datafile = "/opt/dbagent/conf/controller-info.xml"
    with open(datafile, "r") as f:
        newText = f.read()
        newText = newText.replace("<controller-host></controller-host>",
                                  "<controller-host>%s</controller-host>"%(AppDynamicsControllerHost))
        newText = newText.replace("<controller-port></controller-port>", "<controller-port>%s</controller-port>"%(AppDynamicsControllerPort))
        newText = newText.replace("<controller-ssl-enabled>false</controller-ssl-enabled>",
                                  "<controller-ssl-enabled>true</controller-ssl-enabled>")
        newText = newText.replace("<use-simple-hostname></use-simple-hostname>",
                                  "<use-simple-hostname>false</use-simple-hostname>")
        newText = newText.replace("<node-name></node-name>", "<node-name>%s</node-name>")
        newText = newText.replace("<enable-orchestration></enable-orchestration>",
                                  "<enable-orchestration>false</enable-orchestration>")
        newText = newText.replace("<use-ssl-client-auth></use-ssl-client-auth>",
                                  "<use-ssl-client-auth>false</use-ssl-client-auth>")
        newText = newText.replace("<account-name></account-name>",
                                  "<account-name>%s</account-name>"%(AppDynamicsAccountName))
        newText = newText.replace("<account-access-key></account-access-key>",
                                  "<account-access-key>%s</account-access-key>"%(AppDynamicsAccessKey))
        newText = newText.replace("<force-agent-registration></force-agent-registration>",
                                  "<force-agent-registration>false</force-agent-registration>")
        newText = newText.replace("<auto-naming></auto-naming>", "<auto-naming>true</auto-naming>")
    with open(datafile, "w") as f:
        f.write(newText)
    os.chdir("/opt/dbagent")
    command1 = subprocess.Popen(["yum", "install", "-y", " java"], stdout=subprocess.PIPE)
    out, err = command1.communicate()
    print(out)
    os.system("nohup /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el7_6.x86_64/jre/bin/java  -Xmx1536m -jar /opt/dbagent/db-agent.jar > /dev/null 2>&1 &")
    print("DB AGENT STARTED")
#installing javaserveragent
def javaserveragent(access_token,ApplicationName,ApplicationNode,AppDynamicsControllerHost, AppDynamicsControllerPort,AppDynamicsAccountName,AppDynamicsAccessKey,cliqrNodePublicIp):
    headers = {"Authorization": "Bearer %s" % (access_token)}
    url = 'https://download.appdynamics.com/download/prox/download-file/sun-jvm/4.4.3.23530/AppServerAgent-4.4.3.23530.zip'
    response = requests.get(url,
                            headers=headers)
    if response.status_code in [200]:
        print("File downloaded")
        with open("javaagent.zip", "wb") as code:
            code.write(response.content)
    else:
        sys.exit(127)
    size = os.path.getsize("javaagent.zip") >> 20

    if size > 15:
        print("File downloaded")
    else:
        print("Please check your credentials")
        sys.exit(127)
    try:
        os.mkdir("/opt/javaagent")

    except Exception as e:
        print(e)
        sys.exit(127)
    with ZipFile("javaagent.zip", 'r') as zipObj:
        zipObj.extractall('/opt/javaagent')
    subprocess.call(['chmod', '755', '-R ', r'/opt/javaagent'])
    datafile = "/opt/javaagent/conf/controller-info.xml"
    with open(datafile, "r") as f:
        newText = f.read()
        newText = newText.replace("<controller-host></controller-host>",
                                  "<controller-host>%s</controller-host>"%(AppDynamicsControllerHost))
        newText = newText.replace("<controller-port></controller-port>", "<controller-port>%s</controller-port>"%(AppDynamicsControllerPort))
        newText = newText.replace("<controller-ssl-enabled></controller-ssl-enabled>",
                                  "<controller-ssl-enabled>true</controller-ssl-enabled>")
        newText = newText.replace("<use-simple-hostname></use-simple-hostname>",
                                  "<use-simple-hostname>false</use-simple-hostname>")
        newText = newText.replace("<node-name></node-name>", "<node-name>%s:80</node-name>"%(cliqrNodePublicIp))
        newText = newText.replace("<enable-orchestration></enable-orchestration>",
                                  "<enable-orchestration>false</enable-orchestration>")
        newText = newText.replace("<use-ssl-client-auth></use-ssl-client-auth>",
                                  "<use-ssl-client-auth>false</use-ssl-client-auth>")
        newText = newText.replace("<account-name></account-name>",
                                  "<account-name>%s</account-name>"%(AppDynamicsAccountName))
        newText = newText.replace("<account-access-key></account-access-key>",
                                  "<account-access-key>%s</account-access-key>"%(AppDynamicsAccessKey))
        newText = newText.replace("<force-agent-registration></force-agent-registration>",
                                  "<force-agent-registration>false</force-agent-registration>")
        newText = newText.replace("<auto-naming></auto-naming>", "<auto-naming>true</auto-naming>")
        newText = newText.replace("<application-name></application-name>", "<application-name>%s</application-name>"%(ApplicationName))
        newText = newText.replace("<tier-name></tier-name>", "<tier-name>%s</tier-name>"%(ApplicationNode))
    with open(datafile, "w") as f:
        f.write(newText)
    for root, dirs, files in os.walk("/usr"):
        for file in files:
            if file.endswith("catalina.sh"):
                filecatlina = os.path.join(root, file)
    replace = '# resolve links - $0 may be a softlink'
    addon = 'export CATALINA_OPTS="$CATALINA_OPTS -javaagent:/opt/javaagent/javaagent.jar"'
    with open(filecatlina) as f:
        newText = f.read().replace(replace, addon)
    with open(filecatlina, "w") as f:
        f.write(newText)
    os.popen("export JAVA_HOME=/usr/lib/jvm/java-8-sun")
    command1 = subprocess.Popen(["sh", filecatlina, "start"], stdout=subprocess.PIPE)
    out, err = command1.communicate()
    print(out)
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    #    command1 = subprocess.Popen(["./service", "start"], stdout=subprocess.PIPE)
    #    out, err = command1.communicate()
    #    print(out)
    #    for line in out.splitlines():
    #       if 'java' in line:
    #          pid = int(line.split(None, 1)[0])
    #         print(pid)
    #         os.kill(pid, signal.SIGKILL)
    os.chdir(r"/usr/local/cliqr/service/tomcat7")
    command1 = subprocess.Popen(["./service", "restart"], stdout=subprocess.PIPE)
    out, err = command1.communicate()
    print(out)
    command1 = subprocess.Popen(["./service", "restart"], stdout=subprocess.PIPE)
    out, err = command1.communicate()
    print(out)
    command1 = subprocess.Popen(["./service", "restart"], stdout=subprocess.PIPE)
    out, err = command1.communicate()
    print(out)

#installing machineagent
def machineagent(access_token,AppDynamicsControllerHost,AppDynamicsControllerPort,AppDynamicsAccountName,AppDynamicsAccessKey,cliqrNodePublicIp):
    headers = {"Authorization": "Bearer %s" % (access_token)}
    os.popen("export JAVA_HOME=/usr/lib/jvm/java-8-sun")
    url = 'https://download.appdynamics.com/download/prox/download-file/machine-bundle/4.4.3.1214/machineagent-bundle-64bit-linux-4.4.3.1214.zip'
    response = requests.get(url,
                            headers=headers)
    if response.status_code in [200]:
        print("File downloaded")
        with open("machineagent.zip", "wb") as code:
            code.write(response.content)
    else:
        sys.exit(127)
    size = os.path.getsize("machineagent.zip") >> 20
    if size > 60:
        print("File downloaded")
    else:
        print("Please check your credentials")
        sys.exit(127)
    try:
        os.mkdir("/opt/machineagent")

    except Exception as e:
        print(e)
        sys.exit(127)
    with ZipFile("machineagent.zip", 'r') as zipObj:
        zipObj.extractall('/opt/machineagent')
    cerfile = r"/opt/remoteFiles/appPackage/appdynamics.cer"
    destcer = r"/opt/machineagent/conf/appdynamics.cer"
    shutil.copy(cerfile, destcer)
    datafile = r"/opt/machineagent/conf/controller-info.xml"
    with open(datafile, "r") as f:
        newText = f.read()

        newText = newText.replace("<controller-host></controller-host>",
                                  "<controller-host>%s</controller-host>"%(AppDynamicsControllerHost))
        newText = newText.replace("<controller-port></controller-port>", "<controller-port>%s</controller-port>"%(AppDynamicsControllerPort))
        newText = newText.replace("<controller-ssl-enabled></controller-ssl-enabled>",
                                  "<controller-ssl-enabled>true</controller-ssl-enabled>")
        newText = newText.replace("<account-name></account-name>",
                                  "<account-name>%s</account-name>"%(AppDynamicsAccountName))
        newText = newText.replace("<account-access-key></account-access-key>",
                                  "<account-access-key>%s</account-access-key>"%(AppDynamicsAccessKey))
        newText = newText.replace("<controller-ssl-enabled>false</controller-ssl-enabled>",
                                  "<controller-ssl-enabled>true</controller-ssl-enabled>")
        newText = newText.replace("<machine-path></machine-path>",
                                  "<machine-path>/opt/machineagent/conf/appdynamics.cer</machine-path>")

    with open(datafile, "w") as f:
        f.write(newText)
    machineagentfile=r'/opt/machineagent/bin/machine-agent'
    with open(machineagentfile, "r") as f:
        newText = f.read()
        newText = newText.replace('exec "$JAVA" $JAVA_OPTS "$LOG4J_CONFIG" $props -jar "$MACHINE_AGENT_JAR_PATH"',
                                  'mkdir -p `dirname "$STARTUP_OUT"`\n        exec nohup "$JAVA" $JAVA_OPTS "$LOG4J_CONFIG" $props -jar "$MACHINE_AGENT_JAR_PATH" <&- >>"$STARTUP_OUT" 2>&1 &')
    with open(machineagentfile, "w") as f:
        f.write(newText)
    try:
        os.chdir("/opt/machineagent/bin")
        os.popen("chmod 755 -R /opt/machineagent")
        print(os.popen("ls").read())

        p = subprocess.Popen(['./machine-agent'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = p.communicate()
        print(out)
    except Exception as e:
        print(e)
        sys.exit(127)

#installing webserver agent
def webserveragent(access_token,ApplicationName,ApplicationNode,AppDynamicsControllerHost, AppDynamicsControllerPort,AppDynamicsAccountName,AppDynamicsAccessKey,cliqrNodePublicIp):
    headers = {"Authorization": "Bearer %s" % (access_token)}
    os.popen("export JAVA_HOME=/usr/lib/jvm/java-8-sun")
    url = r'https://download.appdynamics.com/download/prox/download-file/webserver-sdk/4.4.0.37433/appdynamics-sdk-native-nativeWebServer-64bit-linux-4.4.0.37433.tar.gz'
    response = requests.get(url,
                            headers=headers)
    if response.status_code in [200]:
        print("File downloaded")
        with open("webserveragent.tar.gz", "wb") as code:
            code.write(response.content)
    else:
        sys.exit(127)
    command1 = subprocess.Popen(r"tar xzf %s -C %s" % ("webserveragent.tar.gz", r"/opt"), shell=True,
                                stdout=subprocess.PIPE)
    out, err = command1.communicate()
    print(out)
    subprocess.call(['chmod', '755', '-R ', r'/opt'])
    webserveragentconf = '''
LoadFile /opt/appdynamics-sdk-native/sdk_lib/lib/libappdynamics_native_sdk.so
#Load the Apache Agent. In this example for Apache 2.4
LoadModule appdynamics_module /opt/appdynamics-sdk-native/WebServerAgent/Apache/libmod_appdynamics.so
AppDynamicsEnabled On
#AppDynamics Controller connection.
AppDynamicsControllerHost %s
AppDynamicsControllerPort %s
AppDynamicsControllerSSL ON

#Account credentials
AppDynamicsAccountName  %s
AppDynamicsAccessKey  %s

#Configure Controller connection through an HTTP proxy server.
#AppDynamicsProxyHost <proxy host>
#AppDynamicsProxyPort <proxy port>

#Business application, tier, node
AppDynamicsApplication %s
AppDynamicsTier %s
AppDynamicsNode %s
'''%(AppDynamicsControllerHost,str(AppDynamicsControllerPort),AppDynamicsAccountName,AppDynamicsAccessKey,ApplicationName,ApplicationNode,cliqrNodePublicIp)
    webserverconfigfile = "/etc/httpd/conf/appdynamics_agent.conf"
    with open(webserverconfigfile, "w") as data:
        data.write(webserveragentconf)
    apacheconfigfile = "/etc/httpd/conf/httpd.conf"
    webserverconfigfilesam = "/opt/remoteFiles/appPackage/httpd.conf"
    shutil.copy(webserverconfigfilesam,apacheconfigfile)
    print("File copied")
    os.chdir(r"/opt/appdynamics-sdk-native")
    command1 = os.system("sh  install.sh ")
    command1 = os.system("sh  install.sh ")
    command1 = os.system(
        "nohup /opt/appdynamics-sdk-native/runSDKProxy.sh >>/dev/null 2>/opt/appdynamics-sdk-native/logs/proxy.out &")
    command1 = subprocess.Popen("apachectl restart", shell=True, stdout=subprocess.PIPE)
    out, err = command1.communicate()
    print(out)




if __name__ == "__main__":
    try:
        AppdynamicsUsername = os.environ['AppdynamicsUsername']
        AppdynamicsPassword = os.environ['AppdynamicsPassword']
        AppDynamicsControllerHost = os.environ['AppDynamicsControllerHost']
        AppDynamicsControllerPort = os.environ['AppDynamicsControllerPort']
        AppDynamicsAccountName = os.environ['AppDynamicsAccountName']
        AppDynamicsAccessKey = os.environ['AppDynamicsAccessKey']
        #cliqrNodePublicIp=os.environ['cliqrNodePublicIp']
    except Exception as e:
        print(e)
        print("Error while getting environment variables")
        sys.exit(127)
    try:
        ApplicationName = os.environ['ApplicationName']
        ApplicationNode = os.environ['ApplicationName']
        cliqrNodePublicIp=os.environ['cliqrNodePublicIp']

    except:
        pass
    try:
        cliqrWebServerType = os.environ['cliqrWebServerType']
    except:
        cliqrWebServerType = ''
        pass
    try:
        cliqrWARFile = os.environ['cliqrWARFile']
    except:
        cliqrWARFile = ''
        pass
    try:
        cliqrDatabaseType = "postgre"  # os.environ['cliqrWebServerType']
    except:
        cliqrDatabaseType = ''
        pass
    if "tomcat" in cliqrWebServerType and len(cliqrWARFile) > 1:
        access_token = GetToken(AppdynamicsUsername,AppdynamicsPassword)
        javaserveragent(access_token,ApplicationName,ApplicationNode,AppDynamicsControllerHost,AppDynamicsControllerPort,AppDynamicsAccountName,AppDynamicsAccessKey,cliqrNodePublicIp)
        machineagent(access_token,AppDynamicsControllerHost,AppDynamicsControllerPort,AppDynamicsAccountName,AppDynamicsAccessKey,cliqrNodePublicIp)
    elif "apache" in cliqrWebServerType:
        access_token = GetToken(AppdynamicsUsername,AppdynamicsPassword)
        webserveragent(access_token,ApplicationName,ApplicationNode,AppDynamicsControllerHost,AppDynamicsControllerPort,AppDynamicsAccountName,AppDynamicsAccessKey,cliqrNodePublicIp)
        machineagent(access_token,AppDynamicsControllerHost,AppDynamicsControllerPort,AppDynamicsAccountName,AppDynamicsAccessKey,cliqrNodePublicIp)
    elif len(cliqrDatabaseType) > 1:
        access_token = GetToken(AppdynamicsUsername,AppdynamicsPassword)
        dbagent(access_token,AppDynamicsControllerHost,AppDynamicsControllerPort,AppDynamicsAccountName,AppDynamicsAccessKey)
    else:
        access_token = GetToken(AppdynamicsUsername,AppdynamicsPassword)
        machineagent(access_token,AppDynamicsControllerHost, AppDynamicsControllerPort,AppDynamicsAccountName,AppDynamicsAccessKey,cliqrNodePublicIp)







