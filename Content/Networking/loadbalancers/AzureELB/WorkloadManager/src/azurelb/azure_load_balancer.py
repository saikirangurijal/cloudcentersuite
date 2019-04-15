#!/usr/bin/env python

from haikunator import Haikunator
import sys
from util import *
from msrestazure.azure_exceptions import CloudError
from common import *
from error_utils import ErrorUtils
import json

haikunator = Haikunator()

'''
   Base Azure Load Balancer
   Load Balancer Type: Private, Public
   SKU: Basic
   FrontEnd: Single
'''
class AzureLoadBalancerBase(object):
    def __init__(self, location, subscription_id, parameters):
        self.params = parameters

        self.location = location

        self.subscription_id = subscription_id

        self.public_ip = None

        self.front_end_ip_configurations = self.params['loadBalancer']['frontEndIp']

        self.backend_pools = self.params['loadBalancer']['backEndPools']

        self.health_probes = self.params['loadBalancer']['healthProbes']

        self.rules = self.params['loadBalancer']['rules']

        self.nat_rules = self.params['loadBalancer']['inboundNatRules']

        self.client = None

    def get(self, name, group_name):
        '''
            Get Load Balancer information
        '''
        print "Getting Load Balancer Information"
        lb_info = self.client.network_mgmt.load_balancers.get(
            group_name,
            name
        )

        return lb_info

    def _assign_vms(self, lb_info):
        '''
            Assign VM instances to load balancer
        '''
        vms = self.params['vms']

        check_availability_set = False
        if len(vms) > 1:
            check_availability_set = True
            
        vm_configure_count = 0
        for vm in vms:
            vm_name = vm['name']

            back_end_address_pool_id = lb_info.backend_address_pools[0].id

            #inbound_nat_rule_id = lb_info.inbound_nat_rules[0].id
            vm_info = False
            try:
                print "Getting Virtual Machine instance information....."
                vm_info = self.client.compute_mgmt.virtual_machines.get(
                    self.vm_group_name,
                    vm_name
                )
            except CloudError as cloud_err:
                self._rollback(True, True)

                print_error(ErrorUtils.api_error(cloud_err.error.error, cloud_err.message, resourceGroup=self.vm_group_name, name=vm_name))
                write_error(cloud_err)

                sys.exit(127)
            except Exception as err:
                print err
                self._rollback(True, True)

                print_error(ErrorUtils.internal_error(err))
                write_error(err)

                sys.exit(127)


            if check_availability_set:
                if not vm_info.availability_set and vm_configure_count > 0:
                    break

            nic_name = vm_info.network_profile.network_interfaces[0].id.split('/')[-1]
            print nic_name
            nic_info = self.client.network_mgmt.network_interfaces.get(
                self.vm_group_name,
                nic_name
            )

            nic_ip_configurations = nic_info.ip_configurations[0].load_balancer_backend_address_pools
            if nic_ip_configurations:
                print_error(ErrorUtils.api_error("AlreadyNICAssigned", "", name=nic_name))

            try:
                # Updating NIC Information
                print "Updating NIC information"
                async_nic_creation = self.client.network_mgmt.network_interfaces.create_or_update(
                    self.vm_group_name,
                    nic_name,
                    update_nic_paramaters(back_end_address_pool_id, self.location, nic_info, self.params)
                )

                nic_info = async_nic_creation.result()
            except CloudError as cerr1:
                self._rollback(True, True)

                print_error(ErrorUtils.api_error(cerr1.error.error, cerr1.message, name=nic_name))
                write_error(cerr1)

                sys.exit(127)
            except Exception as err1:
                self._rollback(True, True)

                print_error(ErrorUtils.internal_error(err1))
                write_error(err1)

                sys.exit(127)

            vm_configure_count += 1
            print "Successfully load balancer configured in NIC"

        result = {
            "hostName":self.params['appTierName'],
            "environment": {
                "instanceName":self.params['loadBalancer']['name'],
                "instanceType": "LoadBalancer",
                "serviceType": "azurelb"
            }
        }
        if self.params['loadBalancer']['type'].lower() in 'public':
            result['ipAddress'] = str(self.public_ip.ip_address)
            
        return result

    def _rollback(self, is_load_balancer_created, is_new_public_ip_created):
        '''
            Rollback all items
        '''
        print_log("Started Rollbacking")

        if is_load_balancer_created:
            self.delete()
            
        if is_new_public_ip_created:
            print self.params
            self.client.delete_public_ip(self.params['publicIp']['name'])

        print_log("Rollback Done")



'''
    Public Load Balancer
'''
class AzurePublicLoadBalancer(AzureLoadBalancerBase):

    def create(self):
        '''
            Create Public Load Balancer
        '''
        self.group_name = self.params['resourceGroup']
        self.vm_group_name = self.params['resourceGroup']

        self.client.resource_mgmt.resource_groups.create_or_update(self.group_name, {'location':self.location})        
        self.name = self.params['loadBalancer']['name']
        
        # Creating Load Balancer
        print_log('Creating Load Balancer')

        # create public ip
        public_ip_name = self.params['publicIp']['name']
        is_new_public_ip_created = False
        is_load_balancer_created = False

        if self.params['publicIp']['createNew']:
            dns_name = "c-ext-service"+haikunator.haikunate()
            self.params['publicIp']['defaults']['dns_settings']['domain_name_label'] = dns_name

            try:
                self.public_ip = self.client.create_public_ip(public_ip_name, self.params['publicIp']['defaults'])
                is_new_public_ip_created = True
            except CloudError as cloud_err:
                print_error(ErrorUtils.api_error("PublicIpCreationError", cloud_err, name=public_ip_name))
                write_error(cloud_err)

                sys.exit(127)
            except Exception as err:
                print err
                print_error(ErrorUtils.internal_error(err))
                write_error(err)

                sys.exit(127)

        else:
            self.public_ip = self.client.get_public_ip(public_ip_name)
            
        try:
            print "**************Got Public Info"
            # create frontend pool configuration

            for front_end_ip_config in self.front_end_ip_configurations:
                front_end_ip_config['public_ip_address']['id'] = self.public_ip.id

            # create load balancing rules configuration
            rule_index = 1
            for rule in self.rules:
                rule['name'] = rule['name'] + "_" + str(rule_index)
                rule['frontend_ip_configuration']['id'] = construct_fip_id(self.client.subscription_id, self.group_name, self.name, self.front_end_ip_configurations[0]['name'])
                rule['backend_address_pool']['id'] = construct_bap_id(self.client.subscription_id, self.group_name, self.name, self.backend_pools[0]['name'])
                rule['probe']['id'] = construct_probe_id(self.client.subscription_id, self.group_name, self.name, self.health_probes[0]['name'])

                rule_index = rule_index + 1

            nat_rule_index = 1
            for rule in self.nat_rules:
                rule['name'] = rule['name'] + "_" + str(nat_rule_index)
                rule['frontend_ip_configuration']['id'] = construct_fip_id(self.client.subscription_id, self.group_name, self.name, self.front_end_ip_configurations[0]['name'])

                nat_rule_index = nat_rule_index + 1

            print "********get load balancer info"
            try:
                _lb_info = self.get(self.name, self.group_name)
                print _lb_info

                if _lb_info:
                    print_error(ErrorUtils.api_error("ResourceAlreadyExists", "", name=self.name))
                    sys.exit(127)

            except CloudError as c:
                pass
            except Exception as e:
                pass

            print_log("Initiated Load Balancer Creation")
            lb_async_creation = self.client.network_mgmt.load_balancers.create_or_update(
                self.group_name,
                self.name,
                {
                    'location': self.location,
                    'frontend_ip_configurations': self.front_end_ip_configurations,
                    'backend_address_pools': self.backend_pools,
                    'probes': self.health_probes,
                    'load_balancing_rules': self.rules,
                    'inbound_nat_rules': self.nat_rules
                }
            )

            lb_info = lb_async_creation.result()
            is_load_balancer_created = True

            print_log("Load Balancer Created Successfully")

            return self._assign_vms(lb_info)

        except CloudError as cloud_err:
            self._rollback(is_load_balancer_created, is_new_public_ip_created)

            print_error(ErrorUtils.api_error(cloud_err.error.error, cloud_err.message, name=self.name, publicip=self.params['publicIp']['name']))
            write_error(cloud_err)

            sys.exit(127)

        except Exception as err:
            self._rollback(is_load_balancer_created, is_new_public_ip_created)

            print_error(ErrorUtils.internal_error(err))
            write_error(err)

            sys.exit(127)

    def delete(self):
        '''
            Delete Load Balancer
        '''
        print_log("Stop Initiated")
        group_name = self.params['resourceGroup']
        name = self.params['loadBalancer']['name']

        async_lb_delete = self.client.network_mgmt.load_balancers.delete(
            group_name,
            name
        )

        async_lb_delete.wait()

        public_ip_name = self.params['publicIp']['name']

        public_ip_info = self.client.network_mgmt.public_ip_addresses.get(group_name, public_ip_name)
        
        self.client.network_mgmt.public_ip_addresses.delete(group_name, public_ip_info.name)

        print_log("Service Stopped")

        result = {
            "hostName":self.params["appTierName"],
            "status": "Terminated"
        }   

        return result    

'''
    Private Load Balancer
'''
class AzureInternalLoadBalancer(AzureLoadBalancerBase):
    def create(self):
        '''
            Create Private Load Balancer
        '''
        self.group_name = self.params['resourceGroup']
        self.vm_group_name = self.params['resourceGroup']     
        self.name = self.params['loadBalancer']['name']
        self.vnet_name = self.params['vnet']
        self.subnet = self.params['subnet']
        
        # Creating Load Balancer
        print_log('Creating Internal Load Balancer')
        is_load_balancer_created = False
            
        try:
            # create frontend pool configuration
            # Get SubNet
            if not self.vnet_name or not self.subnet:
                print_error(ErrorUtils.validation_error("VirtualNetworkMissing", "CreationError", parameter=self.name))
                sys.exit(127)
                
            subnet_info = self.client.network_mgmt.subnets.get(
                self.group_name,
                self.vnet_name,
                self.subnet
            )

            for front_end_ip_config in self.front_end_ip_configurations:
                del front_end_ip_config['public_ip_address']
                front_end_ip_config["subnet"] = {
                    "id": subnet_info.id
                }

            # create load balancing rules configuration
            rule_index = 1
            for rule in self.rules:
                rule['name'] = rule['name'] + "_" + str(rule_index)
                rule['frontend_ip_configuration']['id'] = construct_fip_id(self.client.subscription_id, self.group_name, self.name, self.front_end_ip_configurations[0]['name'])
                rule['backend_address_pool']['id'] = construct_bap_id(self.client.subscription_id, self.group_name, self.name, self.backend_pools[0]['name'])
                rule['probe']['id'] = construct_probe_id(self.client.subscription_id, self.group_name, self.name, self.health_probes[0]['name'])

                rule_index = rule_index + 1

            nat_rule_index = 1
            for rule in self.nat_rules:
                rule['name'] = rule['name'] + "_" + str(nat_rule_index)
                rule['frontend_ip_configuration']['id'] = construct_fip_id(self.client.subscription_id, self.group_name, self.name, self.front_end_ip_configurations[0]['name'])

                nat_rule_index = nat_rule_index + 1

            print "********get load balancer info"
            try:
                _lb_info = self.get(self.name, self.group_name)
                print _lb_info

                if _lb_info:
                    print_error(ErrorUtils.api_error("ResourceAlreadyExists", "", name=self.name))
                    sys.exit(127)

            except CloudError as c:
                pass
            except Exception as e:
                pass

            print_log("Initiated Load Balancer Creation")
            print self.rules
            lb_async_creation = self.client.network_mgmt.load_balancers.create_or_update(
                self.group_name,
                self.name,
                {
                    'location': self.location,
                    'frontend_ip_configurations': self.front_end_ip_configurations,
                    'backend_address_pools': self.backend_pools,
                    'probes': self.health_probes,
                    'load_balancing_rules': self.rules,
                    'inbound_nat_rules': self.nat_rules
                }
            )

            lb_info = lb_async_creation.result()
            is_load_balancer_created = True

            print_log("Load Balancer Created Successfully")

            return self._assign_vms(lb_info)

        except CloudError as cloud_err:
            self._rollback(is_load_balancer_created, False)

            print_error(ErrorUtils.api_error(cloud_err.error.error, cloud_err.message, name=self.name))
            write_error(cloud_err)

            sys.exit(127)

        except Exception as err:
            self._rollback(is_load_balancer_created, False)

            print_error(ErrorUtils.internal_error(err))
            write_error(err)

            sys.exit(127)

    def delete(self):
        '''
            Delete Private Load Balancer
        '''
        print_log("Stop Initiated")
        group_name = self.params['resourceGroup']
        name = self.params['loadBalancer']['name']

        async_lb_delete = self.client.network_mgmt.load_balancers.delete(
            group_name,
            name
        )

        async_lb_delete.wait()

        print_log("Service Stopped")

        result = {
            "hostName":self.params["appTierName"],
            "status": "Terminated"
        }   

        return result    

    
               