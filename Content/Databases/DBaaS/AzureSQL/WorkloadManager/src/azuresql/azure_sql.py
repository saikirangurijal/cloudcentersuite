#!/usr/bin/env python
import os
from datetime import time

from haikunator import Haikunator
import sys,time
from util import *
from msrestazure.azure_exceptions import CloudError
from error_utils import ErrorUtils
import json

haikunator = Haikunator()

'''
   Azure SQL
    
'''
class AzureSQL(object):
    def __init__(self, location, subscription_id, parameters):

        self.params = parameters

        self.group_name = self.params['resourceGroup']

        self.location = location

        self.subscription_id = subscription_id

        self.name = self.params['name']

        self.username = self.params['administrator_login']

        self.password = self.params['administrator_login_password']

        self.db_name= self.params['dbName']

        self.public_IP = self.params['publicIP']

        self.client = None

        self.version = ""

        self.dependents = os.environ.get('cliqrAppTierName', "")

    def create(self):
        '''
            Create SQL Server
            Create Database for that SQl Server and creates firewall rule for the publicI of previous tier
        '''

        print_log('Creating SQL Server.')

        try:

            print_log("********get sql server info.")
            try:
                #print_log("server name is :",self.name)
                print("############## Server name availability check")

                _server_info=self.check_name_availability(self.name)

                if not _server_info:
                    print_error(ErrorUtils.api_error("ResourceAlreadyExists", "", name=self.name))
                    print_log("ResourceAlreadyExists")
                    sys.exit(127)

            except CloudError as c:
                pass
            except Exception as e:
                pass

            # Create a SQL server

            async_server_create = self.client.sql_mgmt.servers.create_or_update(
                self.group_name,
                self.name,
                {
                    'location': self.location,
                    'administrator_login': self.username,  # Required for create
                    'administrator_login_password': self.password  # Required for create
                }
            )
            sql_info = async_server_create.result()

            is_server_created = True

            print_log("Server Created Successfully.")

            # Create a database
            print_log('Creating Database.')
            async_db_create = self.client.sql_mgmt.databases.create_or_update(
                self.group_name,
                self.name,
                self.db_name,
                {
                    'location': self.location,
                    'api_version':self.version
                }
            )
            db_info = async_db_create.result()
            is_db_created = True

            print_log("Database Created Successfully")

            print_log("Creating firewall rule.")
            #print_log("public ip is :",self.public_IP)
            try:
                firewall_rule = self.client.sql_mgmt.firewall_rules.create_or_update(
                    self.group_name,
                    self.name,
                    "contentlibrary_fire_wall_rule",
                    self.public_IP,  # Start ip range
                    self.public_IP,	# End ip range
                    {
                        'api_version': self.version
                    }
                )
                print_log("Firewall rule created.")
            except Exception as er:
                print_error("firewall rule creation failed.")
                print_error (ErrorUtils.api_error (er.error.error, er.message,publicIP=self.public_IP))
                print_log(er)

            json_result = {
                "hostName": self.dependents,
                "ipAddress": "",
                "environment": {
                    "serverName": self.name,
                    "dbName": self.db_name,
                    "serverUsername": self.username,
                    "serverPassword": self.password
                }
            }
            print("json result.....")
            print(json_result)
            print_result(json.dumps (json_result))
            time.sleep(30)
            return async_db_create

        except CloudError as cloud_err:
            print_log("some error occured in cloud.")
            print_log(cloud_err)
            print_error(ErrorUtils.api_error(cloud_err.error.error, cloud_err.message, name=self.name))
            write_error(cloud_err)
            self.delete ()
            sys.exit(127)

        except Exception as err:
            print_log(err)
            print_error(ErrorUtils.internal_error(err))
            write_error(err)
            self.delete ()
            sys.exit(127)

    def check_name_availability(self, server_name, ):
        print("In name check method..")
        try:
            resource_availibility = self.client.sql_mgmt.servers.check_name_availability(server_name,
                                                                                         custom_headers=None, raw=False)

            print_log(resource_availibility.available)
            print(resource_availibility.available)
            return resource_availibility.available
        except Exception as er:
            print(er)
            write_error(er)

    def delete(self):
        '''
            Delete SQL Server and data base
        '''
        print_log("Stop Initiated.")
        group_name = self.group_name
        name = self.name
        db_name=self.db_name
        is_db_exists=False
        is_server_exists=False

        response_db_list= self.client.sql_mgmt.databases.list_by_server(self.group_name,self.name)

        response_server_list = self.client.sql_mgmt.servers.list_by_resource_group(group_name)

        for item in response_db_list :

            if item.name==db_name:
                print_log("database found.")
                is_db_exists=True


        print("is db found :",is_db_exists)

        for items in response_server_list:

            if items.name == name:
                is_server_exists = True


        if is_db_exists:
            try:
                self.client.sql_mgmt.databases.delete(group_name, name, db_name)
                print_log("Data base deleted.")
                is_db_exists=False
            except Exception as er:
                print_log(er)

        if is_server_exists :
            try:
                self.client.sql_mgmt.servers.delete(group_name,name)
                print_log("SQL Server deleted.")
                is_server_exists = False
            except Exception as err:
                print_log(er)

        print_log("Service Stopped")




