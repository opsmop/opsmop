
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
from opsmop.types.file import File

class Directory(File):

    """
    Represents a software package
    """

    # FIXME: we need to split the file and directory provider code
    # not all of these parameters are needed for directory

    def __init__(self, name=None, **kwargs):
        self.setup(name=name, **kwargs)
        self.directory = True

    def fields(self):
        return Fields(
            self,
            name = Field(kind=str, help="path to the destination file"),
            from_file = Field(kind=str, default=None, help="path to a source file"),
            from_template = Field(kind=str, default=None, help="path to a source Jinja2 template"),
            from_content = Field(kind=str, default=None, help="use this string as source data instead of a file"),
            owner = Field(kind=str, default=None, help="owner name"),
            group = Field(kind=str, default=None, help="group name"),
            mode = Field(kind=int, default=None, help="file mode, in hex/octal (not a string)"),
            absent = Field(kind=bool, default=False, help="if true, delete the file/directory"),
            # don't use directory=, it's internal magic used by the Directory() type to allow two 
            # types to share the File provider implementation. This may go away so use that instead.
            directory = Field(kind=bool, default=False, help=None, internal=True),
            overwrite = Field(kind=bool, default=True, help="replace existing files"),
            # same with directory
            recursive = Field(kind=bool, default=False, help="if true, owner, group, and mode become recursive and always run if set")
        )
