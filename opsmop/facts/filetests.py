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
import stat
import hashlib

from opsmop.facts.facts import Facts

class FileTestFacts(Facts):
    
    """
    As this evolves, facts can be dynamically injected into this base class based on platform, allowing a subclass
    for things like LinuxFacts. When this happens, we can have a "facts/" package.
    """

    def exists(self, fname):
        return os.path.exists(fname)
    
    def executable(self, fname):
        return os.path.isfile(fname) and os.access(fname, os.X_OK)
    
    def is_file(self, fname):
        from pathlib import Path

        if not self.exists(fname):
            return None
        return Path(fname).is_file()
    
    def is_directory(self, fname):
        from pathlib import Path

        if not self.exists(fname):
            return None
        return Path(fname).is_dir()

    def mode(self, fname):
        from pathlib import Path

        if not self.exists(fname):
            return None
        lstat = Path(fname).lstat()
        return stat.S_IMODE(lstat.st_mode)
    
    def owner(self, fname):
        from pathlib import Path

        if not self.exists(fname):
            return None
        return Path(fname).owner()
    
    def group(self, fname):
        from pathlib import Path

        if not self.exists(fname):
            return None
        return Path(fname).group()

    def checksum(self, fname, blocksize=65535):
        m = hashlib.sha256()
        with open(fname, "rb") as f:
            block = f.read(blocksize)
            while len(block) > 0:
                block = f.read(blocksize)
                m.update(block)
        return m.hexdigest()

    def string_checksum(self, msg):
        m = hashlib.sha256()
        m.update(msg.encode())
        return m.hexdigest()

    def same_contents(self, a, b):
        if not self.exists(b):
            return False
        m = hashlib.sha256()
        c1 = self.checksum(a)
        c2 = self.checksum(b)
        return (c1 == c2)        

FileTests = FileTestFacts()
