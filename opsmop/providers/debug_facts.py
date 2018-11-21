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

from opsmop.providers.provider import Provider

class DebugFacts(Provider):

    def quiet(self):
        return True

    def verb(self):
        return "debugging constant facts..."

    def skip_plan_stage(self):
        return True
 
    def apply(self):
        
        # fact_instances return a dictionary of fact
        # instances such as:
        # dict(
        #     UserFacts: UserFacts
        #     Platform: Platform
        #     FileTest: FileTest
        # )

        context = self.resource.fact_context()

        for (k,v) in context.items():

            # for each fact instance, print a header
            # and then show the contant facts in
            # each (the facts that don't take)
            # parameters

            self.echo("---")
            self.echo("Facts Class: %s" % k)
            for (k2, v2) in v.constants().items():
                self.echo("  %s => %s" % (k2, v2))
            self.echo("note: other methods may exist that take parameters")

        return self.ok()
