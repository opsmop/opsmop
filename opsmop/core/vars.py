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

class VarsLoader(object):

    def __init__(self, role):

        """
        Allows for, inside of any role, access to self.vars.b, and the right thing is done
        regardless of whether the variable is defined via set_variables, as a role parameter,
        in python scope, or elsewhere
        """

        self.role = role

    #def __getattr__(self, x):
    #    variables = self.role.template_context()
    #    if x in variables:
    #        return variables[x]
    #    else:
    #        raise AttributeError
