
# Copyright 2018 Michael DeHaan LLC, <michael@michaeldehaan.net>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

from opsmop.client.callbacks import CliCallbacks
from opsmop.core.api import Api

# import argparse


USAGE = """
|
| opsmop - (C) 2018, Michael DeHaan LLC
|
| opsmop show  demo/policy.py 
| opsmop check demo/policy.py
| opsmop apply demo/policy.py  
|
"""

class Cli(object):

    __slots__ = [ 'args' ]

    def __init__(self, args):
        """
        The CLI is constructed with the sys.argv command line, see bin/opsmop
        """
        self.args = args
 
    def go(self):
       
        if len(self.args) < 3 or sys.argv[1] == "--help":
            print(USAGE)
            sys.exit(1)

        mode = self.args[1]
        path = sys.argv[2]
        callbacks = [ CliCallbacks() ]

        api = Api.from_file(path=path, callbacks=callbacks)
        
        if mode == 'validate':
            # just check for missing files and invalid types
            api.validate()
        elif mode == 'check':
            # operate in dry-run mode
            api.check()
        elif mode == 'apply':
            # configure everything
            api.apply()
        else:
            print(USAGE)
            sys.exit(1)
   
        print("")
        sys.exit(0)
