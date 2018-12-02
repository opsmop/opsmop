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
import shutil
from pathlib import Path

from opsmop.core.errors import ProviderError
from opsmop.facts.filetests import FileTests
from opsmop.providers.provider import Provider

class Directory(Provider):

    # ---------------------------------------------------------------

    def plan(self):
        """ what actions are needed? """

        if self.recursive:
            raise ProviderError(self, "recursive is not implemented yet")
        if FileTests.is_file(self.name):
            raise ProviderError(self, f"destination path ({self.name}) is a file, uncertain how to proceed")

        exists = FileTests.exists(self.name)

        if self.absent:
            # removal actions?
            if not exists:
                return
            elif FileTests.is_directory(self.name):
                self.needs('rmdir')
        else:
            # creation?
            if not exists:
                self.needs('mkdir')

            # metadata?
            if self.owner and (self.recursive or not exists or (FileTests.owner(self.name) != self.owner)):
                self.needs('chown')
            elif self.group and (self.recursive or not exists or (FileTests.group(self.name) != self.group)):
                self.needs('chgrp')
            elif self.mode and (self.recursive or not exists or (FileTests.mode(self.name) != self.mode)):
                 self.needs('chmod')

    # ---------------------------------------------------------------

    def apply(self):
        """ perform planned actions """

        if self.should('rmdir'):
            self.do('rmdir')
            Path(self.name).rmdir()
            return self.ok()

        if self.should('mkdir'):
            self.do('mkdir')
            if self.mode:
                os.makedirs(self.name, self.mode)
            else:
                os.makedirs(self.name)

        # TODO: move the guts of these into something like a FileUtils class
        if self.should('chmod'):
            self.do('chmod')
            os.chmod(self.name, self.mode)

        if self.should('chown'):
            self.do('chown')
            try:
                shutil.chown(self.name, user=self.owner)
            except PermissionError:
                return self.fatal("chown failed")

        if self.should('chgrp'):
            self.do('chgrp')
            try:
                shutil.chown(self.name, group=self.group)
            except PermissionError:
                return self.fatal("chgrp failed")

        return self.ok()
