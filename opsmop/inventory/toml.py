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
import toml
from opsmop.core.errors import InventoryError
from opsmop.inventory.inventory import Inventory

class TomlInventory(Inventory):

    def __init__(self):
        super().__init__()

    def load(self, filename):

        path = os.path.expanduser(os.path.expandvars(filename))
        if not os.path.exists(path):
            raise InventoryError(msg="TOML inventory does not exist at: %s" % path)
        data = open(path).read()
        data = toml.loads(data)
        self.accumulate(data)
        return self

        

