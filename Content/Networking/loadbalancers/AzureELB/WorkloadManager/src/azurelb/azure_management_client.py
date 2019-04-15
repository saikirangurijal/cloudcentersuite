#!/usr/bin/env python
# Azure Management Client
# Construct Azure Client with Credentials
# Create Compute Client Object
# Create Resource Management Client Object
# Create Network Management Client Object

import os
import json
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from haikunator import Haikunator
import sys
from util import *
from azure_load_balancer import AzureInternalLoadBalancer, AzurePublicLoadBalancer
from error_utils import ErrorUtils


'''
    Load Parameters
'''
try:
    with open('params.json', 'r') as file:
        global params
        params = json.loads(str(file.read()), object_pairs_hook=deunicodify_hook)
except Exception as err:
    print_error(ErrorUtils.internal_error(err))
    sys.exit(127)


INTERNAL_LOAD_BALANCER_TYPE = 'private'
PUBLIC_LOAD_BALANCER_TYPE = 'public'

'''
    Azure Management Client
'''
class AzureManagement(object):
    def __init__(self):
        #
        # Initialize Azure Basic Setup
        #
        self.group_name = params['resourceGroup']
        self.location = params['account']['location']

        self.subscription_id = params['account']['subscriptionId']

        self.credentials = ServicePrincipalCredentials(
            client_id=params['account']['clientId'],
            secret=params['account']['clientSecret'],
            tenant=params['account']['tenantId']
        )

        self.compute_mgmt = ComputeManagementClient(self.credentials, self.subscription_id)
        self.network_mgmt = NetworkManagementClient(self.credentials, self.subscription_id)
        self.resource_mgmt = ResourceManagementClient(self.credentials, self.subscription_id)

        # Load Balancer type
        self.lbtype = str(params['loadBalancer']['type']).strip().lower()

        if self.lbtype in INTERNAL_LOAD_BALANCER_TYPE:
            self._load_balancer = AzureInternalLoadBalancer(self.location, self.subscription_id, params)
        elif self.lbtype in PUBLIC_LOAD_BALANCER_TYPE:
            self._load_balancer = AzurePublicLoadBalancer(self.location, self.subscription_id, params)
            
        self._load_balancer.client = self

    def create_public_ip(self, public_ip_name, public_ip_parameters) :
        # Create Public IP
        print 'Create Public IP'
        
        public_ip_parameters['location'] = self.location

        async_publicip_creation = self.network_mgmt.public_ip_addresses.create_or_update(
            self.group_name,
            public_ip_name,
            public_ip_parameters
        )

        return async_publicip_creation.result()

    def get_public_ip(self, name):
        # Get Public IP
        print 'Getting Public IP'

        async_publicip_creation = self.network_mgmt.public_ip_addresses.get(
            self.group_name,
            name
        )

        return async_publicip_creation.result()

    def delete_public_ip(self, name):
        # Delete Public IP
        print 'Deleting Public IP'

        async_publicip_deletion = self.network_mgmt.public_ip_addresses.delete(
            self.group_name,
            name
        )

        return async_publicip_deletion.result()
        
    @property
    def load_balancer(self):      
        # Get Load Balancer Object  
        return self._load_balancer
       
        


      
