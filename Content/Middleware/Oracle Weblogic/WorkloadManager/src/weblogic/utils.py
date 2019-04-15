import sys
import os
from os.path import exists

# Get File Path
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

# Parse Properties File
def parse_file(path):
    _dict = {}
    if exists(path):
        try:
            fo = open(path, 'r+')
            lines = fo.readlines()
            for line in lines:
                if "=" in line:
                    line = line.rstrip()
                    key = line.split('=')[0]
                    value = line.split('=')[1]
                    _dict[key] = value
        except Exception, e:
            print e
    return _dict

# Get All nodes as list
def get_nodes():
    nodes = []
    try:
        app_tier_name = os.environ.get("cliqrAppTierName", False)
        print app_tier_name
        if not app_tier_name:
            sys.exit(127)

        names = str(os.environ['CliqrTier_' + app_tier_name + '_HOSTNAME']).split(',')
        ips = str(os.environ['CliqrTier_' + app_tier_name + '_IP']).split(',')

        for i in range(0, len(names)):
            _node = {}
            _node["name"] = names[i]
            _node["ip"] = ips[i]

            nodes.append(_node)

    except Exception, err:
        print err
        sys.exit(127)

    return nodes