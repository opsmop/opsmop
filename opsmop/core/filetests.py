import os
from pathlib import Path
import stat

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
