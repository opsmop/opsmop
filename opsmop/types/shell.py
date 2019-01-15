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


class Shell(Type):

    """
    Represents a command to be run
    """

    def __init__(self, cmd=None, **kwargs):
        self.setup(cmd=cmd, **kwargs)
        if self.auto_dispatch:
            self.run()
            
    def fields(self):
        return Fields(
            self,
            cmd      = Field(kind=str, default=None, help="execute this shell code in the default shell"),
            timeout  = Field(kind=int, default=99999, help="max time to allow this command to run") 
        )

    def validate(self):
        # v = Validators(self)
        # FIXME: add this back when we add the 'script' feature
        # v.mutually_exclusive(['cmd', 'script'])
        # v.required_one_of(['cmd', 'script'])
        # v.path_exists(self.script)
        pass

    def default_provider(self):
        from opsmop.providers.shell import Shell
        return Shell
