#!/bin/python3
### Doesn't Work, Need Help!!!

from libqtile.command import client

import getpass
import subprocess

try:
    client = Client()
    client.shutdown()
except:
    subprocess.Popen(["liginctl","terminate-user",getpass.getuser()])
