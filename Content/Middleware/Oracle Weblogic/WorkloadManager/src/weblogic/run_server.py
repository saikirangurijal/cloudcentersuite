import sys
import os
from utils import get_script_path, parse_file, get_nodes

# Domain Properties default config file to dictionary

def export_properties():
    global _dict
    global domain_name
    global domain_root
    global domain_path
    global admin_password
    global admin_username
    try:
        domain_name = _dict.get('domain_name')
        domain_root = _dict.get('domainroot')
        domain_path = domain_root + '/' + domain_name

        admin_username = os.environ.get('adminUserName')
        admin_password = os.environ.get('adminPassword', 'weblogic123')
    except Exception, err:
        print err
        sys.exit(127)

# Start NodeManager, AdminServer and All Cluster Manager Servers
def startAll(cluster_name, primary_node_ip):
    try:
        nmConnect(admin_username,admin_password,primary_node_ip,'5556',domain_name, domain_path, 'PLAIN')

        nmStart('AdminServer')
        connect(admin_username,admin_password,'t3://' + primary_node_ip + ":7001")

        start(cluster_name, 'Cluster')
    except Exception, err:
        print err
        sys.exit(127)

if __name__ != "__main__":
    print "Start All Servers............"
    nodes = get_nodes()
    hostname = os.environ.get("cliqrNodeHostname")
    if hostname in nodes[0]['name']:
        properties_file_path = get_script_path() + "/domain.properties"
        _dict = parse_file(properties_file_path)

        export_properties()

        # Read domain
        readDomain(domain_path)

        cluster_name = nodes[0]['name'] + '.Cluster'

        # Start All
        startAll(cluster_name, nodes[0]['ip'])

        print "Deploying Applications.............."

        # Deploy App
        app_package_path = os.environ.get('appPackage', '/opt/remoteFiles/appPackage/*.war')
        deploy('MyApplication', str(app_package_path).strip(), targets=cluster_name)
        print "Successfully Deployed!"

