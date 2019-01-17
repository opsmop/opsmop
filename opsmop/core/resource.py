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

import jinja2

from opsmop.core.fields import COMMON_FIELDS
from opsmop.core.context import Context

class Resource(object):

    def __init__(self,  *args, **kwargs):
        self.setup(*args, **kwargs)
        self.run()

    def run(self):
        pass

    def setup(self, **kwargs):
        self.changed = False
        self.data = None
        self.rc = None

        self.kwargs = kwargs
        self.facts = None
        self.condition_stack = []
        self._variables = dict()
        self._scope = None
        self._field_spec = self.fields()
        self._field_spec.find_unexpected_keys(self)
        self._field_spec.load_parameters(self)

        # FIXME: load these up
        self.changed = False
        self.data = None

    def quiet(self):
        """ If true, surpresses some callbacks """
        return False

    def split_common_kwargs(self, kwargs):
        """
        Return a set of (original, common) dicts, where original contains
        any arguments specified in Fields for a resource (Type) and common
        includes the ones available to all types
        """

        from opsmop.core.fields import Fields

        common = dict()
        original = dict()
        for (k,v) in kwargs.items():
            if k in COMMON_FIELDS:
                common[k] = v
            else:
                original[k] = v
        return (original, common)

    def set_scope(self, scope):
        """
        Used by Executor code to assign the current scope.
        """
        self._scope = scope

    def scope(self):
        """
        Gets the scope object for this resource, which is assigned while executing the resource.
        Without a scope object, it is impossible to compute variables for use in template
        and conditional evaluation, hence the assert.
        """
        if self._scope is None:
            role = Context().role()
            role.attach_child_scope_for(self)
        return self._scope

    def top_level_resource(self):
        """
        Return the top resource in the resources tree, which should be a policy.
        """
        return self.scope().top_level_resource()

    def set_variables(self):
        """ 
        A method that can be defined on any resource class to provide extra variables to templating.
        This is used heavily in the opsmop-demo content. This does NOT actually store in variables.
        For this, see the update_parent_variables() method.
        """
        return dict()

    def policy(self):
        """
        Find the policy object at the top of the object tree.
        """
        return self.top_level_resource()

    def template_context(self):
        """
        Get the full Jinja2 context available for templating at this resource.
        This includes facts + variables
        """
        context = Context()
        results = self.get_variables()
        results.update(context.globals())
        results.update(self.fact_context())
        results.update(context.scope_variables())
        results.update(context.extra_vars())
        return results

    def fact_context(self):
        """
        Get the facts available inside templating for this resource.
        To keep things simple, we just ask the Policy.
        """
        return self.policy().fact_context()

    def get_children(self, method=None):
        """
        Returns the resources contained within this resource.  This won't
        normally have a value except for Collection subclasses.
        """
        return None

    def validate(self):
        """
        An optional hook, typically added to type code, that checks to
        make sure the arguments of a resource are sensical with each other.
        """
        pass

    def update_variables(self, variables):
        """
        This is called by the executor.  It mixes in variables from higher scopes
        allowing local variables to win.
        """
        self.scope().update_variables(variables)

    def update_parent_variables(self, variables):
        """
        Update variables at the parent scope.  This is used by the Set() resource
        and also 'register'
        """
        self.scope().update_parent_variables(variables)

    def role(self):
        """
        What's my role?
        """
        return self.scope().role()

    def get_variables(self):
        """
        Return the variables at the current scope.  Used in conditional evaluation
        and templating.
        """
        return self.scope().variables()

    def parent(self):
        parent_scope = self.scope().parent()
        if parent_scope is None:
            return None
        return parent_scope.resource()

    def all_handles(self):
        """
        Handles could be nested in collections, if so, find the handlers names that apply to this resource.
        """
        result = []
        ptr = self
        while ptr is not None:
            if ptr.handles:
                result.append(ptr.handles)
            ptr = ptr.parent()
        return result

    def to_dict(self):
        result = dict()
        result['cls']= self.__class__.__name__
        for (k,v) in self.kwargs.items():
            if hasattr(v, 'to_dict'):
                v = v.to_dict()
            result[k] = v
        return result
