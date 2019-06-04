
import time
import json
import sys,os
import googleapiclient.discovery
from oauth2client._helpers import _to_bytes
from google.oauth2 import service_account
from util import print_error,print_log,print_result,write_error
from error_utils import ErrorUtils
import re
import base64

class mysql_instance():
    def __init__(self,auth_security):
        """
        Authenticating google cloud account and assign it into service object and access it within the class
        :param auth_security:
        """
        self.dbs = []
        self.db_name = ''
        self.project = ''
        self.instance = ''
        self.region = ''
        self.user_name = ''
        self.db_params = {}
        self.instance_params = {}
        self.instance_info = {}
        self.DEFAULT_DB_LIST = ['information_schema', 'mysql', 'performance_schema']
        try:            
            auth_sercurity  = auth_security
            SCOPES = ["https://www.googleapis.com/auth/sqlservice.admin"]  
            credentials = service_account.Credentials.from_service_account_info(auth_sercurity, scopes=SCOPES)            
            self.service = googleapiclient.discovery.build('sqladmin', 'v1beta4', credentials=credentials)
             
        except Exception as err:
            print(err)
            sys.exit(127)

    def _getting_instances(self, instance_name=None, checkFor=None):
        """
        Getting the instance informaation by project and assign it into instance object and access it within the class
        :param instance_name:
        :param checkFor:
        :return:
        """

        try:
            instances = []
            names = []
            print("Getting instance for creating sql server")     

            self.instance_info = {} 
            request = self.service.instances().list(project=self.project)
            response = request.execute()
            if 'items' in response:
                items = response['items']                            
                for item in items:         

                    if instance_name == item['name']:
                        self.instance_info = item 
                        print("source instances is found :") 
             
            if 'name' not in self.instance_info and checkFor == None:  
                print("No instance are there.") 
                
        except Exception as er:
            print("Error, there is no instance are there. Please create new instance")
            print_error(er) 
            sys.exit(127)
            
    def _getting_db(self):
        """
        Getting the database list by using the project and instance assign  and access database object to access it within the class
        :return:
        """
        try:
            instances = []
            print("Getting database in this instance") 
            response = ''
            request = self.service.databases().list(project=self.project, instance=self.instance)            
            response = request.execute()  
                   
            if response:
                items = response["items"] 
                for item in items:
                    if item['name'] not in self.DEFAULT_DB_LIST:
                        try:
                            self.dbs.append(item['name'])
                        except:
                            continue 
                print("databases are :", self.dbs)

                if not self.dbs:
                    print("No database are there .")
            else:
                print("No database are there .")
                print("Please create the new instance")
        except Exception as er:
            print("Error, there is no database are there. Please create new database")
            print_error(er)
            sys.exit(127)

    def _creating_instance(self, target_pool_body):
        """
        Create an instance by passing the generated payload and project
        :param target_pool_body:
        :return:
        """

        print 'Instance creation service running'
        try:             
            request = self.service.instances().insert(project=self.project, body=target_pool_body)
            response = request.execute()
            if response: 
                self.instance = response["targetId"]
                self.instance_link = response["targetLink"]
                print "Created instance with : "+response["targetId"]         
                ### There is a few minutes to take the instance as runnable state.####
                flag = 1
                while flag == 1:                             
                    self._getting_instances(response["targetId"]) 
                    print "status of instance"
                    print self.instance_info['state']
                    if self.instance_info['state'] == 'RUNNABLE': 
                        flag = 0 
                        print "Intializing User Creation"
                        self._create_user() 
                        if self.user_name:
                            time.sleep(30)
                            print "Intializing Database Creation"
                            self._create_db() 
                            if not self.db_name: 
                                print "Database not created. Intiating Delete Instance."
                                self.delete_instance()
                                sys.exit(127)
                            else:
                                print "Instance creation process successfully completed"
                        else:
                            print "User not created. Intiating Delete Instance."
                            self.delete_instance()
                            sys.exit(127)
                    else:
                        time.sleep(120) 
                        continue   
            else:
                print("Failed to create instance")
        except Exception as err:
            print(err)
            print_error(err)
            sys.exit(127)
    
    def _create_db(self):
        """
        Create an database by passing the project and instance params.
        :return:
        """

        try:
            target_pool_body = {                
                "name": self.db_name,
                "instance":self.instance,
                "project":self.project
            }
            """if charset != None:
                target_pool_body['charset'] =  charset
            if collation != None:
                target_pool_body['collation'] =  collation 
            """
            print "Creating database"
            request = self.service.databases().insert(project=self.project, instance=self.instance, body=target_pool_body)
            response = request.execute()
            if response:
                self.db_name = response["targetId"]
                self.db_link = response["targetLink"]  
                print "Database created."
            else:
                print "Failed to create database."
        except Exception as err:
            print(err)
            print_error(err) 
            self.delete_instance()
            sys.exit(127)
    
    def _create_user(self):
        """
        Create user by passing the project and instance and db_params object
        :return:
        """

        try:
            request = self.service.users().insert(project=self.project, instance=self.instance, body=self.db_params)
            response = request.execute()
            if response: 
                self.user_name = response["targetId"] 
                print "Default users created."
            else:                
                print "Failed to create users."
                
        except Exception as err:
            print(err)
            print_error(err)
            self.delete_instance()
            sys.exit(127)
    
    def _delete_db(self):
        """
        Delete database by passing project, instance and database
        :return:
        """

        try: 
            self._getting_db()
            responseDbState = True
            if len(self.dbs) > 0:
                for database in self.dbs:
                    try:
                        request = self.service.databases().delete(project=self.project, instance=self.instance, database=database)
                        response = request.execute()
                        if response:
                            self.db_status = response["status"]
                            if self.db_status == 'DONE':
                                print("deleted database successfully!!!")                        
                            else:
                                print("Database status: "+self.db_status)
                                responseDbState = False
                    except:
                        continue 
                    
            return responseDbState
        except Exception as err:
            print(err)
            print_error(err)
            sys.exit(127)
     
    def delete_instance(self):
        """
        Delete the instance by passing project
        :return:
        """

        print_log("Deleting instance")  
        if self.instance != None:
            try:
                db_delete_state = self._delete_db()   
                print db_delete_state  
                if db_delete_state:     
                    request = self.service.instances().delete(project=self.project, instance=self.instance)
                    response = request.execute()                    
                    if response:
                        flag = 1
                        while flag == 1:                     
                            self._getting_instances(self.instance)
                            if 'name' not in self.instance_info: 
                                flag = 0                                              
                            else:
                                time.sleep(30) 
                                continue   
                        print_log("Deleted instance successfully!!!")               
                    else:
                        print_log("Failed to delete the instance")   
            except Exception as err:
                print(err)
                print_error(err)
                sys.exit(127)
        else:
            print_log("Failed to delete the instance")   

def main(cmd):
    """
    This is the function to create or delete the service action based on life cycle action command
    :param cmd:
    :return:
    """
    arguments = cmd  
    db_password = ''

    if 'geDbPassword' in os.environ:
        db_password = os.environ['geDbPassword'] 
    try:                        
        region_name = os.environ['CliqrCloud_Region']  
        instance_name = os.environ['geInstanceName']   
        auth_security = os.environ['CliqrCloud_JsonServiceAccount'] 
        auth_security = auth_security.replace('\n', '')
        auth_security = json.loads(auth_security)            
        project_name = auth_security['project_id'] 

        if arguments in "start": 
            sqlType = os.environ['geSqlType']  
            db_username = os.environ['geDbUserName']              
            db_name = os.environ['geDbName'] 
            db_host = os.environ['geDbHost']    
            validate_resp = ErrorUtils.validate_name(instance_name)
            if validate_resp['error']:
                print_error(validate_resp['message'])
                sys.exit(127)

        dependents = os.environ.get('CliqrDependents', "")
        ip_address = ''
        networks = []
        if len(dependents) > 0:
			if 'CliqrTier_' + dependents + '_PUBLIC_IP' in os.environ:
				istances = str(os.environ['CliqrTier_' + dependents + '_HOSTNAME']).split(',')
				network_ip =  str(os.environ['CliqrTier_' + dependents + '_PUBLIC_IP']).split(',') 
				ip_address = str(os.environ['CliqrTier_' + dependents + '_IP']).split(',') 
				print("my instances is ===================>{}".format(istances))
				print("my vm instance public ip is ===================>{}".format(network_ip))
				networks.append({
					"name": "Compute Engine",
					"value": network_ip
				})
        
    except Exception as er:
        print_error(er.message)
        f = open('FAILURE', 'w')
        f.write(str(er))
        f.close()
        print_error("Unable to get environmental variables")
        sys.exit(127)
    
     
    def __create_instance(auth_security, project_name, region_name, body, db_params, db_name, sqlType):
        """
        Assinging the environment variable to object and call the instance creation process
        :param auth_security:
        :param project_name:
        :param region_name:
        :param body:
        :param db_params:
        :param db_name:
        :return:
        """
        response = {}
        try:
            _object = mysql_instance(auth_security)      
            _object.project = project_name 
            _object.region = region_name
            _object._getting_instances(body['name'], 'new')         
            if _object.instance_info:
                instance_exists_msg = ErrorUtils.resource_exists(body['name'])  
                print instance_exists_msg              
                print_error(instance_exists_msg)
                sys.exit(127)                 
            else:             
                print "Sending params to create instance"   
                _object.db_params = db_params
                _object.db_name = db_name 
                _object.instance_params = body            
                _object._creating_instance(body) 
                data = _object.instance_info
                ip = data["ipAddresses"][0]["ipAddress"]
                sql_type =  sqlType.lower()
		param1 =  base64.b64encode(db_params['password'].encode())
                response =   {
                        'driverClassName' : sql_type,
                        'url' : sql_type+'://'+ip+':3306/'+db_name,
                        'Database_Username':db_params['name'],
                        'Database_Name': db_name,
                        'DB_TIER_IP' : ip,
                        'Database_IP': ip,                     
                        'CloudCenter_Database_IP': ip,
                        'CloudCenter_DB_TIER_IP': ip,
			'param1': param1,
			'instanceName': body['name']

                    }
            return response
            
        except Exception as Err:
            print("Error while creating instance {}".format(Err))
            sys.exit(127)

    def __delete_instance(auth_security, project_name, region_name, instance_name):
        """
        Assinging the environment variable to object and call the deletion instance process
        :param auth_security:
        :param project_name:
        :param region_name:
        :param instance_name:
        :return:
        """
        print "Intiaiting deleting service"
        try:
            _object = mysql_instance(auth_security) 
            _object.project = project_name 
            _object.region = region_name
            _object.instance = instance_name
            _object._getting_instances(instance_name)    
            if 'name' in _object.instance_info: 
                print "instance found"
                _object.instance = instance_name
                _object.delete_instance()                
            else: 
                print ("Instance doesn't exists.")

        except Exception as e:
            print("Error while deleting instances {}".format(e))

    def mysql_params(project, name, region, networks=[]):
        """
        Generating payload for mysql instance creation
        :param project:
        :param name:
        :param region:
        :param networks:
        :return:
        """
        return { 
            "name": name,  
            "project": project, 
            "backendType": "SECOND_GEN",
            "databaseVersion": "MYSQL_5_7",
            "region": region,  
            "settings": {               
                "authorizedGaeApplications": [],
                "tier": "db-n1-standard-1",
                "dataDiskSizeGb": 10,
                "dataDiskType": "PD_SSD", 
                "storageAutoResize": True,
                "storageAutoResizeLimit": 0,
                "backupConfiguration": { 
                   "startTime": "12:00",
                    "enabled": True,
                    "binaryLogEnabled": True,
                    "replicationLogArchivingEnabled": False
                },
                "pricingPlan": "PER_USE",
                "replicationType": "SYNCHRONOUS",
                "activationPolicy": "ALWAYS",
                "ipConfiguration": {
                    "ipv4Enabled": True,
                    "authorizedNetworks": networks
                }, 
                "maintenanceWindow": { 
                    "hour": 0,
                    "day": 0
                }                
            }, 
            "instanceType": "CLOUD_SQL_INSTANCE" 
        }
         
    def postgre_params(project, name, region, networks=[]):
        """
        Generating payload for postgresql instance creation
        :param project:
        :param name:
        :param region:
        :param networks:
        :return:
        """
        return { 
            "name": name,  
            "project": project, 
            "backendType": "SECOND_GEN",
            "databaseVersion": "POSTGRES_9_6",
            "region": region, 
            "settings": {                  
                "pricingPlan": "PER_USE",
                "replicationType": "SYNCHRONOUS",
                "activationPolicy": "ALWAYS",
                "authorizedGaeApplications": [],
                "tier": "db-custom-1-3840",
                "dataDiskSizeGb": 10,
                "dataDiskType": "PD_SSD", 
                "storageAutoResize": True,
                "storageAutoResizeLimit":0,
                "backupConfiguration": { 
                    "startTime": "14:00",
                    "enabled": True,
                    "binaryLogEnabled": False 
                },
                "ipConfiguration": {
                    "ipv4Enabled": True,
                    "authorizedNetworks": networks
                }, 
                "maintenanceWindow": { 
                    "hour": 0,
                    "day": 0
                }                
            }, 
            "instanceType": "CLOUD_SQL_INSTANCE" 
        }
    

    if arguments in "start":
        print_log("Intializing Instance...") 
        instance_params = {}
        db_params = {
            "name": db_username,
            "host": db_host,
            "password": db_password,
        }

        if sqlType == "MYSQL": 
            instance_params = mysql_params(project_name, instance_name, region_name, networks)
        elif sqlType == "POSTGRESQL":
            instance_params = postgre_params(project_name, instance_name, region_name, networks)
        else:
            print_error("Error, Please give correct sql type.")
        
        try:  
             
            if instance_params:
                print_log("Creating Instance...") 
                response = __create_instance(auth_security, project_name, region_name, instance_params, db_params, db_name, sqlType)
                print "Setting database to environment variable"
                json_result =  { 
                    "hostName":dependents,
                    "ipAddress": "",
                    'DB_TIER_IP' : response['DB_TIER_IP'],
                    'Database_IP': response['DB_TIER_IP'],
                    "environment": response
                } 

                print_result(json.dumps(json_result))
                    

        except Exception as e:
            print(e)
        
    elif arguments in "stop":
        print_log("Deleting Instance...") 
        try:
            print("Stoping Sql Server")               
            __delete_instance(auth_security, project_name, region_name, instance_name)
        except:
            print("Error while taking arguments from the user")
 
