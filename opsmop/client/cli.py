
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
import argparse
import os

from opsmop.callbacks.callbacks import Callbacks
from opsmop.callbacks.local import LocalCliCallbacks
from opsmop.callbacks.event_stream import EventStreamCallbacks
from opsmop.callbacks.common import CommonCallbacks
from opsmop.core.context import Context
from opsmop.core.api import Api
from opsmop.core.errors import OpsMopError, OpsMopStop

USAGE = """
|
| opsmop - (C) 2018, Michael DeHaan LLC
|
| opsmop --validate demo/policy.py 
| opsmop --check demo/policy.py [--local|--push]
| opsmop --apply demo/policy.py [--local|--push]
|
"""

class Cli(object):

    def __init__(self, policy):
        """
        The CLI is constructed with the sys.argv command line, see bin/opsmop
        """
        self.policy = policy
        self.args = sys.argv
        self.go()
 
    def go(self):
       
        if len(self.args) < 3 or sys.argv[1] == "--help":
            print(USAGE)
            sys.exit(1)

        mode = self.args[1]
        path = sys.argv[2]
        callbacks = None

        parser = argparse.ArgumentParser()
        parser.add_argument('--validate', action='store_true', help='policy file to validate')
        parser.add_argument('--apply', action='store_true', help="policy file to apply")
        parser.add_argument('--check', action='store_true', help="policy file to check")
        parser.add_argument('--tags', help='optional comma seperated list of tags')
        parser.add_argument('--push', action='store_true', help='run in push mode')
        parser.add_argument('--local', action='store_true', help='run in local mode')
        parser.add_argument('--verbose', action='store_true', help='increase verbosity (for remote modes)')

        args = parser.parse_args(self.args[1:])

        all_modes = [ args.validate, args.apply, args.check ]
        selected_modes = [ x for x in all_modes if x is True ]
        if len(selected_modes) != 1:
            print(selected_modes)
            print(USAGE)
            sys.exit(1)

        all_modes = [ args.push, args.local ]
        selected_modes = [ x for x in all_modes if x is True ]
        if len(selected_modes) != 1:
            print(USAGE)
            sys.exit(1)

        Callbacks.set_callbacks([ EventStreamCallbacks(), CommonCallbacks() ])
        Context.set_verbose(args.verbose)

        tags = None
        if args.tags is not None:
            tags = args.tags.strip().split(",")

        api = Api(policies=[self.policy], tags=tags, push=args.push)

        abspath = os.path.abspath(sys.modules[self.policy.__module__].__file__)
        os.chdir(os.path.dirname(abspath))

        try:
            if args.validate:
                # just check for missing files and invalid types
                api.validate()
            elif args.check:
                # operate in dry-run mode
                api.check()
            elif args.apply:
                # configure everything
                api.apply()
            else:
                print(USAGE)
                sys.exit(1)
        except OpsMopStop as oms:
            sys.exit(1)
        except OpsMopError as ome:
            print("")
            print(str(ome))
            print("")
            sys.exit(1)


        print("")
        sys.exit(0)
