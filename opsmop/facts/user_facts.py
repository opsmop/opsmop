from opsmop.core.common import memoize
from opsmop.facts.facts import Facts
from opsmop.facts.filetests import FileTests
import subprocess
import glob
import yaml

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