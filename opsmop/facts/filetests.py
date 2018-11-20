from opsmop.facts.facts import Facts
from pathlib import Path
import os

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

