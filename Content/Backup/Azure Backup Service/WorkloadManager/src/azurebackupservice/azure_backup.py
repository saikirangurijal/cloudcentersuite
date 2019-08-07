import requests
import json
import os
import sys
from util import *

def  get_accesstoken(tenantid, client_id, client_secret):
    '''GET access token for Authorization'''
    endpoint = "https://login.microsoftonline.com/{}/oauth2/token".format(tenantid)
    resource ="https://management.azure.com/"
    grant_type = "client_credentials"
    payload = {"client_id": client_id, "client_secret":client_secret,
               "resource":resource, "grant_type":grant_type}
    response = requests.post(url= endpoint, data=payload)
    json_resp = response.json()
    if response.status_code == 200:
        return json_resp["access_token"]
    else:
        print_log("No Access token")
        sys.exit(127)

def enable_backup_policy(subscription_id,resource_group,vaultname, policyname,
                         fabric_name, containerName, protectedItemName, tenantid,
                         vm_id, policy_id, client_id, client_secret):
    '''Enabling Backup policy for Virtual Machine'''
    endpoint = "https://management.azure.com/Subscriptions/{}/resourceGroups/{}/" \
               "providers/Microsoft.RecoveryServices/vaults/{}/backupFabrics/{}/" \
               "protectionContainers/{}/protectedItems/{}" \
               "?api-version=2016-12-01".format(subscription_id, resource_group,
                                                vaultname,fabric_name,containerName,protectedItemName)
    payload = { "properties": {"protectedItemType": "Microsoft.Compute/virtualMachines",
                               "sourceResourceId": vm_id,
                               "policyId": policy_id
                               }
                }
    access_token = get_accesstoken(tenantid, client_id, client_secret)
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}
    response = requests.put(url=endpoint, data=json.dumps(payload), headers=headers)
    print_log(response.status_code)
    if response.status_code == 200 or response.status_code == 202:
        enable_endpoint = response.headers['Location']
        enable_api = requests.get(url=enable_endpoint, headers=headers)
        print_log(enable_api.status_code)
        if enable_api.status_code == 200 or enable_api.status_code == 202:
            print_log("Enabling backupolicy for VM Success")
    else:
        print_log("Enabling Backup policy API failed")
        sys.exit(127)

def list_unprotectvm(subscription_id,resource_group, vaultname,
                      policyname,fabric_name, tenantid,
                     vmname, policy_id, client_id, client_secret):
    '''Listing Unpeotected VMs for region'''
    access_token = get_accesstoken(tenantid, client_id, client_secret)
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}
    endpoint = "https://management.azure.com/Subscriptions/{}/" \
               "resourceGroups/{}/providers/Microsoft.RecoveryServices/vaults/" \
               "{}/backupProtectableItems?api-version=2016-12-01&$filter=backupManagementType " \
               "eq 'AzureIaasVM'".format(subscription_id, resource_group, vaultname)
    res = requests.get(url=endpoint, headers=headers)
    vm_list = res.json()
    vm_exists = 0
    if vm_list['value']:
        for i in vm_list['value']:
            if i['properties']['friendlyName'] == vmname:
                vm_exists = 1 
                containerName = "iaasvmcontainer;" + i['name']
                protectedItemName = "vm;" + i['name']
                vm_id = i['properties']["virtualMachineId"]
                print_log(containerName)
                print_log(protectedItemName)
                print_log(vm_id)
                os.environ["containerName"] = containerName
                os.environ["protectedItemName"] = protectedItemName
                app_tier_name = os.environ['cliqrAppTierName']
                json_result = {
                    "hostName": app_tier_name,
                    "ipAddress": "",
                    "environment": {
                        "containerName": containerName,
                        "protectedItemName": protectedItemName
                    }
                }
                print_result(json.dumps(json_result))
                enable_backup_policy(subscription_id, resource_group, vaultname, policyname
                                     , "Azure", containerName, protectedItemName, tenantid,
                                     vm_id, policy_id, client_id, client_secret)
        if(vm_exists == 0):
            print_log("The VM may not be exist or in some other region")
            sys.exit(127)
    else:
        print_log("No unprotected vms for this region")
        sys.exit(127)


def refresh_vm(subscription_id,resource_group, vaultname,
                      policyname,tenantid, fabric_name, vmname, policy_id, client_id, client_secret):
    '''Refresh VM'''
    endpoint = "https://management.azure.com/Subscriptions/{}/resourceGroups/" \
               "{}/providers/Microsoft.RecoveryServices/vaults/{}" \
               "/backupFabrics/{}/" \
               "refreshContainers?api-version=2016-12-01".format(subscription_id, resource_group, vaultname, fabric_name)
    access_token = get_accesstoken(tenantid, client_id, client_secret)
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}
    res = requests.post(url=endpoint, headers=headers)
    if res.status_code == 202:
        refresh_endpoint = res.headers['Location']
        refreshvm = requests.get(url=refresh_endpoint, headers=headers)
        print_log("Refresh VM API success")
        list_unprotectvm(subscription_id,resource_group, vaultname,
                         policyname, fabric_name, tenantid, vmname, policy_id, client_id, client_secret)
    else:
        print_log("Error in refresh vm api")
        sys.exit(127)

def create_backup_policy(subscription_id,
                         resource_group, vaultname,
                         policyname,tenantid, vmname, client_id, client_secret):
    '''Creating Backup policy'''
    backuppolicy_exists = "https://management.azure.com/Subscriptions/{}/resourceGroups/{}/" \
                          "providers/Microsoft.RecoveryServices/vaults/{}/" \
                          "backupPolicies?api-version=2017-07-01&" \
                          "$filter=backupManagementType eq 'AzureIaasVM'".format(subscription_id,
                                                                                 resource_group, vaultname)
    access_token = get_accesstoken(tenantid, client_id, client_secret)
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}
    response = requests.get(url=backuppolicy_exists, headers=headers)
    listpolicy = response.json()
    policy_exists = "false"
    for i in listpolicy['value']:
        if i["name"] == policyname and policyname == "DefaultPolicy":
            policy_exists = "true"
            policy_id = i["id"]
            refresh_vm(subscription_id, resource_group, vaultname, policyname, tenantid,
                       "Azure", vmname, policy_id, client_id, client_secret)
        elif i["name"] == policyname:
			policy_exists = "true"
            policy_id = i["id"]
            refresh_vm(subscription_id, resource_group, vaultname, policyname, tenantid,
                       "Azure", vmname, policy_id, client_id, client_secret)
        else:
            print_log("policy not exists")

def create_recovery_vault(subscription_id, resource_group, vaultname, tenantid,
                          location, policyname, vmname, client_id, client_secret):
    '''Creating Recovery Service Vault'''
    recovery_exists = "https://management.azure.com/subscriptions/{}/resourceGroups/{}/" \
                      "providers/Microsoft.RecoveryServices/vaults?" \
                      "api-version=2016-06-01".format(subscription_id, resource_group)
    access_token = get_accesstoken(tenantid, client_id, client_secret)
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}
    response = requests.get(url=recovery_exists, headers=headers)
    listvault = response.json()
    vault_exists = "false"
    for i in listvault['value']:
        if i["name"] == vaultname:
            vault_exists = "true"
            print_log("Vault exists")
            create_backup_policy(subscription_id, resource_group, vaultname,
                                 policyname, tenantid, vmname, client_id, client_secret)
    if vault_exists == "false":
        endpoint = "https://management.azure.com/subscriptions/{}/resourceGroups/{}/" \
                   "providers/Microsoft.RecoveryServices/vaults/{}?" \
                   "api-version=2016-06-01".format(subscription_id, resource_group, vaultname)
        payload = {"properties": {},"sku": {"name": "Standard"},"location": "West US"}
        access_token = get_accesstoken(tenantid, client_id, client_secret)
        headers = {"Content-Type":"application/json", "Authorization":"Bearer " + access_token}
        response = requests.put(url=endpoint, data=json.dumps(payload), headers = headers)
        if response.status_code == 200 or response.status_code == 201:
            print_log("Vault created")
            create_backup_policy(subscription_id,resource_group, vaultname,
                                 policyname,tenantid, vmname, client_id, client_secret)
        else:
            print_log("Vault not created")
            sys.exit(127)

def deletebackup(subscription_id, resource_group, vaultname, tenantid,
                 location, policyname, vmname, client_id, client_secret):
    '''Deleting backup items, backuppolicy and RecoveryServicevault'''
    containerName = os.environ.get("containerName", None)
    protectedItemName = os.environ.get("protectedItemName", None)
    print_log(containerName)
    print_log(protectedItemName)
    if containerName != None and protectedItemName != None:
        deletebcdata= "https://management.azure.com/subscriptions/{}/resourceGroups/{}/" \
                  "providers/Microsoft.RecoveryServices/vaults/{}/backupFabrics/" \
                  "Azure/protectionContainers/{}/protectedItems/" \
                  "{}?api-version=2017-07-01".format(subscription_id, resource_group,
                                                     vaultname, containerName, protectedItemName)
        access_token = get_accesstoken(tenantid, client_id, client_secret)
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}
        response = requests.delete(url=deletebcdata, headers=headers)
        print_log(response.status_code)
        time.sleep(200)
        print_log("Backup items deleted")
    access_token = get_accesstoken(tenantid, client_id, client_secret)
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}
    delrecovervault = "https://management.azure.com/subscriptions/{}/resourceGroups/" \
                      "{}/providers/Microsoft.RecoveryServices/vaults/" \
                      "{}?api-version=2016-06-01".format(subscription_id, resource_group, vaultname)
    response = requests.delete(url=delrecovervault, headers=headers)
    if response.status_code == 200:
        print_log("Recovery Vault Deleted")

