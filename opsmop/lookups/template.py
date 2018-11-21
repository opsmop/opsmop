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

from opsmop.core.template import Template as CoreTemplate
from opsmop.lookups.lookup import Lookup

class Template(Lookup):

    """
    T() is a deferred lookup that evaluates a template at runtime, allowing variables
    established by Set() to be used. While some providers (like Echo) will template
    arguments automatically, most arguments in OpsMop must be explicitly templated
    with T. In the future T may also support some additional options.
    """

    def __init__(self, expr):
        super().__init__()
        self.expr=expr

    def evaluate(self, resource):
        return CoreTemplate.from_string(self.expr, resource)

    def __str__(self):
        return "T: <'%s'>" % self.expr

T = Template
