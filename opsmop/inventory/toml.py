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

import logging
import os

import toml

from opsmop.core.errors import InventoryError
from opsmop.inventory.inventory import Inventory

logger = logging.getLogger('toml')


class TomlInventory(Inventory):

    def __init__(self, filename):
        super().__init__()
        self._path = os.path.expanduser(os.path.expandvars(filename))

    def load(self):
        if self._loaded:
            return self
        if not os.path.exists(self._path):
            raise InventoryError(msg="TOML inventory does not exist at: %s" % self._path)
        data = open(self._path).read()
        data = toml.loads(data)
        self.accumulate(data)
        return self
