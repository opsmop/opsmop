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

    def _on_walk(self, context):
        """
        A hook that fires on traversal of each object inside walk_children.
        """
        pass

    def get_children(self, mode):
        """
        Returns child objects, mode may be 'resources' or 'handlers'
        """
        return self.items

    def walk_children(self, items=None, context=None, which=None, mode=None, fn=None, handlers=False, tags=None):

        """
        A relatively complex iterator used by Executor() code.
        Walks the entire object tree calling fn() on each element.
        
        items - the kids to start the iteration with
        context - a Context() object for callback tracking
        which - 'resources' or 'handlers'
        mode - 'validate', 'check', or 'apply'
        fn - the function to call on each object
        """

        self._on_walk(context)
        items_type = type(items)
 
        if items is None:
            return

        validate = (mode == 'validate')

        def maybe(v):
            # we'll visit every resource but only call the function on items if tags are *not* engaged
            if not tags or v.has_tag(tags):
                fn(v)
       
        if issubclass(items_type, Collection):            
            self.attach_child_scope_for(items)
            proceed = items.conditions_true(context, validate=validate)
            if proceed:
                return items.walk_children(items=items.get_children(mode), mode=mode, which=which, context=context, fn=fn, tags=tags)
            else:
                context.on_skipped(items, is_handler=handlers)

        elif issubclass(items_type, Resource):
            self.attach_child_scope_for(items)
            if items.conditions_true(context, validate=validate):
                return maybe(items)
            else:
                context.on_skipped(items, is_handler=handlers)

        elif items_type == list:
            for x in items:        
                self.attach_child_scope_for(x)
                if x.conditions_true(context, validate=validate):
                    if issubclass(type(x), Collection):
                        x.walk_children(items=x.get_children(mode), mode=mode, which=which, context=context, fn=fn, tags=tags)
                    else:
                        maybe(x)
                else:
                    context.on_skipped(items, is_handler=handlers)

        elif items_type == dict:
            for (k,v) in items.items():
                self.attach_child_scope_for(v)
                if v.conditions_true(context, validate=validate):
                    if issubclass(type(v), Collection):
                        items.walk_children(items=v.get_children(mode), mode=mode, which=which, context=context, fn=fn, tags=tags)
                    else:
                        v.handles = k
                        maybe(v)
                else:
                    context.on_skipped(items, is_handler=handlers)
