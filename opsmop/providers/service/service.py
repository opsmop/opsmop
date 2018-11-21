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

class Service(Provider):
    
    """
    Contains some fuzzy matching code all service instances should be able to use
    """

    def _is_started(self, status):
        if not status:
            return False
        return status in [ 'running', 'started' ]

    def _is_enabled(self, status):
        if not status:
            return False
        return status in [ 'running', 'started', 'stopped', 'enabled' ]

    def plan(self, on_boot=True):

        status = self._get_status()

        if self._is_started(status):
            if not self.started:
                self.needs('stop')
        else:
            if self.started:
                self.needs('start')
            elif self.restarted:
                self.needs('restart')

        if on_boot:
            # this part of the planner can be switched off for services
            # that don't support it, allowing them to not fail when they
            # are only able to execute part of the plan
            if self._is_enabled(status):
                if not self.enabled:
                    self.needs('disable')
            else:
                if self.enabled:
                    self.needs('enable')
