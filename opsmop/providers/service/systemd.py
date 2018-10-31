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

from opsmop.providers.service.service import Service

STATUS = "brew services list | grep {name} -m1"
START = "brew services start {name}"
STOP  = "brew services stop {name}"
RESTART = "brew services restart {name}"

class Systemd(Service):

    def _get_status(self):
        return self.test(STATUS.format(name=self.name))

    def plan(self):
        super().plan(on_boot=False)

    def apply(self):

        # restart/start/stop
        if self.should('restart'):
            self.do('restart')
            self.run(RESTART.format(name=self.name))
        elif self.should('start'):
            self.do('start')
            self.run(START.format(name=self.name))
        elif self.should('stop'):
            self.do('stop')
            self.run(STOP.format(name=self.name))

        # enable/disable
        if self.should('enable') and not self.should('start'):
            self.do('enable')
            self.error("brew does not support enablement")

        elif self.should('disable') and not self.should('stop'):
            self.do('disable')
            self.error("brew does not support disablement")
        
        return self.ok()
