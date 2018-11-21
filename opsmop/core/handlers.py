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

from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.resource import Resource
from opsmop.core.resources import Resources

class Handlers(Resources):

    def __init__(self, **kwargs):
        handlers = []
        for (k,v) in kwargs.items():
            v.handles = k
            handlers.append(v)
        self.setup(items=handlers)

    def fields(self):
        return Fields(
            self,
            items = Field(kind=list, of=Resource),
        )
