#!/usr/bin/env python

import json,sys
from util import print_error, print_log, print_result


def deunicodify_hook(pairs):
    new_pairs = []
    for key, value in pairs:
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        new_pairs.append((key, value))
    return dict(new_pairs)

def construct_fip_id(subscription_id, group_name, lb_name, fip_name):
    """Build the future FrontEndId based on components name.
    """
    return ('/subscriptions/{}'
            '/resourceGroups/{}'
            '/providers/Microsoft.Network'
            '/loadBalancers/{}'
            '/frontendIPConfigurations/{}').format(
                subscription_id, group_name, lb_name, fip_name
            )

def construct_bap_id(subscription_id, group_name, lb_name, address_pool_name):
    """Build the future BackEndId based on components name.
    """
    return ('/subscriptions/{}'
            '/resourceGroups/{}'
            '/providers/Microsoft.Network'
            '/loadBalancers/{}'
            '/backendAddressPools/{}').format(
                subscription_id, group_name, lb_name, address_pool_name
            )

def construct_probe_id(subscription_id, group_name, lb_name, probe_name):
    """Build the future ProbeId based on components name.
    """
    return ('/subscriptions/{}'
            '/resourceGroups/{}'
            '/providers/Microsoft.Network'
            '/loadBalancers/{}'
            '/probes/{}').format(
                subscription_id, group_name, lb_name, probe_name
            )         

def update_nic_paramaters(address_pool_id, location, nic_info, params):
    """Update the NIC parameters structure.
    """
    nic_params = params['nicParams']
    nic_params['location'] = location
    nic_params['ip_configurations'][0]['name'] = nic_info.ip_configurations[0].name
    nic_params['ip_configurations'][0]['subnet']['id'] = nic_info.ip_configurations[0].subnet.id
    nic_params['ip_configurations'][0]['load_balancer_backend_address_pools'] = [{
        "id": address_pool_id
    }]

    return nic_params

    #nic_params['ip_configurations'][0]['load_balancer_inbound_nat_rules'][0]['id'] = natrule_id

def create_vm_parameters(nic_id, is_nic_primary, location, vm_info, params):
    """Create the VM parameters structure.
    """
    vm_params = params['vmParams']
    vm_params['location'] = location
    vm_params['network_profile']['network_interfaces'][0]['id'] = nic_id
    vm_params['network_profile']['network_interfaces'][0]['primary'] = is_nic_primary
    return vm_params     

def get_error_messages():
    messages = {}
    try:
        with open('error_messages.json', 'r') as file:
            messages = json.loads(str(file.read()), object_pairs_hook=deunicodify_hook)
    except Exception as err:
        print_error('failed to load parmaters json!')
        sys.exit(127)

    return messages

def generate_params_error_message(parameters, error_message):
    reason = ""
    if isinstance(parameters, list):
        reason = ','.join(parameters)
    else:
        reason = parameters

    reason += " ," + error_message
    return reason


def write_log(err):
    f = open('FAILURE','w')
    f.write(str(err))
    f.close()

def error_messages():
    global error_messages
    error_messages = get_error_messages()

error_messages()