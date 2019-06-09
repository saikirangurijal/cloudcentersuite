from google.cloud import dns
from google.cloud.exceptions import NotFound
import time
from util import *
import os
from error_utils import ErrorUtils
import sys
from google.oauth2 import service_account

class GoogleDNSClient(object):
    def __init__(self, project_id, service_account_json):
        credentials = service_account.Credentials.from_service_account_info(service_account_json)

        self.client = dns.Client(project=project_id, credentials=credentials)

    # Create Zone
    def create_zone(self, name, dns_name, description):
        zone = self.client.zone(
            name,  
            dns_name,
            description=description)
        zone.create()
        return zone

    # Get Zone
    def get_zone(self, name):
        zone = self.client.zone(name=name)

        try:
            zone.reload()
            return zone
        except NotFound:
            return None

    # List zones
    def list_zones(self):
        zones = self.client.list_zones()
        return [zone.name for zone in zones]

    # Delete zone
    def delete_zone(self, name):
        zone = self.client.zone(name)
        zone.delete()

    # List resource records
    def list_resource_records(self, zone_name):
        zone = self.client.zone(zone_name)

        records = zone.list_resource_record_sets()

        return [(record.name, record.record_type, record.ttl, record.rrdatas)
                for record in records]

    # List changes
    def list_changes(self, zone_name):
        zone = self.client.zone(zone_name)

        changes = zone.list_changes()

        return [(change.started, change.status) for change in changes]

    def create(self):
        zone_name = os.environ["subDomainName"]
        name = os.environ["subDomainName"]
        description = "DNS"

        domain = os.environ["domainName"] + "."
        if self.get_zone(name):
            print "exist"
            print_error(ErrorUtils.api_error("ResourceAlreadyExists", "", name=name))
            sys.exit(127)

        zone = self.create_zone(name, domain, description)

        ip_address = os.environ.get("ipAddress", False)

        app_tier_name = os.environ.get("CliqrDependencies", False)
        if not ip_address:
            if not app_tier_name:
                print_error(ErrorUtils.mandatory_params_missing("PublicIPAddress"), "PublicIPAddress")
                sys.exit(127)

            ip_address = os.environ.get('CliqrTier_' + app_tier_name + '_IP', False)
            if not ip_address:
                print_error(ErrorUtils.mandatory_params_missing("PublicIPAddress"), "PublicIPAddress")
                sys.exit(127)

        TWO_HOURS = 2 * 60 * 60  # seconds
        record_set = zone.resource_record_set(name + "." + domain, 'A', TWO_HOURS, ip_address)
        changes = zone.changes()
        changes.add_record_set(record_set)
        changes.create()  # API request
        while changes.status != 'done':
            print_log('Waiting for changes to complete')
            time.sleep(60)     # or whatever interval is appropriate
            changes.reload()

        print_log("Record Set created")
        print_log("Please update all below name servers into your registerd domain server.")
        records = zone.list_resource_record_sets()
        for record in records:
            if record.record_type in 'NS':
                log = '''{0}
{1}
{2}
{3}'''
                print_log(log.format(*record.rrdatas))


        print_log("Please wait until your subdomain got up, please ensure domain registrar got updated with all name servers.")
        sub_domain = name + "." + domain
        result = {
            "hostName":"Google DNS Zone",
            "ipAddress": str(sub_domain)
        }

        return result

    def delete(self):
        zone_name = os.environ["subDomainName"]
        zone = self.get_zone(zone_name)
        records = zone.list_resource_record_sets()

        changes = zone.changes()
        for record in records:
            if record.record_type not in ['NS', 'SOA']:
                changes.delete_record_set(record)
                changes.create()  # API request
        
        while changes.status != 'done':
            print_log('Waiting for changes to complete')
            time.sleep(60)     # or whatever interval is appropriate
            changes.reload()

        zone.delete()
        print_log("Record Set and Zone deleted")

        app_tier_name = os.environ.get("cliqrAppTierName", False)
        result = {
            "hostName":app_tier_name,
            "status": "Terminated"
        }
        
        return result