"This method is used to get the details from user and assigning to domain creation json"

import json,os
import re,sys
from util import print_error,print_log,print_result,write_error

try:

    currentworkingdir = os.getcwd()
    filename = os.path.join(currentworkingdir, "domaincreation.json")
    print("filename is :",filename)
    with open(filename, 'r') as file:
         json_data = json.load(file)
         global json_data
         print(json_data)

except IOError as ioerr:
    print_error(ioerr)
    write_error(ioerr)
    sys.exit(127)


def create_domain_json():

    json_data["AdminContact"]["FirstName"] = os.environ["FirstName"]
    json_data["AdminContact"]["LastName"] = os.environ["LastName"]
    json_data["AdminContact"]["ContactType"] = os.environ["ContactType"]
    json_data["AdminContact"]["OrganizationName"] = os.environ["Organization"]
    json_data["AdminContact"]["AddressLine1"] = os.environ["AddressLine1"]
    json_data["AdminContact"]["AddressLine2"] = os.environ["AddressLine2"]
    json_data["AdminContact"]["City"] = os.environ["City"]
    phoneNumber = os.environ["PhoneNumber"]
    try:
        if phoneNumber:
            rule = re.compile(r'(^[+0-9]{1,3}).([0-9]{5,10}$)')

            if rule.search(phoneNumber):
                print("Mobile Number is valid")

            else:
                print("Mobile Number is not valid please mention like <+12>.<123456789> based on country code.")
                print_error("Mobile Number is not valid please mention like <+12>.<123456789> based on country code.")
                sys.exit(127)
    except Exception as er:
        print(er)
    json_data["AdminContact"]["PhoneNumber"] = phoneNumber
    json_data["AdminContact"]["State"] = os.environ["StateCode"]
    json_data["AdminContact"]["CountryCode"] = os.environ["CountryCode"]
    json_data["AdminContact"]["ZipCode"] = os.environ["zipcode"]
    json_data["AdminContact"]["Email"] = os.environ["Email"]
    # json_data["AdminContact"]["FAX"] = ""

    json_data["RegistrantContact"]["FirstName"] = os.environ["FirstName"]
    json_data["RegistrantContact"]["LastName"] = os.environ["LastName"]
    json_data["RegistrantContact"]["ContactType"] = os.environ["ContactType"]
    json_data["RegistrantContact"]["OrganizationName"] = os.environ["Organization"]
    json_data["RegistrantContact"]["AddressLine1"] = os.environ["AddressLine1"]
    json_data["RegistrantContact"]["AddressLine2"] = os.environ["AddressLine2"]
    json_data["RegistrantContact"]["City"] = os.environ["City"]
    json_data["RegistrantContact"]["PhoneNumber"] = phoneNumber
    json_data["RegistrantContact"]["State"] = os.environ["StateCode"]
    json_data["RegistrantContact"]["CountryCode"] = os.environ["CountryCode"]
    json_data["RegistrantContact"]["ZipCode"] = os.environ["zipcode"]
    json_data["RegistrantContact"]["Email"] = os.environ["Email"]
    # json_data["RegistrantContact"]["FAX"] = ""

    json_data["TechContact"]["FirstName"] = os.environ["FirstName"]
    json_data["TechContact"]["LastName"] = os.environ["LastName"]
    json_data["TechContact"]["ContactType"] = os.environ["ContactType"]
    json_data["TechContact"]["OrganizationName"] = os.environ["Organization"]
    json_data["TechContact"]["AddressLine1"] = os.environ["AddressLine1"]
    json_data["TechContact"]["AddressLine2"] = os.environ["AddressLine2"]
    json_data["TechContact"]["City"] = os.environ["City"]
    json_data["TechContact"]["PhoneNumber"] = phoneNumber
    json_data["TechContact"]["State"] = os.environ["StateCode"]
    json_data["TechContact"]["CountryCode"] = os.environ["CountryCode"]
    json_data["TechContact"]["ZipCode"] = os.environ["zipcode"]
    json_data["TechContact"]["Email"] = os.environ["Email"]
    # json_data["TechContact"]["FAX"] = ""
    return json_data
