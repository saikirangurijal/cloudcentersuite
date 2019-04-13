"This method is used to get the details from user and assigning to domain creation json"

import json,os
import re,sys
from util import print_error,print_log,print_result,write_error

try:

    currentworkingdir = os.getcwd()
    filename = os.path.join(currentworkingdir, "createrecordset.json")
    print("filename is :",filename)
    with open(filename, 'r') as file:
         json_data = json.load(file)
         global json_data
         print(json_data)

except IOError as ioerr:
    print_error(ioerr)
    write_error(ioerr)
    sys.exit(127)

try:
    #Getting inputs from user for creaating sub domain and health check from environment variable.
    domainName = os.environ["DomainName"]
    subDomainName = os.environ["subDomainName"]
    IpAddress = os.environ["IpAddress"]
    healthCheckport = os.environ["healthCheckport"]
    healthCheckpath = os.environ["healthCheckpath"]

except Exception as er:
    print_error("Required parameter is missing .")
    print_error(er)
    sys.exit(127)

def create_domain_json():

    json_data["AdminContact"]["FirstName"] = ""
    json_data["AdminContact"]["LastName"] = ""
    json_data["AdminContact"]["ContactType"] = ""
    json_data["AdminContact"]["OrganizationName"] = ""
    json_data["AdminContact"]["AddressLine1"] = ""
    json_data["AdminContact"]["AddressLine2"] = ""
    json_data["AdminContact"]["City"] = ""
    json_data["AdminContact"]["PhoneNumber"] = ""
    json_data["AdminContact"]["State"] = ""
    json_data["AdminContact"]["CountryCode"] = ""
    json_data["AdminContact"]["ZipCode"] = ""
    json_data["AdminContact"]["Email"] = ""
    # json_data["AdminContact"]["FAX"] = ""



    json_data["RegistrantContact"]["FirstName"] = ""
    json_data["RegistrantContact"]["LastName"] = ""
    json_data["RegistrantContact"]["ContactType"] = ""
    json_data["RegistrantContact"]["OrganizationName"] = ""
    json_data["RegistrantContact"]["AddressLine1"] = ""
    json_data["RegistrantContact"]["AddressLine2"] = ""
    json_data["RegistrantContact"]["City"] = ""
    json_data["RegistrantContact"]["PhoneNumber"] = ""
    json_data["RegistrantContact"]["State"] = ""
    json_data["RegistrantContact"]["CountryCode"] = ""
    json_data["RegistrantContact"]["ZipCode"] = ""
    json_data["RegistrantContact"]["Email"] = ""
    # json_data["RegistrantContact"]["FAX"] = ""

    json_data["TechContact"]["FirstName"] = ""
    json_data["TechContact"]["LastName"] = ""
    json_data["TechContact"]["ContactType"] = ""
    json_data["TechContact"]["OrganizationName"] = ""
    json_data["TechContact"]["AddressLine1"] = ""
    json_data["TechContact"]["AddressLine2"] = ""
    json_data["TechContact"]["City"] = ""
    json_data["TechContact"]["PhoneNumber"] = ""
    json_data["TechContact"]["State"] = ""
    json_data["TechContact"]["CountryCode"] = ""
    json_data["TechContact"]["ZipCode"] = ""
    json_data["TechContact"]["Email"] = ""
    # json_data["TechContact"]["FAX"] = ""
    return json_data

def create_record_set_json():
    json_data["Changes"]["Changes"][0]["Action"] = "UPSERT"
    subName = subDomainName+"."+domainName
    print("subDomainName is :",subName)
    json_data["Changes"]["Changes"][0]["ResourceRecordSet"]["Name"] = subName
    json_data["Changes"]["Changes"][0]["ResourceRecordSet"]["TTL"] = 60
    json_data["Changes"]["Changes"][0]["ResourceRecordSet"]["ResourceRecords"][0]["Value"] = IpAddress
    return json_data

def delete_record_set_json():
    json_data["Changes"]["Changes"][0]["Action"] = "DELETE"
    subName = subDomainName+"."+domainName
    print("subDomainName is :", subName)
    json_data["Changes"]["Changes"][0]["ResourceRecordSet"]["Name"] = subName
    json_data["Changes"]["Changes"][0]["ResourceRecordSet"]["TTL"] = 60
    json_data["Changes"]["Changes"][0]["ResourceRecordSet"]["ResourceRecords"][0]["Value"] = IpAddress
    return json_data

def create_healthcheck():
    json_data["HealthCheckConfig"]["IPAddress"]= IpAddress
    print(type(healthCheckport))
    json_data["HealthCheckConfig"]["Port"]= int(healthCheckport)
    json_data["HealthCheckConfig"]["Type"]= "HTTP"
    json_data["HealthCheckConfig"]["FullyQualifiedDomainName"]=subDomainName+"."+domainName
    json_data["HealthCheckConfig"]["ResourcePath"]= healthCheckpath
    # json_data["HealthCheckConfig"]["ResourcePath"] = "/ui/auth/login",
    json_data["HealthCheckConfig"]["RequestInterval"]= 30
    json_data["HealthCheckConfig"]["FailureThreshold"]= 5
    return json_data