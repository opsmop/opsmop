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

from opsmop.callbacks.callbacks import Callbacks
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.resource import Resource


class Collection(Resource):

    """
    A collection is a type of resources that can contain other Resources.

    Example:

        Collection(
            Resource(...),
            Resource(...)
        )

    OR

        Collection(*resource_list)


    key-value arguments are available after the resource declaration, like:
    Collection(*resource_list, when=is_os_x)
    """

    def __init__(self, *args, **kwargs):
        self.setup(items=args, **kwargs)

    def fields(self):
        return Fields(
            self,
            items = Field(kind=list, of=Resource),
        )

    def add(self, what):
        if type(what) == list:
            self.items.extend(what)
        else:
            assert issubclass(type(what), Resource)
            self.items.append(what)

    def attach_child_scope_for(self, resource):
        """
        Used by walk_children, this marks each object as being a child of the parent scope
        """
        my_scope = self.scope()
        kid_scope = my_scope.deeper_scope_for(resource)
        resource.set_scope(kid_scope)

    def _on_walk(self):
        """
        A hook that fires on traversal of each object inside walk_children.
        """
        pass

    def get_children(self):
        """
        Returns child objects, mode may be 'resources' or 'handlers'
        """
        return self.items
