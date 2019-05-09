#!/usr/bin/env python

import os
import sys
import base64

try:
    pwd = os.environ['commvaultPassword']
    print(base64.b64encode(pwd))
except:
    print("")
    sys.exit(0)
