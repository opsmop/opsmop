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
from opsmop.core.validators import Validators
from opsmop.types.type import Type

class File(Type):

    def __init__(self, name=None, **kwargs):
        self.setup(name=name, **kwargs)

    def fields(self):
        return Fields(
            self,
            name = Field(kind=str, help="path to the destination file"),
            from_file = Field(kind=str, default=None, help="path to a source file"),
            from_url = Field(kind=str, default=None, help="url to a source file"),
            from_template = Field(kind=str, default=None, help="path to a source Jinja2 template"),
            from_content = Field(kind=str, default=None, help="use this string as source data instead of a file"),
            owner = Field(kind=str, default=None, help="owner name"),
            group = Field(kind=str, default=None, help="group name"),
            mode = Field(kind=int, default=None, help="file mode, in hex/octal (not a string)"),
            absent = Field(kind=bool, default=False, help="if true, delete the file/directory"),
            overwrite = Field(kind=bool, default=True, help="replace existing files"),
        )

    def validate(self):
        v = Validators(self)
        v.mutually_exclusive(['from_file', 'from_url', 'from_template', 'from_content'])
        v.path_exists(self.from_file)
        v.path_exists(self.from_template)

    def default_provider(self):
        from opsmop.providers.file import File
        return File
