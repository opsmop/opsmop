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
from opsmop.types.type import Type


class Asserts(Type):

    def __init__(self, *args, **kwargs):
        (original, common) = self.split_common_kwargs(kwargs)
        self.setup(evals=args, variable_checks=original, **common)
        if self.auto_dispatch:
            self.run()

    def fields(self):
        return Fields(
            self,
            evals = Field(kind=list),
            variable_checks = Field(kind=dict)
        )

    def default_provider(self):
        from opsmop.providers.asserts import Asserts
        return Asserts
