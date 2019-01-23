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

from opsmop.callbacks.callbacks import Callbacks
from opsmop.client.user_defaults import UserDefaults
from opsmop.core.collection import Collection
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.handlers import Handlers
from opsmop.core.resource import Resource
from opsmop.core.resources import Resources
from opsmop.core.vars import VarsLoader

class Role(Collection):

    """
    A role is a collection of resources, handlers, and variables.  A Site policy can
    contain more than one one role.
    
    For an example see demo/content.py
    """

    def __init__(self, *args, **kwargs):
        (original, common) = self.split_common_kwargs(kwargs)
        self.setup(extra_variables=original, **common)
        #self.vars = VarsLoader(self)

    def fields(self):
        return Fields(
            self,
            name = Field(kind=str, default=None),
            variables = Field(kind=dict, loader=self.set_variables),
            resources = Field(kind=list, of=Resource, loader=self.set_resources),
            handlers  = Field(kind=dict, of=Resource, loader=self.set_handlers),
        )

    def serial(self):
        # number of hosts to simultaenously execute
        return 80

    def set_variables(self):
        return dict()

    def set_resources(self):
        return Resources()

    def set_handlers(self):
        return Handlers()

    def allow_fileserving_paths(self):
        # returning None means ask the policy, return [] for
        return None

    def role(self):
        return self

    def sudo(self):
        return False

    def ssh_as(self):
        return (UserDefaults.ssh_username(), UserDefaults.ssh_password())

    def sudo_as(self):
        return (UserDefaults.sudo_username(), UserDefaults.sudo_password())

    def check_host_keys(self):
        return UserDefaults.ssh_check_host_keys()

    def get_delegate_host(self, host_obj):
        return host_obj # or name, either is ok.

    def before_contact(self, host):
        return True

    def should_contact(self, host):
        return True

    def after_contact(self, host):
        return True

    def get_children(self, mode):
        if mode == 'resources':
            return self.resources
        elif mode == 'handlers':
            return self.handlers

    def __str__(self):
        return "Role: %s" % self.__class__.__name__
