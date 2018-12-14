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

from opsmop.lookups.lookup import Lookup
from opsmop.providers.provider import Provider


class Set(Provider):

    def plan(self):
        self.needs('set')
        self.copy_variables()

    def copy_variables(self):
        temp_items = dict()
        for (k,v) in self.extra_variables.items():
            if issubclass(type(v), Lookup):
                temp_items[k] = v.evaluate(self.resource)
            else:
                temp_items[k] = v
            self.echo("%s = %s" % (k,temp_items[k]))
        self.resource.update_parent_variables(temp_items)

    def skip_plan_stage(self):
        return True

    def apply(self):
        self.do('set')
        # we run this again so that any registered variables can be erased if so desired
        self.copy_variables()
        return self.ok()
