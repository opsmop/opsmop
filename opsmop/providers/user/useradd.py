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

from opsmop.providers.provider import Provider

CREATE = "useradd {name}"
REMOVE = "userdel {name} --force"
EXISTS = "getent passwd {name}"

class UserAdd(Provider):

    def _exists(self):
        test = self.test(EXISTS.format(name=self.name))
        return test is not None

    def plan(self):
        exists = self._exists()
        # at this point, no attributes are modified by this resource if they exist
        # this is probably desirable in most cases, but some future attributes
        # should be modifiable.
        if exists and self.absent:
            self.needs('remove')
        elif not exists:
            self.needs('add')

    def apply(self):

        if self.should('remove'):
            # if folks want control over using --force and keeping homedirs, patches would be considered.
            self.do('remove')
            return self.run(REMOVE.format(name=self.name))
        elif self.should('add'):
            # patches for additional options would be considered
            self.do('add')
            cmd = CREATE.format(name=self.name)
            if self.uid:
                cmd = cmd + " --uid=%s" % self.uid
            if self.group:
                cmd = cmd + " --gid=%s" % self.group
            if self.groups:
                cmd = cmd + " --groups=%s" % ",".join(self.groups)
            if self.home:
                cmd = cmd + " --home=%s --create-home" % self.home
            if self.system:
                cmd = cmd + " --system"
            if self.shell:
                cmd = cmd + " --shell=%s" % self.shell
            return self.run(cmd)


    


