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

import glob
import subprocess
import yaml

from opsmop.facts.facts import Facts
from opsmop.facts.filetests import FileTests

FACTS_PATTERN = "/etc/opsmop/facts.d/*.*"
FACTS_CACHE = None

def invalidate():
    global FACTS_CACHE
    FACTS_CACHE = None

class UserFactsGenerator(Facts):

    def __init__(self):
        super().__init__() 
        self.reload()

    def reload(self):
        global FACTS_CACHE
        FACTS_CACHE = dict()
        files = glob.glob(FACTS_PATTERN)
        for f in files:
            content = None
            if FileTests.executable(f):
                content = subprocess.check_output(f) 
            else:
                fd = open(f)
                content = fd.read()
                fd.close()
            parsed = self._parse(content)
            FACTS_CACHE.update(parsed)

    def _parse(self, content):
        return yaml.safe_load(content)

    def invalidate(self):
        global FACTS_CACHE
        FACTS_CACHE = None

    def get(self, *args):
        global FACTS_CACHE
        if FACTS_CACHE is None:
            self.reload()
        base = FACTS_CACHE
        for arg in args:
            base = base.get(arg)
        return base

    def constants(self):
        """
        This returns all facts that do not take parameters and is mostly for debug/demo
        purposes when someone wants to know the values of all the facts.
        See the 'opsmop-demo' repo in 'content/fact_demo.py' for an example or execute
        # python -m opsmop.core.facts.local to see values
        """
        return FACTS_CACHE

    def __getattr__(self, attr):
        if FACTS_CACHE and (attr in FACTS_CACHE):
            return FACTS_CACHE.get(attr)
        else:
            return object.__getattribute__(self, attr)

UserFacts = UserFactsGenerator()

if __name__ == "__main__":
    print(UserFacts.constants())
