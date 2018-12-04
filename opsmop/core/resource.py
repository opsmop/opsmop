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

from opsmop.core.fields import COMMON_FIELDS
import jinja2

class Resource(object):

    def __init__(self,  *args, **kwargs):
        self.setup(*args, **kwargs)

    def setup(self, **kwargs):
        self.kwargs = kwargs
        self.facts = None
        self.condition_stack = []
        self._variables = dict()
        self._scope = None
        self._field_spec = self.fields()
        self._field_spec.find_unexpected_keys(self)
        self._field_spec.load_parameters(self)

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
        results = self.get_variables()
        results.update(self.fact_context())
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

    def should_process_when(self):
        """
        A subclassable hook to conditionally skip a resource. Useful for lazy
        evaluation of runtime conditions that may change between resources
        """
        return True

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

    def has_tag(self, tags):
        my_tags = self.all_tags()
        if 'any' in my_tags:
            return True
        for t in tags:
            if t in my_tags:
                return True
        return False

    def conditions_true(self, context, validate=False):
        """
        Called by Executor code to decide if a resource is processable.
        """

        from opsmop.lookups.eval import Eval 
        from opsmop.lookups.lookup import Lookup

        if not self.should_process_when():
            return False

        when = self.when
        if when is None:
            return True
        if type(when) == str:
            try:
                return Eval(self.when).evaluate(self)
            except jinja2.exceptions.UndefinedError:
                if not validate:
                    raise
                # this value may need to late bind, we'll catch it later
                return True
            return res
        elif issubclass(type(when), Lookup):
            try:
                return when.evaluate(self)
            except jinja2.exceptions.UndefinedError:
                if not validate:
                    raise
                # this value may need to late bind, we'll catch it later
                return True
        else:
            return when

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

    def all_tags(self):
        result = []
        ptr = self
        while ptr is not None:
            if ptr.tags:
                result.extend(ptr.tags)
            ptr = ptr.parent()
        return result

    def pre(self):
        """
        user hook. called before executing a resource in Executor code
        """
        pass

    def post(self):
        """
        user hook. called after executing a resource in Executor code
        """
        pass
