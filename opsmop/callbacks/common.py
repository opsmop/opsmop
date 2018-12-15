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
import sys

from opsmop.callbacks.callback import BaseCallbacks
from opsmop.core.errors import CommandError, OpsMopError, ProviderError
from opsmop.core.role import Role
from opsmop.types.type import Type

class CommonCallbacks(BaseCallbacks):

    """
    Regardless of output modes, some behavior needs to happen after
    all callbacks are run. To keep this behavior user extensible,
    this behavior is implemented in a Callback class versus
    in the main Executor code.
    """

    def set_phase(self, phase):
        self.phase = phase

    def on_taken_actions(self, provider, actions_taken):
        if provider.skip_plan_stage():
            return
        taken = sorted([ str(x) for x in provider.actions_taken ])
        planned = sorted([ str(x) for x in provider.actions_planned ])
        if (taken != planned):
            err = ProviderError(provider, "actions taken (%s) do not equal planned (%s)" % (taken, planned))
            self.record_host_failure(Context().host(), err)
            raise err

    def on_command_result(self, provider, result):
        if not result.primary and result.fatal:
            # only process intermediate command results here, if the command result is to be the final
            # return of a module, let the Executor code handle this so failed_when/ignore_errors can take
            # effect
            err = CommandError(provider, "command failed", result)
            self.record_host_failure(Context().host(), err)
            raise err

    def on_fatal(self, provider, msg=None):
        #raise OpsMopError("failed")
        pass

    def on_host_exception(self, host, exc):
        Context().record_host_failure(host, exc)
