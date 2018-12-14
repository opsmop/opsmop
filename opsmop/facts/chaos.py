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

import platform
import random as prandom

from opsmop.core.common import memoize
from opsmop.facts.facts import Facts

prandom.seed()

# TODO: there are a LOT of facts to add yet!  We are just starting out
# contributions are very welcome

class ChaosFacts(Facts):
    
    """
    As this evolves, facts can be dynamically injected into this base class based on platform, allowing a subclass
    for things like LinuxFacts. When this happens, we can have a "facts/" package.
    """

    def random(self):
        return prandom.random()

    def choice(self, args):
        return prandom.choice(*args)

    def constants(self):
        """
        This returns all facts that do not take parameters .
        Mostly for the DebugFacts() implementation
        """
        return dict(
            random = self.random(),
        )

    def invalidate(self):
        pass

Chaos = ChaosFacts()

if __name__ == "__main__":
    print(Chaos.constants())
