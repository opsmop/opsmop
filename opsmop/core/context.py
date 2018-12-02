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

class Context(object):

    def __init__(self, mode=None, callbacks=None):

        self._callbacks = callbacks
        self._signals = []
        assert mode in [ 'validate', 'apply', 'check' ]
        self._mode = mode
        for cb in self._callbacks:
            cb.set_context(self)

    def mode(self):
        return self._mode

    def add_signal(self, signal):
        self._signals.append(signal)

    def has_seen_any_signal(self, signals):
        for x in self._signals:
            if x in signals:
                return True
        return False
            
    def _run_callbacks(self, cb_method, *args):
        """ 
        Run a named callback method against all attached callback classes, in order.
        """
        for c in self._callbacks:
            c.set_context(self)
            attr = getattr(c, cb_method)
            attr(*args)

    def on_apply(self, provider):
        self._run_callbacks('on_apply', provider)

    def on_finished(self, value):
        self._run_callbacks('on_finished')

    def on_echo(self, provider, value):
        self._run_callbacks('on_echo', provider, value)

    def on_plan(self, provider):
        self._run_callbacks('on_plan', provider)

    def on_role(self, role):
        self._run_callbacks('on_role', role)

    def on_command_echo(self, value):
        self._run_callbacks('on_command_echo', value)

    def on_execute_command(self, value):
        self._run_callbacks('on_execute_command', value)

    def on_resource(self, resource, is_handler):
        self._run_callbacks('on_resource', resource, is_handler)

    def on_command_result(self, value):
        self._run_callbacks('on_command_result', value)

    def on_needs(self, provider, action):
        self._run_callbacks('on_needs', provider, action)

    def on_do(self, provider, action):
        self._run_callbacks('on_do', provider, action)
    
    def on_taken_actions(self, provider, actions_list):
        self._run_callbacks('on_taken_actions', provider, actions_list)

    def on_result(self, result):
        self._run_callbacks('on_result', result)
        if result.fatal:
            self._run_callbacks('on_fatal', result)

    def on_skipped(self, value, is_handler=False):
        self._run_callbacks('on_skipped', value, is_handler)

    def on_flagged(self, value):
        self._run_callbacks('on_flagged', value)

    def on_complete(self, value):
        self._run_callbacks('on_complete', value)

    def on_update_variables(self, variables):
        self._run_callbacks('on_update_variables', variables)

    def on_begin_role(self, role):
        self._run_callbacks('on_begin_role', role)

    def on_begin_handlers(self):
        self._run_callbacks('on_begin_handlers')

    def on_validate(self):
        self._run_callbacks('on_validate')
