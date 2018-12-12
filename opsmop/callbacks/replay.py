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

class ReplayCallbacks(object):
    
    def __init__(self):
        pass

    def on_validate(self, host, evt):
        pass

    def on_role(self, host, evt):
        pass

    def on_begin_role(self, host, evt):
        pass

    def on_resource(self, host, evt):
        # {'evt': 'resource', 'resource': {'cls': 'Debug', 'variable_names': (), 'evals': {}}, 'is_handler': False}
        print(f"{host.name} : {evt['resource']['cls']}")
        pass

    def on_apply(self, host, evt):
        pass

    def on_echo(self, host, evt):
        pass

    def on_taken(self, host, evt):
        pass

    def on_plan(self, host, evt):
        pass

    def on_needs(self, host, evt):
        pass

    def on_apply(self, host, evt):
        pass
    
    def on_do(self, host, evt):
        pass

    def on_execute_command(self, host, evt):
        pass

    def on_command_echo(self, host, evt):
        pass

    def on_command_result(self, host, evt):
        pass

    def on_complete(self, host, evt):
        pass

    def on_result(self, host, evt):
        # {'evt': 'result', 'provider': {'cls': 'Debug'}, 'data': {'cls': 'Result', 'rc': None, 'data': None, 'fatal': False, 'message': None, 'reason': None}}
        print(f"{host.name} : {evt['data']}")

    def on_default(self, host, evt):
        print(f"{host.name} : {evt}")

    def on_fatal(self, host, evt):
        print('task failed on host %s: %s' % (host.name, e))

    