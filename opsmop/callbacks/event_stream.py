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
from opsmop.core.errors import FailedResult
from opsmop.core.role import Role
from opsmop.types.type import Type


class EventStreamCallbacks(BaseCallbacks):

    """
    Callback class for the default CLI implementation.
    Improvements are welcome.
    """

    __slots__ = [ 'phase', 'count' ]

    def __init__(self, sender=None):
        super()
        self.sender = sender

    def on_execute_command(self, provider, command):
        self.event('execute_command', provider=provider, data=command)

    def on_result(self, provider, result):
        self.event('result', provider=provider, data=result)

    def on_resource(self, resource):
        self.event('resource', resource=resource)

    def on_fatal(self, exception=None):
        self.event('fatal', exception=exception)

    def on_command_result(self, provider, result):
        self.event('command_result', provider=provider, data=result)

    def on_command_echo(self, provider, echo):
        self.event('command_echo', provider=provider, data=echo)

    def on_echo(self, provider, echo):
        self.event('echo', provider=provider, data=echo)

    def on_complete(self, policy):
        self.event('complete', policy=policy)

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
        self.sender.send(data)
