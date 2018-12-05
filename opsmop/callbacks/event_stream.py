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

class EventStreamCallbacks(BaseCallback):

    """
    Callback class for the default CLI implementation.
    Improvements are welcome.
    """

    __slots__ = [ 'phase', 'count' ]

    def __init__(self):
        super()

    def on_command_echo(self, provider, echo):
        self.event('command_echo', data=echo)

    def on_echo(self, provider, echo):
        self.event('echo', data=echo)

    def on_execute_command(self, provider, command):
        self.event('execute_command', provider=provider, data=command)

    def on_plan(self, provider):
        self.event('plan', provider=provider)
 
    def on_apply(self, provider):
        self.event('apply', provider=provider)
    
    def on_needs(self, provider, action):
        self.event('needs', provider=provider, data=action)

    def on_do(self, provider, action):
        self.event('do', provider=provider, data=action)

    def on_taken_actions(self, provider, actions_taken):
        self.event('taken', provider=provider, data=actions_taken)

    def on_result(self, provider, result):
        self.event('result', provider=provider, data=result)

    def on_command_result(self, provider, result):
        self.event('command_result', provider=provider, data=result)

    def on_skipped(self, skipped, is_handler=False):
        pass

    def on_begin_role(self, role):
        self.event('begin_role', role=role)

    def on_validate(self):
        self.event('validate')

    def on_begin_handlers(self):
        pass

    def on_resource(self, resource, is_handler):
        self.event('resource', resource=resource, is_handler=is_handler)

    def on_signaled(self, resource, event_name):
        self.event('signaled', resource=resource, data=event_name)

    def on_complete(self, policy):
        self.event('complete', policy=policy)

    def on_role(self, role):
        self.event('role', role=role)

    def summarize(self):
        pass

    def on_fatal(self, provider, msg=None):
        self.event('fatal', provider=provider, data=msg)

    def on_update_variables(self, variables):
        pass

    def event(self, name, **kwargs):
        data = dict()
        data['evt'] = name
        for (k,v) in kwargs.items():
            if type(v) == list:
                interim = []
                for i in v:
                    if hasattr(i, 'to_dict'):
                        interim.append(i.to_dict())
                    else:
                        interim.append(i)
                v = interim
            else:
                if hasattr(v, 'to_dict'):
                    v = v.to_dict()
            data[k] = v
        print(json.dumps(data))
