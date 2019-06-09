#!/usr/bin/env python

# External Life Cycle Action Invocation

from google_dns_client import GoogleDNSClient
import sys
from util import *
from error_utils import ErrorUtils
import json
import os

cmd = sys.argv[1]
# Create Google Management Object with credentials
try:
    project_id = os.environ.get("Cloud_Setting_projectName", False)
    
    service_account_str = str(os.environ['CliqrCloud_JsonServiceAccount']).replace('\n', '')
    service_account_json = json.loads(service_account_str)

    google_dns_client = GoogleDNSClient(project_id, service_account_json)
except Exception as aerr:
    write_error(aerr)

    sys.exit(127)
    
except Exception as err:
    write_error(err)
    print_error(ErrorUtils.internal_error(err.message))

    sys.exit(127)

# External Life Cycle Action
# Start - Create subdomain, recordset and assign ip
def start():
    try:
        result = google_dns_client.create()
        print_result(json.dumps(result))
    except Exception as err:
        write_error(err)
        sys.exit(127)

# Stop - Delete subdomain and record set
def stop() :
    try:
        result = google_dns_client.delete()
        print_result(json.dumps(result))
    except Exception as err:
        write_error(err)
        sys.exit(127)

if cmd in "start":
    start()
elif cmd in "stop":
    stop()
    
    



