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

from opsmop.core.template import Template
from opsmop.lookups.lookup import Lookup


class Eval(Lookup):

    """
    when=Eval("a > b")
    """

    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def evaluate(self, resource):
        return Template.native_eval(self.expr, resource)

    def __str__(self):
        return "Eval: <'%s'>" % self.expr

    def to_dict(self):
        return dict(cls=self.__class__.__name__, expr=self.expr)
