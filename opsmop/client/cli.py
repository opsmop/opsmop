
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

import argparse
import os
import sys

from colorama import init as colorama_init

from opsmop.callbacks.callbacks import Callbacks
from opsmop.callbacks.common import CommonCallbacks
from opsmop.callbacks.event_stream import EventStreamCallbacks
from opsmop.callbacks.local import LocalCliCallbacks
from opsmop.core.api import Api
from opsmop.core.context import Context
from opsmop.core.errors import OpsMopError, OpsMopStop
from opsmop.core.common import load_data_file, shlex_kv

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

    def handle_extra_vars(self, extra_vars):
        data = None
        # TODO: make some functions in common that do this generically
        if extra_vars.startswith("@"):
            extra_vars = extra_vars.replace("@","")
            data = load_data_file(extra_vars)
        else:
            data = shlex_kv(extra_vars)
        return data
 
    def go(self):

        colorama_init()
       
        if len(self.args) < 3 or sys.argv[1] == "--help":
            print(USAGE)
            sys.exit(1)

        mode = self.args[1]
        path = sys.argv[2]
        callbacks = None
        extra_vars = dict()

        parser = argparse.ArgumentParser()
        parser.add_argument('--validate', action='store_true', help='policy file to validate')
        parser.add_argument('--apply', action='store_true', help="policy file to apply")
        parser.add_argument('--check', action='store_true', help="policy file to check")
        parser.add_argument('--tags', help='optional comma seperated list of tags')
        parser.add_argument('--push', action='store_true', help='run in push mode')
        parser.add_argument('--local', action='store_true', help='run in local mode')
        parser.add_argument('--verbose', action='store_true', help='(with --push) increase verbosity')
        parser.add_argument('--extra-vars', help="add extra variables from the command line")
        parser.add_argument('--limit-groups', help="(with --push) limit groups executed to this comma-separated list of patterns")
        parser.add_argument('--limit-hosts', help="(with --push) limit hosts executed to this comma-separated list of patterns")
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

        if args.extra_vars is not None:
            extra_vars = self.handle_extra_vars(args.extra_vars)

        Callbacks().set_callbacks([ LocalCliCallbacks(), CommonCallbacks() ])
        Context().set_verbose(args.verbose)

        tags = None
        if args.tags is not None:
            tags = args.tags.strip().split(",")

        api = Api(policies=[self.policy], tags=tags, push=args.push, extra_vars=extra_vars, limit_groups=args.limit_groups, limit_hosts=args.limit_hosts)

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
