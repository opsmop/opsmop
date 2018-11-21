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
from opsmop.facts.platform import Platform
from opsmop.types.type import Type
from opsmop.core.errors import ValidationError

class Package(Type):

    def __init__(self, name=None, **kwargs):
        self.setup(name=name, **kwargs)

    def fields(self):
        return Fields(
            self,
            name = Field(kind=str, help="the name of the package to install"),
            version = Field(kind=str, default=None, help="what version to install"),
            latest = Field(kind=bool, default=False, help="if true, upgrade the package regardless of version"),
            absent = Field(kind=bool, default=False, help="if true, remove the package")
        )

    def validate(self):
        # FIXME: latest and absent are incompatible, as are version and absent
        pass

    def get_provider(self, method):
        if method == 'brew':
            from opsmop.providers.package.brew import Brew
            return Brew
        raise ValidationError("unsupported provider: %s" % method)

    def default_provider(self):
        return Platform.default_package_manager()
