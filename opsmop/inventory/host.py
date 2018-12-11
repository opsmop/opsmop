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

from opsmop.client.user_defaults import UserDefaults

class Host(object):

    def __init__(self, name, variables=None):
        self.name = name
        if variables is None:
            variables = dict()
        self.variables = variables
        self._groups = dict()

    def update_variables(self, variables):
        self.variables.update(variables)

    def add_group(self, group):
        self._groups[group.name] = group

    def hostname(self):
        return self.variables.get('opsmop_host', self.name)

    def all_variables(self):
        results = dict()
        for g in self._groups.values():
            results.update(g.variables)
        results.update(self.variables)
        return results

    def hostname(self):
        return self.variables.get('opsmop_host', self.name)

    def ssh_username(self):
        return self.variables.get('opsmop_ssh_username', UserDefaults.ssh_username())

    def sudo_username(self):
        return self.variables.get('opsmop_sudo_username', UserDefaults.sudo_username())

    def ssh_password(self):
        return self.variables.get('opsmop_ssh_password', UserDefaults.ssh_password())

    def sudo_password(self):
        return self.variables.get('opsmop_sudo_password', UserDefaults.sudo_password())

    def check_host_keys(self):
        return self.variables.get('opsmop_ssh_check_host_keys', UserDefaults.ssh_check_host_keys())
    
    def to_dict(self):
        # serialization for remote functionality only, sends a limited set of info
        return dict(
            name = self.name,
            variables = self.variables,
        )

    @classmethod
    def from_dict(cls, data):
        return Host.__new__(cls, name=data['name'], variables=data['variables'])
      