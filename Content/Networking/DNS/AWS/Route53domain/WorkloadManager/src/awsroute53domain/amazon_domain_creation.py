import boto3
import sys,os,json,time
from util import print_error,print_log,print_result,write_error


class awsroute53domain():

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
                print_log(e)
                sys.exit(127)
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

    def registerDomain(self,domainName):
        """
        Register domainName once the DomainName is Available.
        :return:
        """
        try:
            if self.checkingDomaninAvailability(domainName):
                from prerequiste_environments import create_domain_json
                data = create_domain_json()
        except Exception as er:
            print_log(er)
            print("Error while parsing json file is :",er)
            sys.exit(127)
        try:

            print_log(" Starting Domain Registration.")
            AdminContact_data = data["AdminContact"]
            RegistrantContact_data = data["RegistrantContact"]
            TechContact_data = data["TechContact"]

            print("AdminContact_data is :",AdminContact_data)
            print("RegistrantContact_data is :",RegistrantContact_data)
            print("TechContact_data is :",TechContact_data)

            response = self.client.register_domain(
                DomainName=domainName,
                DurationInYears=1,
                AutoRenew=True,
                AdminContact=AdminContact_data,
                RegistrantContact=RegistrantContact_data,
                TechContact=TechContact_data,
                PrivacyProtectAdminContact=True,
                PrivacyProtectRegistrantContact=False,
                PrivacyProtectTechContact=False
            )
            print(response)
            # self.operation_id = response["OperationId"]
            print_log("Domain Creation request Submitted Successfully...please wait for 10 minutes for getting success")

        except Exception as err:
            print(err)
            print_error(err)
            sys.exit(127)


def main(command):
    DomainName = os.environ["DomainName"]
    if command in "start":
        object = awsroute53domain()
        object.checkingDomaninAvailability(DomainName)
        object.registerDomain(DomainName)

    elif command in "stop":
        object = awsroute53domain()
        # object.get_hosted_zones("qwertyuioptest12345.com")
        # object.delete_record_set()
        # object.delete_hosted_zone("qwertyuioptest12345.com")
        # # object.list_resource_record_set("qwertyuioptest12345.com")
        # object.delete_health_check("route53healthchecktest90")