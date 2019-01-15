
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

from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.types.type import Type


class Directory(Type):

    def __init__(self, name=None, **kwargs):
        self.setup(name=name, **kwargs)
        if self.auto_dispatch:
            self.run()

    def fields(self):
        return Fields(
            self,
            name = Field(kind=str, help="path to the destination file"),
            owner = Field(kind=str, default=None, help="owner name"),
            group = Field(kind=str, default=None, help="group name"),
            mode = Field(kind=int, default=None, help="file mode, in hex/octal (not a string)"),
            absent = Field(kind=bool, default=False, help="if true, delete the file/directory"),
            recursive = Field(kind=bool, default=False, help="if true, owner, group, and mode become recursive and always run if set")
        )

    def validate(self):
        pass

    def default_provider(self):
        from opsmop.providers.directory import Directory
        return Directory
