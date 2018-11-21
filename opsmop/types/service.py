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
from opsmop.facts.platform import Platform
from opsmop.core.errors import ValidationError

class Service(Type):

    """
    Represents a OS background service.
    """

    def __init__(self, name=None, **kwargs):
        self.setup(name=name, **kwargs)

    def fields(self):
        return Fields(
            self,
            name = Field(kind=str),
            started = Field(kind=bool, default=True),
            enabled = Field(kind=bool, default=True),
            restarted = Field(kind=bool, default=False),
        )

    def validate(self):
        pass

    def get_provider(self, method):
        if method == 'brew':
            from opsmop.providers.service.brew import Brew
            return Brew
        raise ValidationError("unsupported provider: %s" % method)

    def default_provider(self):
        return Platform.default_service_manager()
