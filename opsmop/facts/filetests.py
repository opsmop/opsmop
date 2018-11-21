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
from pathlib import Path

from opsmop.facts.facts import Facts

# TODO: there are a LOT of facts to add yet!  We are just starting out
# in particular we also want to add /etc/opsmop/facts.d

class FileTestFacts(Facts):
    
    """
    As this evolves, facts can be dynamically injected into this base class based on platform, allowing a subclass
    for things like LinuxFacts. When this happens, we can have a "facts/" package.
    """

    def exists(self, fname):
        return os.path.exists(fname)
    
    def executable(self, fname):
        return os.path.isfile(fname) and os.access(fname, os.X_OK)

FileTests = FileTestFacts()
