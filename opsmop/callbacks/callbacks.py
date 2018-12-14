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

# NOTE: this interface is subject to change

CALLBACKS = []

class Callbacks(object):

    @classmethod
    def set_callbacks(cls, callbacks):
        global CALLBACKS
        CALLBACKS = callbacks
            
    @classmethod
    def _run_callbacks(cls, cb_method, *args):
        """ 
        Run a named callback method against all attached callback classes, in order.
        """
        global CALLBACKS
        for c in CALLBACKS:
            attr = getattr(c, cb_method, None)
            if attr:
                attr(*args)

    @classmethod
    def on_apply(cls, provider):
        cls._run_callbacks('on_apply', provider)

    @classmethod
    def on_finished(cls, value):
        cls._run_callbacks('on_finished')

    @classmethod
    def on_echo(cls, provider, value):
        cls._run_callbacks('on_echo', provider, value)

    @classmethod
    def on_plan(cls, provider):
        cls._run_callbacks('on_plan', provider)

    @classmethod
    def on_command_echo(cls, provider, value):
        cls._run_callbacks('on_command_echo', provider, value)

    @classmethod
    def on_execute_command(cls, provider, value):
        cls._run_callbacks('on_execute_command', provider, value)

    @classmethod
    def on_resource(cls, resource, is_handler):
        cls._run_callbacks('on_resource', resource, is_handler)

    @classmethod
    def on_command_result(cls, provider, value):
        cls._run_callbacks('on_command_result', provider, value)

    @classmethod
    def on_needs(cls, provider, action):
        cls._run_callbacks('on_needs', provider, action)

    @classmethod
    def on_do(cls, provider, action):
        cls._run_callbacks('on_do', provider, action)

    @classmethod
    def on_taken_actions(cls, provider, actions_list):
        cls._run_callbacks('on_taken_actions', provider, actions_list)

    @classmethod
    def on_result(cls, provider, result):
        cls._run_callbacks('on_result', provider, result)
        if result.fatal:
            cls._run_callbacks('on_fatal', provider, result)

    @classmethod
    def on_skipped(cls, value, is_handler=False):
        cls._run_callbacks('on_skipped', value, is_handler)

    @classmethod
    def on_signaled(cls, resource, event_name):
        cls._run_callbacks('on_signaled', resource, event_name)

    @classmethod
    def on_complete(cls, policy):
        cls._run_callbacks('on_complete', policy)

    @classmethod
    def on_update_variables(cls, variables):
        cls._run_callbacks('on_update_variables', variables)

    @classmethod
    def on_begin_role(cls, role):
        cls._run_callbacks('on_begin_role', role)

    @classmethod
    def on_begin_handlers(cls):
        cls._run_callbacks('on_begin_handlers')

    @classmethod
    def on_validate(cls):
        cls._run_callbacks('on_validate')

    @classmethod
    def on_host_exception(cls, host, exc):
        # is this needed?
        cls._run_callbacks('on_failed_host', host, exc)

    @classmethod
    def on_terminate_with_host_list(cls, host_list):
        cls._run_callbacks('on_terminate_with_host_list', host_list)
