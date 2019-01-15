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

from opsmop.core.errors import NoSuchProviderError, ValidationError
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.facts.platform import Platform
from opsmop.types.type import Type


class Group(Type):

    def __init__(self, name=None, **kwargs):
        self.setup(name=name, **kwargs)
        if self.auto_dispatch:
            self.run()
            
    def fields(self):
        return Fields(
            self,
            name = Field(kind=str, help="the name of the group"),
            gid = Field(kind=int, default=None, help="if set, use this group ID (on creation)"),
            system = Field(kind=bool, default=False, help="if True, specifies a system group (on creation)"),
            absent = Field(kind=bool, default=False, help="if True, remove this group")
        )

    def validate(self):
        pass

    def get_provider(self, method):
        if method == 'groupadd':
            from opsmop.providers.group.groupadd import GroupAdd
            return GroupAdd
        raise NoSuchProviderError(self, method)

    def default_provider(self):
        return Platform.default_group_manager()
