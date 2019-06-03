from azure.mgmt.dns import DnsManagementClient
from util import print_error,print_log,print_result
from errorutils import ErrorUtils

import os,sys
import json

try:
    from azure.common.credentials import ServicePrincipalCredentials
except Exception as er:
    print_error("error while installing Azure Sdk")
    print("Error while installing Azure SDK ",er)
    sys.exit(127)

'''
    Azure Management Client
'''

class AzureManagement(object):

    def __init__(self):

        # Initialize Azure Basic Setup

        # self.group_name = params['resourceGroup']
        # self.group_name = "Cisco_External_Service_Test"
        # self.location = params['account']['location']

        # self.subscription_id = params['account']['subscriptionId']
        # self.subscription_id = "cbaba14b-e672-47d7-bb59-4a0613d6d149"
        #
        # self.credentials = ServicePrincipalCredentials(
        #     client_id="a25f5c1c-f407-4d96-ba03-4a97dd58e8c9",
        #     secret="It5rUwpvCJx357nD8iJayazSO38aArK56iAzryRKQCo=",
        #     tenant="71d59dd8-2935-48a4-9185-3c5bd27f6dbd"
        # )

        try:
            print_log("Getting Azure Cloud details...")
            try:
                dependents = os.environ['CliqrDependencies']
                if len(dependents) == 0:
                    print_error("There is no dependent tier")
                    sys.exit(127)

                resourceGroup = os.environ['CliqrTier_' + dependents + "_Cloud_Setting_ResourceGroup"]  # Azure Resource Group
            except Exception as er:
                print("Error while taking resource group ",er)

            client_id = os.environ["CliqrCloud_ClientId"]
            secret = os.environ["CliqrCloud_ClientKey"]
            tenant = os.environ["CliqrCloud_TenantId"]
            subscription_id = os.environ["CliqrCloudAccountId"]

            self.group_name = resourceGroup
            # self.location = params['account']['location']

            # self.subscription_id = params['account']['subscriptionId']
            self.subscription_id = subscription_id

            self.credentials = ServicePrincipalCredentials(
                client_id=client_id,
                secret=secret,
                tenant=tenant
            )
            self.dns_client = DnsManagementClient(self.credentials, self.subscription_id)
            print_log("Azure Connection Succeded")

        except KeyError as kerr:
            print kerr
            print_error(ErrorUtils.mandatory_params_missing(kerr))
            # write_error(kerr)
            sys.exit(127)


    def create_recordSet(self,domainName,subdomainName,ipaddress):
        """
        Function to create record set for the given domainName with Ip address
        :param domainName:
        :param subdomainName:
        :return:
        """

        try:
            print_log("Creating Azure Recordset...")
            record_set = self.dns_client.record_sets.create_or_update(
                self.group_name,
                domainName,
                subdomainName,
                'A',
                {
                    "ttl": 300,
                    "arecords": [
                        {
                            "ipv4_address": ipaddress
                        }
                    ]
                }
            )

            if record_set:
                print_log("Record set created successfully.")

                result = {"hostName": "Azure DNS Zone"}
                result['ipAddress'] = str(subdomainName + '.' + domainName)
                print("Result is :", result)
                print_result(json.dumps(result))
            else:
                print_error("Record set creation Failed.")
                sys.exit(127)
        except Exception as er:
            print_error(er)

    def delete_recordset(self,domainName,subdomainName):
        """
        Functio to Delete record set from given domain Name
        :param domainName:
        :param subdomainName:
        :return:
        """
        try:
            print_log("Deleting Record set ...")
            delete_recordset = self.dns_client.record_sets.delete(self.group_name,domainName,subdomainName,'A',)
            if delete_recordset:

                print_log("Record set deleted successfully.")
        except Exception as er:
            print("Error while deleting record set")
            print_error("Error while Deleting record set")
            sys.exit(127)


def main(command):
    """

    :param command:
    :return:
    """
    try:
        print_log("Acessing cloud account details and connecting.")
        try:
            domainName = os.environ["DomainName"]
            subdominName = os.environ["SubdomainName"]
            dependents = os.environ.get('CliqrDependencies', "")
            if os.environ["IpAddress"]:
                IpAddress = os.environ["IpAddress"]
            else:
                if len(dependents) > 0:
                    IpAddress = str(os.environ['CliqrTier_' + dependents + '_PUBLIC_IP'])
                    print("my instances Ip address is : ===================>{}".format(IpAddress))
        except :
            print_log("DomainName is not given properlly")
            sys.exit(127)

        if command in "start":
            object = AzureManagement()
            object.create_recordSet(domainName,subdominName,IpAddress)

        elif command in "stop":
            object = AzureManagement()
            object.delete_recordset(domainName,subdominName)

    except Exception as er:
        print_error(er)
        sys.exit(127)
