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

from opsmop.core.common import Singleton

# TODO: __getattr__ this beast and eliminate all of these methods

class Callbacks(metaclass=Singleton):

    def set_callbacks(self, callbacks):
        self._callbacks = callbacks
        self._hostname_length = 0

    def set_hostname_length(self, length):
        self._hostname_length = length

    def hostname_length(self):
        return self._hostname_length
            
    def _run_callbacks(self, cb_method, *args):
        """ 
        Run a named callback method against all attached callback classes, in order.
        """
        if getattr(self, '_callbacks', None) is None:
            # callbacks not ready yet
            return

        for c in self._callbacks:
            attr = getattr(c, cb_method, None)
            if attr:
                attr(*args)

    def on_apply(self, provider):
        self._run_callbacks('on_apply', provider)

    def on_finished(self, value):
        self._run_callbacks('on_finished')

    def on_echo(self, provider, value):
        self._run_callbacks('on_echo', provider, value)

    def on_plan(self, provider):
        self._run_callbacks('on_plan', provider)

    def on_command_echo(self, provider, value):
        self._run_callbacks('on_command_echo', provider, value)

    def on_execute_command(self, provider, value):
        self._run_callbacks('on_execute_command', provider, value)

    def on_resource(self, resource):
        self._run_callbacks('on_resource', resource)

    def on_command_result(self, provider, value):
        self._run_callbacks('on_command_result', provider, value)

    def on_needs(self, provider, action):
        self._run_callbacks('on_needs', provider, action)

    def on_do(self, provider, action):
        self._run_callbacks('on_do', provider, action)

    def on_taken_actions(self, provider, actions_list):
        self._run_callbacks('on_taken_actions', provider, actions_list)

    def on_result(self, provider, result):
        self._run_callbacks('on_result', provider, result)
        if result.fatal:
            self._run_callbacks('on_fatal', provider, result)

    def on_skipped(self, value, is_handler=False):
        self._run_callbacks('on_skipped', value, is_handler)

    def on_complete(self, policy):
        self._run_callbacks('on_complete', policy)

    def on_update_variables(self, variables):
        self._run_callbacks('on_update_variables', variables)

    def on_begin_role(self, role):
        self._run_callbacks('on_begin_role', role)

    def on_begin_handlers(self):
        self._run_callbacks('on_begin_handlers')

    def on_validate(self):
        self._run_callbacks('on_validate')

    def on_host_exception(self, host, exc):
        # is this needed?
        self._run_callbacks('on_failed_host', host, exc)

    def on_terminate_with_host_list(self, host_list):
        self._run_callbacks('on_terminate_with_host_list', host_list)

    def on_host_changed_list(self, hosts):
        self._run_callbacks('on_host_changed_list', hosts)

