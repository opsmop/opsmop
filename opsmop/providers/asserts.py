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
from opsmop.providers.provider import Provider


class Asserts(Provider):

    def quiet(self):
        return True

    def skip_plan_stage(self):
        return True
 
    def apply(self):

        failed = False
        for expr in self.evals:
            result = None
            if issubclass(type(expr), Lookup):
                result = expr.evaluate(self.resource)
            elif type(expr) == str:
                result = Template.native_eval(expr, self.resource)
            else:
                result = expr
            self.echo("%s => %s" % (expr, result))
            if not result:
                failed = True
        
        variables = self.resource.get_variables()
        for (k,v) in self.variable_checks.items():
            if k not in variables:
                self.echo("%s is not defined" % k)
                failed = True
            else:
                actual = variables[k]
                if (v != actual):
                    self.echo("%s is %s (type:%s), should be %s (type:%s)" % (k, v, type(v), actual, type(actual)))
                    failed = True
                else:
                    self.echo("%s is %s" % (k, v))

        if not failed:
            return self.ok()
        else:
            return self.fatal("assertions failed")
