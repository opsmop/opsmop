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

import inspect
import json
import logging
import logging.handlers
import os
import sys

from opsmop.callbacks.callback import BaseCallbacks
from opsmop.client.user_defaults import UserDefaults
from opsmop.core.context import Context
from opsmop.core.errors import CommandError, OpsMopStop
from opsmop.core.role import Role
from opsmop.types.type import Type

class LocalCliCallbacks(BaseCallbacks):

    """
    Callback class for the default CLI implementation.
    Improvements are welcome.
    """

    __slots__ = [ 'phase', 'count', 'logger' ]

    def __init__(self):
        super().__init__()
        self.phase = None
        self.count = 0
        self.changed_resources = 0
        self.changed_actions = 0
 
    def set_phase(self, phase):
        self.phase = phase

    def banner(self, msg, big=False):
        #self.i1("")# sep)
        self.i1(msg)


    def on_command_echo(self, provider, echo):
        if echo == "":
            return
        self.i5("| %s" % echo.rstrip())

    def on_echo(self, provider, echo):
        if not provider or not provider.very_quiet():
            self.i5("| %s" % echo)
        else:
            self.i3(echo)

    def on_execute_command(self, provider, command):
        if command.echo:
            self.i5("# %s" % command.cmd)

    def on_plan(self, provider):
        self.i3("planning")
 
    def on_apply(self, provider):
        return
    
    def on_needs(self, provider, action):
        if provider.skip_plan_stage():
            return
        if Context().is_check():
            self.i3("needs: %s" % action.do)

    def on_do(self, provider, action):
        if Context().is_apply():
            self.i3("do: %s" % action.do)

    def on_taken_actions(self, provider, actions_taken):
        if provider.skip_plan_stage():
            return

    def on_result(self, provider, result):
        if result.provider.quiet():
            return
        if result.changed:
            self.changed_resources = self.changed_resources + 1
            self.changed_actions = self.changed_actions + len(result.actions)
        self.i3(str(result))

    def on_command_result(self, provider, result):
        self.i5("= %s" % result)

    def on_skipped(self, skipped, is_handler=False):
        if self.phase != 'validate' and not is_handler and issubclass(type(skipped), Type):
            self.i3("skipped")

    def on_begin_role(self, role):
        self.phase = 'resource'
        self.role = role

    def on_validate(self):
        self.phase = 'validate'

    def on_begin_handlers(self):
        self.phase = 'handlers'

    def on_resource(self, resource, is_handler):
        if self.phase == 'validate':
            return

        # print the resource name / banner
        self.i1("")
        role = resource.role()
        self.count = self.count + 1
        self.banner("{count}. {role} => {resource}:".format(count=self.count, role=role.__class__.__name__, resource=resource))
        self.i1("")

        # show the keys for each resource, name first
        # FIXME: refactor coercion of output into provider code
        if not resource.quiet():
            keys = resource.kwargs.keys()
            keys = [ k for k in sorted(keys) if (k != 'name') ]
            if keys:
                self.i3("parameters:")
                for k in keys:
                    v = resource.kwargs[k]
                    if k == 'mode' and type(v) == int:
                        # remove this hack to print modes as octal, move this into
                        # type code and make it generic
                        v = "0o{0:o}".format(v)
                    self.i5("| %s: %s" % (k,v))

        # show if this resource is a handler
        if is_handler:
            self.i3("(handler)")

    def on_signaled(self, resource, event_name):
        self.i3("signaled: %s" % event_name)

    def on_complete(self, policy):
        self.i1("")
        self.i1("complete! changed %s resources (%s actions)" % (self.changed_resources, self.changed_actions))

    def on_fatal(self, provider, msg=None):
        self.i1("")
        if msg:
            self.i1("FAILED: %s" % msg)
        else:
            self.i1("FAILED")
        self.i1("")
        raise OpsMopStop()

    def on_update_variables(self, variables):
        self.i3("registered:")
        for (k,v) in variables.items():
            self.on_echo(None, "%s => %s" % (k,v))

    def on_host_exception(self, host, exc):
        pass
