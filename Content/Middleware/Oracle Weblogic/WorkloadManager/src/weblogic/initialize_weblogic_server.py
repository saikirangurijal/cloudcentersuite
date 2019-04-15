import sys
import os
from utils import get_script_path, parse_file, get_nodes

# Read WLS Template Jar
def read_template():
    try:
        readTemplate(wlshome + "/common/templates/wls/wls.jar")
    except:
        print "Error Reading the Template"
        sys.exit(127)

# Print Domain
def printdomain():
    print '------------------------------'
    print "Properties Information"
    print '------------------------------'
    for key, val in _dict.iteritems():
        print key, "=>", val


# Parse Domain Properties file to Dictonary
def export_properties():
    global _dict
    global mwhome
    global wlshome
    global domain_root
    global domain_home
    global domain_username
    global domain_password
    global admin_port
    global admin_address
    global admin_port_ssl

    try:
        mwhome = _dict.get('mwhome')
        wlshome = _dict.get('wlshome')
        domain_root = _dict.get('domainroot')
        
        domain_home = _dict.get('domain_name')
        domain_username = os.environ.get('adminUserName')
        domain_password = os.environ.get('adminPassword', 'weblogic123')

        admin_port = int(_dict.get("admin.port"))
        admin_address = _dict.get("admin.address")
        admin_port_ssl = int(_dict.get("admin.port.ssl"))

    except Exception, err:
        print err
        sys.exit(127)


# Set Admin Listen Address
def set_admin(address):
    cd('Servers/AdminServer')
    set('ListenAddress', address)
    set('ListenPort', admin_port)

# Configure Admin Addess and Port
def config_admin(address):
    cd('Servers/AdminServer')
    set('ListenAddress', address)
    set('ListenPort', admin_port)

    create('AdminServer', 'SSL')

    cd('SSL/AdminServer')
    set('Enabled', 'True')
    set('ListenPort', admin_port_ssl)

# Set Admin Server Password
def set_admin_user_password():
    try:
        cd('/')
        cd('Security/base_domain/User/' + domain_username)
        cmo.setPassword(domain_password)

        cd('/NMProperties')
        set('SecureListener', 'false')

    except Exception, err:
        print err
        print "Error setting user password"
        sys.exit(127)

# Create JMS Server
def create_jms_server():
    try:
        cd('/')
        create('myJMSServer', 'JMSServer')
    except:
        print "Error in creating a JMS server"

# Create JMS System Resource
def create_jms_sys_resource():
    try:
        cd('/')
        create('myJmsSystemResource', 'JMSSystemResource')
        cd('JMSSystemResource/myJmsSystemResource/JmsResource/NO_NAME_0')
    except:
        print "Error in creating a JMS system resource"


# Create JMS Queque
def create_jms_queue():
    try:
        myq = create('myQueue', 'Queue')
        myq.setJNDIName('jms/myqueue')
        myq.setSubDeploymentName('myQueueSubDeployment')
        cd('/')
        cd('JMSSystemResource/myJmsSystemResource')
        create('myQueueSubDeployment', 'SubDeployment')
    except:
        print "Error in creating JMS queue"

# Create JDBC User
def create_jdbc_user():
    try:
        cd('/')
        create('myDataSource', 'JDBCSystemResource')
        cd('JDBCSystemResource/myDataSource/JdbcResource/myDataSource')
        create('myJdbcDriverParams', 'JDBCDriverParams')
        cd('JDBCDriverParams/NO_NAME_0')
        set('DriverName', 'org.apache.derby.jdbc.ClientDriver')
        set('URL', 'jdbc:derby://localhost:1527/db;create=true')
        set('PasswordEncrypted', 'PBPUBLIC')
        set('UseXADataSourceInterface', 'false')
        create('myProps', 'Properties')
        cd('Properties/NO_NAME_0')
        create('user', 'Property')
        cd('Property/user')
        cmo.setValue('PBPUBLIC')
        cd('/JDBCSystemResource/myDataSource/JdbcResource/myDataSource')
        create('myJdbcDataSourceParams', 'JDBCDataSourceParams')
        cd('JDBCDataSourceParams/NO_NAME_0')
        set('JNDIName', java.lang.String("myDataSource_jndi"))
        cd('/JDBCSystemResource/myDataSource/JdbcResource/myDataSource')
        create('myJdbcConnectionPoolParams', 'JDBCConnectionPoolParams')
        cd('JDBCConnectionPoolParams/NO_NAME_0')
        set('TestTableName', 'SYSTABLES')
    except:
        print "Error in creating JDBC user"


def target_resource():
    try:
        cd('/')
        assign('JMSServer', 'myJMSServer', 'Target', 'AdminServer')
        assign('JMSSystemResource.SubDeployment', 'myJmsSystemResource.myQueueSubDeployment', 'Target', 'myJMSServer')
        assign('JDBCSystemResource', 'myDataSource', 'Target', 'AdminServer')
    except:
        print "Error in targeting resources to servers"

# Write Weblogic Domain
def write_domain():
    try:
        print "Writing Domain in progress"
        setOption('OverwriteDomain', 'true')

        writeDomain(domain_root + '/' + domain_home)
        closeTemplate()
    except Exception, err:
        print err
        print "Writing domain failed"

# Create Cluster
def create_cluster(name):
    try:
        cd('/')
        create(name, 'Cluster')
        cd('Cluster/'+name)

        set('ClusterMessagingMode', "unicast")
    except:
        print "Error while Creating Cluster", cluster
        print "Dumpstack: \n -------------- \n", dumpStack()
        sys.exit(2)

# Create Machine
def _create_machine(name, ip):
    try:
        cd('/')
        create(name,'Machine')
        
        cd('/Machines/'+name)
        create(name,'NodeManager')
        
        cd('/Machines/'+name+'/NodeManager/'+name)
        set('NMType','Plain')
        set('ListenAddress',ip)
        set('ListenPort',int(5556))
        set('DebugEnabled',false)

    except Exception, err:
        print err

# Create Managed Server
def create_manage_server(name, address, port):
    try:
        cd('/')
        create(name, 'Server')
        cd('/Servers/' + name)

        set('ListenAddress',address)
        set('ListenPort',int(port))
        set('ListenPortEnabled',true)

    except Exception, err:
        print err

# Get All Nodes as Dictionary
def get_nodes_dict():
    nodes = {}
    try:
        app_tier_name = os.environ.get("cliqrAppTierName", False)
        if not app_tier_name:
            sys.exit(127)

        names = str(os.environ['CliqrTier_' + app_tier_name + '_HOSTNAME']).split(',')
        ips = str(os.environ['CliqrTier_' + app_tier_name + '_IP']).split(',')

        for i in range(0, len(names)):
            nodes[names[i]] = ips[i]

    except Exception, err:
        print err
        sys.exit(127)

    return nodes


# Assign server to cluster
def assign_to_cluster(server, cluster):
    assign('Server',server,'Cluster',cluster)

# Assign server to machine
def assign_to_machine(server, machine):
    assign('Server', server,'Machine', machine)

if __name__ != "__main__":
    print "Creating Domain from Domain Template..."

    nodes = get_nodes()
    hostname = os.environ.get("cliqrNodeHostname")
    if hostname in nodes[0]['name']:
        properties_file_path = get_script_path() + "/domain.properties"
        _dict = parse_file(properties_file_path)

        export_properties()
        read_template()

        config_admin(nodes[0]['ip'])
        set_admin_user_password()

        cluster_name = hostname + '.Cluster'
        create_cluster(cluster_name)

        start_port_no = 7005
        for node in nodes:
            machine_name = node['name'] + '.Machine'
            _create_machine(machine_name, node['ip'])

            managed_server_name = node['name'] + '.Server'
            create_manage_server(managed_server_name, node['ip'], start_port_no)

            assign_to_machine(managed_server_name, machine_name)
            assign_to_cluster(managed_server_name, cluster_name)

            #start_port_no = start_port_no + 1
    
        create_jms_server()
        create_jms_sys_resource()
        create_jms_queue()
        create_jdbc_user()
        target_resource()

        write_domain()
