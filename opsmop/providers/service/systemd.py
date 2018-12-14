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

from opsmop.core.errors import ProviderError
from opsmop.providers.service.service import Service

STATUS = "systemctl status {name}"
IS_ENABLED = "systemctl is-enabled {name}"
START = "systemctl start {name}"
STOP  = "systemctl stop {name}"
RESTART = "systemctl restart {name}"
ENABLE = "systemctl enable {name}"
DISABLE = "systemctl disable {name}"

class Systemd(Service):

    def _get_status(self):
        status = self.test(STATUS.format(name=self.name), loose=True)
        if "could not be found" in status:
            self.error("service %s could not be found" % self.name)
        if "Active: active" in status:
            return "running"
        else:
            return "stopped"

    def _is_enabled(self, status):
        enabled = self.test(IS_ENABLED.format(name=self.name))
        if enabled is None:
            return False
        return enabled == "enabled"

    def plan(self):
        super().plan()

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
        if self.should('enable'):
            self.do('enable')
            self.run(ENABLE.format(name=self.name))
        elif self.should('disable'):
            self.do('disable')
            self.run(DISABLE.format(name=self.name))
        
        return self.ok()
