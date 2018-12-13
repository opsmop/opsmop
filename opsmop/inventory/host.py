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
    
    def python_path(self):
        return self.variables.get('opsmop_python_path', UserDefaults.python_path())
      
    def connection_context(self, role):
        
        hostname = self.hostname()
        sudo = role.sudo()
        
        (role_sudo_username, role_sudo_password) = role.sudo_as()
        if role_sudo_username is None:
            role_sudo_username = self.sudo_username()
        if role_sudo_password is None:
            role_sudo_password = self.sudo_password()

        (role_ssh_username, role_ssh_password) = role.ssh_as()
        if role_ssh_username is None:
            role_ssh_username = self.ssh_username()
        if role_ssh_password is None:
            role_ssh_password = self.ssh_password()
        
        role_check_host_keys = role.check_host_keys()
        if role_check_host_keys is None:
            role_check_host_keys = self.check_host_keys()
        
        return dict(
            hostname = hostname,
            sudo = sudo,
            username = role_ssh_username,
            password = role_ssh_password,
            sudo_username = role_sudo_username,
            sudo_password = role_sudo_password,
            check_host_keys = role_check_host_keys
        )
