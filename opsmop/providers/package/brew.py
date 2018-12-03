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

from opsmop.providers.package.package import Package

TIMEOUT = 1800
VERSION_CHECK = "brew ls --versions {name} | cut -f2 -d ' '"
INSTALL = "brew install {name}"
UPGRADE = "brew update {name}"
UNINSTALL = "brew uninstall {name}"

class Brew(Package):

    def _get_version(self):
        version_check = VERSION_CHECK.format(name=self.name)
        return self.test(version_check)

    def get_default_timeout(self):
        return TIMEOUT

    def plan(self):
        super().plan()

    def apply(self):
        which = None
        if self.should('install'):
            self.do('install')
            which = INSTALL.format(name=self.name)
        elif self.should('upgrade'):
            self.do('upgrade')
            which = UPGRADE.format(name=self.name)
        elif self.should('remove'):
            self.do('remove')
            which = UNINSTALL.format(name=self.name)

        if which:
            return self.run(which)
        return self.ok()
