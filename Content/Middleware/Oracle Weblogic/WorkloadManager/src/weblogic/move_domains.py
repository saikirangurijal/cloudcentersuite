import subprocess
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
    global private_key_path
    global user
    global connection_path
    try:
        domain_name = _dict.get('domain_name')
        domain_root = _dict.get('domainroot')
        domain_path = domain_root + '/' + domain_name
        private_key_path = _dict.get('private_key_path')
        user = _dict.get('user')
        connection_path = _dict.get('connection_path')

        admin_username = os.environ.get('adminUserName')
        admin_password = os.environ.get('adminPassword')
    except Exception, err:
        print err
        sys.exit(127)


# Move Domains to Child nodes
def move_domains(user, host, path):
    try:
        # Use scp to send file from local to host.
        p = subprocess.Popen(['scp', '-r','-o StrictHostKeyChecking=no','-i' ,private_key_path, domain_path, '{0}@{1}:{2}'.format(user, host, path)])
        sts = p.wait()
        
        ssh_p = subprocess.Popen(['ssh','-o StrictHostKeyChecking=no', '-i', private_key_path, '{0}@{1}'.format(user,host), "sh -c '/usr/local/agentlite/service/weblogic/msserver.sh > /dev/null 2>&1 &'"])
    except CalledProcessError:
        print('ERROR: Connection to host failed!')

nodes = get_nodes()
hostname = os.environ.get("cliqrNodeHostname")
if hostname in nodes[0]['name']:
    properties_file_path = get_script_path() + "/domain.properties"
    _dict = parse_file(properties_file_path)
    export_properties()

    for node in nodes[1::]:
        move_domains(user, node['name'], connection_path)
