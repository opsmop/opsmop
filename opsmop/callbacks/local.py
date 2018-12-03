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
import inspect
import json

from opsmop.core.callback import BaseCallback
from opsmop.core.role import Role
from opsmop.types.type import Type
from opsmop.core.errors import CommandError

# NOTE: this interface is subject to change

INDENT="  "

class LocalCallbacks(BaseCallback):

    """
    Callback class for the default CLI implementation.
    Improvements are welcome.
    """

    __slots__ = [ 'dry_run', 'role', 'phase', 'count' ]

    def __init__(self):
        super()
        self.dry_run = False
        self.role = None
        self.phase = None
        self.count = 0

    def set_phase(self, phase):
        self.phase = phase

    def banner(self, msg, big=False):
        msg_len = len(msg)
        sep = None
        if big:
            sep = "=" * msg_len
        else:
            sep = "-" * msg_len
        self.i1(sep)
        self.i1(msg)
        if big:
            self.i1(sep)

    def on_command_echo(self, echo):
        if echo == "":
            return
        self.i5("| %s" % echo.rstrip())

    def on_echo(self, provider, echo):
        if not provider or not provider.very_quiet():
            self.i5("| %s" % echo)
        else:
            self.i3(echo)

    def on_execute_command(self, command):
        if command.echo:
            self.i5("# %s" % command.cmd)

    def on_plan(self, provider):
        self.provider = provider
        self.i3("planning...")
 
    def on_apply(self, provider):
        return
    
    def on_needs(self, provider, action):
        self.provider = provider
        if self.provider.skip_plan_stage():
            return
        if self.context().is_check():
            self.i3("needs: %s" % action.do)

    def on_do(self, provider, action):
        if self.context().is_apply():
            self.i3("do: %s" % action.do)

    def on_taken_actions(self, provider, actions_taken):
        if provider.skip_plan_stage():
            return
        self.provider = provider

    def on_result(self, result):
        if result.provider.quiet():
            return
        self.i3(str(result))

    def on_command_result(self, result):
        self.i5("= %s" % result)
        if result.fatal:
            raise CommandError(self.provider, "command failed", result)

    def on_skipped(self, skipped, is_handler=False):
        if self.phase != 'validate' and not is_handler and issubclass(type(skipped), Type):
            self.i3("skipped")

    def on_begin_role(self, role):
        self.phase = 'resource'

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
        self.banner("{count}. {role} => {resource}".format(count=self.count, role=role.__class__.__name__, resource=resource))
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

    def on_signalled(self, what):
        self.i3("signalled: %s" % what)

    def on_complete(self, policy):
        self.i1("")
        self.banner("complete!")
        self.summarize()

    def on_role(self, role):
        self.role = role

    def summarize(self):
        # TODO: reimplement the counter and percentages summary
        pass

    def on_fatal(self, msg=None):
        if msg:
            self.i1("FAILED: %s" % msg)
        else:
            self.i1("FAILED")
        self.summarize()

    def on_update_variables(self, variables):
        self.i3("registered:")
        for (k,v) in variables.items():
            self.on_echo(None, "%s => %s" % (k,v))

    def i1(self, msg):
        # indent methods
        self._indent(0, msg)

    def i2(self, msg):
        self._indent(1, msg)

    def i3(self, msg):
        self._indent(2, msg)

    def i4(self, msg):
        self._indent(3, msg)

    def i5(self, msg):
        self._indent(4, msg)
    
    def _indent(self, level, msg):
        spc = INDENT * level
        print("%s%s" % (spc, msg))
