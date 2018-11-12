
from runpy import run_path
import json
import sys
import argparse
import os


from opsmop.core.executor import Executor
from opsmop.types.package import Package
from opsmop.client.facts import Facts
from opsmop.client.callbacks import Callbacks
from opsmop.core.errors import ValidationError

USAGE = """
|
| opsmop - (C) 2018, Michael DeHaan LLC
|
| opsmop show  demo/policy.py 
| opsmop check demo/policy.py
| opsmop apply demo/policy.py  
|
"""

# WARNING: this file is kind of a mess at the moment, but largely works.
# once stabilized, it will get cleaned up lots and be more explicit.
# this is leftover from trying to make a multi-level CLI which I don't think
# we need now.

class Cli(object):

    def __init__(self, args):
        self.args = args
        self.callbacks = Callbacks()

    def go(self):
       
        if len(self.args) < 2 or sys.argv[1] == "--help":
            print(USAGE)
            sys.exit(1)

        mode = self.args[1]
        method = "handle_%s" % (mode)
        method = getattr(self, method, None)

        if method is None:
            print(USAGE)
            sys.exit(1)


        path = os.path.expandvars(os.path.expanduser(self.args[2]))

        if not os.path.exists(path):
            print("file does not exist: %s" % path)
            sys.exit(1)


        print("")
        method(path, self.args[3:])
        print("")

    def local_policy(self, path):
        ran = run_path(path)
        dirname = os.path.dirname(path)
        os.chdir(dirname)
        if 'EXPORTED' not in ran:
            print("unable to find EXPORTED in %s" % fname)
            sys.exit(1)
        for x in ran['EXPORTED']:
            yield x
        return

    def executor(self, policy):
        return Executor(policy, self.callbacks)

    def _parser(self, remote=False, local=False, upload=False, facts=False, ):
        parser = argparse.ArgumentParser()
        # we might actually use this someday!
        return parser

    # all of this is going to get scrapped

    def handle_show(self, path, args):
        parser = self._parser(local=True)
        params = parser.parse_args(args)
        return self.do_policy(path, params, 'show')

    def handle_check(self, path, args):
        parser = self._parser(local=True)
        params = parser.parse_args(args)
        return self.do_policy(path, params, 'check')

    def handle_apply(self, path, args):
        parser = self._parser(local=True)
        params = parser.parse_args(args)
        return self.do_policy(path, params, 'apply')

    def do_policy(self, path, params, method):
        # do something for every local policy resource but validate them all first
        try:
            ok = True
            for policy in self.local_policy(path):
                obj = self.executor(policy)
                method = getattr(obj, method)
                method()
        except ValidationError as ve:
            print("validation error on resource %s: %s" % (ve.resource, ve.msg))
            sys.exit(1)



