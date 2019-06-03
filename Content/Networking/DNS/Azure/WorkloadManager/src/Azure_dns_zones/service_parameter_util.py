#!/usr/bin/env python

import json
import os
import sys
from util import *
from error_utils import ErrorUtils

# Azure Account Parameters
account_params = {
    'CliqrCloudAccountId': "subscriptionId",
    'CliqrCloud_ClientId': "clientId",
    'CliqrCloud_ClientKey': "clientSecret",
    'CliqrCloud_TenantId': "tenantId",
    'region': "location"
}

# ELB Requrired Parameters
mandatory_params = [
    "CliqrCloudAccountId",
    "CliqrCloud_ClientId",
    "CliqrCloud_ClientKey",
    "CliqrCloud_TenantId",
    "region",
    "resourceGroupName",
    "loadBalancerName",
    "lbType",
    "publicIpName",
    "healthProbeRequestPath",
    "healthProbePort"
]

# Open Parameter Template and filling values
try:
    with open('params.json', 'r') as file:
        global params
        params = json.loads(file.read())
except IOError as ioerr:
    print_err(ErrorUtils.bundle_error(ioerr))
    write_error(ioerr)

    sys.exit(127)
except Exception as err:
    print_error(ErrorUtils.internal_error(err.message))
    write_error(err)
    sys.exit(127)


# Create Parameters JSON using Template
def create_params_json():
    # Account params
    try:
        params['appTierName'] = os.environ.get("cliqrAppTierName", "")

        for k, v in account_params.items():
            params['account'][v] = os.environ[k]
    except KeyError as kerr:
        print kerr
        print_error(ErrorUtils.mandatory_params_missing(kerr), kerr.message)
        write_error(kerr)

        sys.exit(127)

        return False
    except Exception as err:
        print_error(ErrorUtils.internal_error(err))
        write_error(err)

        sys.exit(127)

        return False

    # Mandatory params
    try:
        dependents = os.environ['CliqrDependencies']
        if len(dependents) == 0:
            print_error("There is no dependent tier")
            sys.exit(127)

        params['resourceGroup'] = os.environ['CliqrTier_' + dependents + "_Cloud_Setting_ResourceGroup"]  # Azure Resource Group
        params['loadBalancer']['name'] = os.environ['loadBalancerName']  # Unique Load Balancer Name
        params['loadBalancer']['type'] = os.environ['lbType']  # Load Balancer Type
        params['publicIp']['name'] = os.environ['loadBalancerName'] + "_public_ip"

        params['publicIp']['createNew'] = True

        # Get All Virtual Machines name and resource group name associated with load balancer tier
        if len(dependents) > 0:
            _vms = str(os.environ['CliqrTier_' + dependents + '_HOSTNAME']).split(',')
            params['vmResourceGroup'] = str(os.environ['CliqrTier_' + dependents + '_Cloud_Setting_ResourceGroup'])

        env_vnet = str(os.environ['CliqrTier_' + dependents + "_Cloud_Setting_VirtualNetwork"]).split(" ")
        params['vnet'] = env_vnet[1]
        env_subnet = "CliqrTier_" + dependents + "_Cloud_Setting_subnetId"
        params['subnet'] = str(os.environ.get(env_subnet, 'default'))

        vms = params['vms']
        for vm in _vms:
            vm_params = dict(params['vmAttr'])
            vm_params['name'] = vm.strip()

            vms.append(vm_params)

        # Get all service and deployment parameters
        params['loadBalancer']['checkHealthProbe'] = True
        health_probe_params = params['loadBalancer']['healthProbeAttr']
        health_probe_params['protocol'] = os.environ['healthCheckProtocol']
        health_probe_params['request_path'] = os.environ['healthProbeRequestPath']
        health_probe_params['port'] = os.environ['healthProbePort']
        health_probe_params['interval_in_seconds'] = os.environ['healthCheckInterval']
        health_probe_params['number_of_probes'] = os.environ['unhealthThreshold']

        if os.environ['healthCheckProtocol'] in 'TCP':
            del health_probe_params['request_path']

        params['loadBalancer']['healthProbes'].append(health_probe_params)

    except KeyError as kerr:
        print kerr
        print_error(ErrorUtils.mandatory_params_missing(kerr))
        write_error(kerr)
        sys.exit(127)

        return False
    except Exception as err:
        print_error(ErrorUtils.internal_error(err))
        write_error(err)

        sys.exit(127)

        return False

    # Load balancer rules
    _lb_rules = []
    try:
        _load_balancer_rules = json.loads(os.environ['loadBalancerRules'])
        if isinstance(_load_balancer_rules, list):
            _lb_rules = _load_balancer_rules
        else:
            _lb_rules_count = int(os.environ['loadBalancerRules'])
            for i in range(0, _lb_rules_count):
                _lb_rules.append([os.environ['loadBalancerRules_loadBalancerProtocol_' + str(i)],
                                  os.environ['loadBalancerRules_frontEndPort_' + str(i)],
                                  os.environ['loadBalancerRules_backEndPort_' + str(i)],
                                  os.environ['loadBalancerRules_idleTimeout_' + str(i)]])
    except Exception as err:
        print_log(err)
        print_log("Invalid Rules format")

    rules = params['loadBalancer']['rules']
    print _lb_rules
    for _rule in _lb_rules:
        rule = dict(params['loadBalancer']['rulesAttr'])
        rule["protocol"] = _rule[0]
        rule["frontend_port"] = _rule[1]
        rule["backend_port"] = _rule[2]
        rule["idle_timeout_in_minutes"] = _rule[3]

        rules.append(rule)

    front_end_configs = params['loadBalancer']['frontEndIp']
    front_end_params = params['loadBalancer']['frontEndIpAttr']
    front_end_configs.append(front_end_params)

    backend_pools = params['loadBalancer']['backEndPools']
    backend_pools.append(params['loadBalancer']['backEndPoolAttr'])

    # Write All parameters with value in params template file
    with open('params.json', 'w') as file:
        file.write(json.dumps(params))

    print_log("Updating Configuration")

    return True