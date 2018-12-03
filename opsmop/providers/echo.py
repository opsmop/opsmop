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

import os
import shutil

from opsmop.core.template import Template
from opsmop.providers.provider import Provider

COWSAY = "cowsay '{msg}'"

class Echo(Provider):

    def quiet(self):
        return True

    def very_quiet(self):
        return True

    def skip_plan_stage(self):
        return True

    def apply(self):
        
        self.cowsay = shutil.which('cowsay')
        txt = Template.from_string(self.msg, self.resource)

        if self.cowsay and os.environ.get('MOO'):
            cmd = COWSAY.format(msg=txt)
            txt = self.run(cmd, echo=False)
        self.echo(txt)

        return self.ok()
