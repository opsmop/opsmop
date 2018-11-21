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

import stat
from pathlib import Path

# FIXME: TODO: this gets replaced with Facts.FileTests


class FileTests(object):

    def __init__(self, path):
        self.path = Path(path)
        self._exists = True
        try:
            self.stat = self.path.lstat()
        except FileNotFoundError:
            self._exists = False

    def exists(self):
        return self._exists
    
    def is_file(self):
        if self._exists:
            return self.path.is_file()
        return False
    
    def is_directory(self):
        if self._exists:
            return self.path.is_dir()
        return False

    def mode(self):
        if self._exists:
            return stat.S_IMODE(self.stat.st_mode)
        return None
    
    def owner(self):
        if self._exists:
            return self.path.owner()
        return None
    
    def group(self):
        if self._exists:
            return self.path.group()
        return None
