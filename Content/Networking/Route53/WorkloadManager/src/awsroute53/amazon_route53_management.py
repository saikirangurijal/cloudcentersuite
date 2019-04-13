import boto3
import sys,os,json,time
from util import print_error,print_log,print_result,write_error


class route53management():

    def __init__(self):
        """
        Initiallization for AWS clous access using AccessKey ,SecretaKey and RegionName.
        """

        try:

            CliqrCloudAccountPwd = os.environ["CliqrCloudAccountPwd"]
            # CliqrCloudAccountId = os.environ["CliqrCloudAccountId"]
            CliqrCloud_AccessSecretKey = os.environ["CliqrCloud_AccessSecretKey"]
            RegionName = os.environ["region"]

            self.client = boto3.client('route53domains', aws_access_key_id=CliqrCloudAccountPwd,
                                  aws_secret_access_key=CliqrCloud_AccessSecretKey,
                                  region_name=RegionName)

            self.client_route53 = boto3.client('route53', aws_access_key_id=CliqrCloudAccountPwd,
                                       aws_secret_access_key=CliqrCloud_AccessSecretKey,
                                       region_name=RegionName)

            print("AWS Connection Succeded.")
            print_log("AWS Connection Succeded.")

        except Exception as err:
            print(err)
            print_error(err)
            sys.exit(127)


    def checkingDomaninAvailability(self,domainName):
        """
        method to check the availability of DomainName and returning the status of domain
        :param domainName:
        :return:
        """

        try:
            print_log("Checking Given DomainName are Available ...")
            try:
                response = self.client.check_domain_availability(DomainName=domainName)
            except Exception as e:
                print("im in except")
                print(e)
            if response["Availability"] == "AVAILABLE":
                print("Given DomainName {} is Available".format(domainName))
                return True
            else:
                print("Given domainName {} is not available".format(domainName))
                print_log("Given domainName {0} is not available and status is {1}".format(domainName,response["Availability"]))
                print_error("Given domainName {0} is not available and status is {1}".format(domainName,response["Availability"]))
                sys.exit(127)
        except Exception as er:
            print(er)
            print_error(er)
            sys.exit(127)


    def domain_status(self,domainName):
        """
        To Verify the domain status whether this available
        :param domainName:
        :return:
        """
        try:

            print_log("Checking Given Domain is available in AWS RegisteredDomain...")
            response = self.client.get_domain_detail(
                DomainName=domainName
            )
            if response["DomainName"] in domainName:
                print_log("Given Domain Name {} is Available".format(domainName))
            else:
                print_log("Given DomainName is not there please mention exisiting Domain Name.")
                sys.exit(127)
            return True

        except Exception as e:
            print(e)
            print_error(e)
            sys.exit(127)

    def get_hosted_zones(self,domainName):
        """
        Getting hosted zone id through the domainName.
        :param domainName:
        :return:
        """
        try:

            print_log("Getting hosted zoneId using Registered DomainName.")
            response = self.client_route53.list_hosted_zones_by_name(DNSName=domainName)
            datam = response["HostedZones"]
            for data in datam:
                print(data)
                if data["Name"] in domainName+'.':
                    self.dns_id = data['Id'].split('/')[-1]
                    print("Hosted zone id for doamin name {} and its id {} is: ".format(domainName,self.dns_id))
                    break
            print_log("Getting Hosted zoneId Successfull")
            return self.dns_id
        except Exception as er:
            print(er)


    def delete_hosted_zone(self,domainName):
        """
        Deleting hosted zone using hosted zone id.
        :param domainName
        :return:
        """
        try:
            dns_id = self.get_hosted_zones(domainName)
            response = self.client_route53.delete_hosted_zone(
                Id=dns_id
            )
            print("Response for deleting hosted zone is:",response)
        except Exception as e:
            print(e)
            sys.exit(127)

    def create_record_set(self,healthCheckName):
        """
        Creating record set for the Given domainName and assigning webserver/Elastic load balancer etc,.
        :return:
        """
        try:
            print_log("Creating Record set for the Given Domain...")
            from prerequiste_environments import create_record_set_json
            recordSet_json = create_record_set_json()
            healthcheckid = self.list_healthcheck(healthCheckName)
            recordSet_json["Changes"]["Changes"][0]["ResourceRecordSet"]["HealthCheckId"] = healthcheckid
            changes = recordSet_json["Changes"]
            print("record set payload is :",changes)
            response = self.client_route53.change_resource_record_sets(
                HostedZoneId=self.dns_id,
                ChangeBatch=changes
            )
            print(response)
            print_log("Created record set successfully.")
            domainName = os.environ["DomainName"]
            subDomainName = os.environ["subDomainName"]
            print_log("Access your Application from this {}".format(subDomainName+'.'+domainName))
        except Exception as er:
            print_error(er)
            sys.exit(127)

    def delete_record_set(self,healthCheckName):
        """
        Deleting recordset using given input
        :return:
        """
        try:
            from prerequiste_environments import delete_record_set_json
            recordSet_json = delete_record_set_json()
            healthcheckid = self.list_healthcheck(healthCheckName)
            recordSet_json["Changes"]["Changes"][0]["ResourceRecordSet"]["HealthCheckId"] = healthcheckid
            changes = recordSet_json["Changes"]
            print("record set payload is :", changes)
            response = self.client_route53.change_resource_record_sets(
                HostedZoneId=self.dns_id,
                ChangeBatch=changes
            )
            print("Response for delete record set is :",response)
            delete_request_id = response["ChangeInfo"]["Id"].split('/')[-1]
        except Exception as error:
            print_error(error)
            sys.exit(127)


    def create_healthchech(self,healthCheckName):
        """
        Creating health check for the given application Ip or DNS.
        :return:
        """

        try:
            print_log("Creating Healthcheck given application Ip address")
            from prerequiste_environments import create_healthcheck
            recordSet_json = create_healthcheck()
            healthCheckconf = recordSet_json["HealthCheckConfig"]
            response = self.client_route53.create_health_check(
                CallerReference=healthCheckName,
                HealthCheckConfig=healthCheckconf
            )
            time.sleep(10)
            print(response)
            print_log("Health check created successfully.")

        except Exception as err:
            print(err)
            print_error(err)
            sys.exit(127)

    def list_healthcheck(self,callReferenceHealthCheck):
        """
        listing all healh check available in the aws cloud platform
        Checking weather given healthcheck is avail or not ,if it is getting health checj id for
        given healthcheck reference.
        :param callReferenceHealthCheck:
        :return:
        """
        try:

            response = self.client_route53.list_health_checks()
            print("healthcheck is",response)
            for data in response["HealthChecks"]:
                if data["CallerReference"] in callReferenceHealthCheck:
                    healthcheckId = data["Id"]
                    print("HealthCheckId is :",healthcheckId)
                    break
            return healthcheckId

        except Exception as er:
            print_error(er)
            sys.exit(127)

    def delete_health_check(self,callReferenceHealthCheck):
        """
        Deleting Health check which is created by input and thriugh healthcheck id.
        :param callReferenceHealthCheck:
        :return:
        """
        try:
            healthCheckId = self.list_healthcheck(callReferenceHealthCheck)
            response = self.client_route53.delete_health_check(
                HealthCheckId=healthCheckId
            )
            print("Response for deleting healthcheck is :",response)

        except Exception as e:
            print_error(e)
            sys.exit(127)

def main(command):
    """

    :param command:
    :return:
    """
    try:
        try:
            domainName = os.environ["DomainName"]
            healthCheckName = os.environ["healthCheckName"]
        except :
            print_log("DomainName or healthCheck Name is not given properlly")
            sys.exit(127)

        if command in "start":
            object = route53management()
            domainstatus = object.domain_status(domainName)
            object.get_hosted_zones(domainName)
            if domainstatus:
                object.create_healthchech(healthCheckName)
                object.list_healthcheck(healthCheckName)
                object.create_record_set(healthCheckName)

        elif command in "stop":
            object = route53management()
            object.get_hosted_zones(domainName)
            object.delete_record_set(healthCheckName)
            object.delete_hosted_zone(domainName)
            object.delete_health_check(healthCheckName)
    except Exception as er:
        print_error(er)
        sys.exit(127)
