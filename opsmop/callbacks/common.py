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
from opsmop.core.errors import CommandError, ProviderError


INDENT="  "

class CommonCallbacks(BaseCallback):

    """
    Regardless of output modes, some behavior needs to happen after
    all callbacks are run. To keep this behavior user extensible,
    this behavior is implemented in a Callback class versus
    in the main Executor code.
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

    def on_command_echo(self, echo):
        pass

    def on_echo(self, provider, echo):
        pass

    def on_execute_command(self, command):
        pass

    def on_plan(self, provider):
        self.provider = provider
 
    def on_apply(self, provider):
        pass

    def on_needs(self, provider, action):
        self.provider = provider
        if self.provider.skip_plan_stage():
            return
        pass

    def on_do(self, provider, action):
        pass

    def on_taken_actions(self, provider, actions_taken):
        self.provider = provider
        if provider.skip_plan_stage():
            return
        taken = sorted([ str(x) for x in provider.actions_taken ])
        planned = sorted([ str(x) for x in provider.actions_planned ])
        if (taken != planned):
            raise ProviderError(provider, "actions taken (%s) do not equal planned (%s)" % (taken, planned))

    def on_result(self, result):
        pass

    def on_command_result(self, result):
        pass

    def on_skipped(self, skipped, is_handler=False):
        pass

    def on_begin_role(self, role):
        self.phase = 'resource'

    def on_validate(self):
        self.phase = 'validate'

    def on_begin_handlers(self):
        self.phase = 'handlers'

    def on_resource(self, resource, is_handler):
        pass

    def on_signalled(self, what):
        pass

    def on_complete(self, policy):
        pass

    def on_role(self, role):
        pass

    def summarize(self):
        pass

    def on_fatal(self, msg=None):
        sys.exit(1)

    def on_update_variables(self, variables):
        pass

