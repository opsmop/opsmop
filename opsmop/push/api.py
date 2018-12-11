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
from runpy import run_path

from opsmop.core.executor import Executor

class PushApi(object):

    __slots__ = [ '_policies']

    def __init__(self, policies=None):

        assert type(policies) == list
        self._policies = policies
              
    def check(self):
        """
        This is dry-run mode
        """
        return Executor(policies=self._policies, local=False).check()

    def apply(self):
        """
        This is live-configuration mode.
        """
        return Executor(policies=self._policies, local=False).apply()
