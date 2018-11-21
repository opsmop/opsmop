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

from opsmop.core.errors import ValidationError

class Validators(object):

    def __init__(self, resource):
        self.resource = resource

    def mutually_exclusive(self, fields):
        values = [ f for f in fields if getattr(self.resource, f) ]
        if len(values) > 1:
            raise ValidationError(self.resource, "fields are mutually exclusive: %s" % fields)

    def path_exists(self, path):
        if path is None:
            return False
        # FIXME use the FileTest module, don't duplicate this here
        path = os.path.expandvars(os.path.expanduser(path))
        if not os.path.exists(path):
            raise ValidationError(self.resource, "path does not exist: %s" % path)
