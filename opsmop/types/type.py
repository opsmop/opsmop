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

import inspect
import json

from opsmop.callbacks.callbacks import Callbacks
from opsmop.core.context import Context
from opsmop.core.resource import Resource
from opsmop.core.result import Result
from opsmop.core.template import Template
from opsmop.lookups.lookup import Lookup


class Type(Resource):

    def validate(self):
        pass

    def run(self):

        Callbacks().on_resource(self)

        provider = self.do_plan()
        if Context().is_apply():
            result = self.do_apply(provider)
        else:
            result = self.do_simulate(provider)
        # copy over results
        self.changed = result.changed
        self.data = result.data
        self.rc = result.rc

    def provider(self):
        """
        Given a facts instance, obtain the provider used to fulfill the resource. 
        """

        cls = None
        if 'method' in self.kwargs:
            method = self.kwargs.get('method')
            cls = self.get_provider(method)
        else:
            cls = self.default_provider()
        inst = cls(self)
        self.copy_fields_to_provider(inst)
        self.resolve_provider_fields(inst)
        return inst

    # ---------------------------------------------------------------

    def get_provider(self, provider):
        return None

    # ---------------------------------------------------------------

    def copy_fields_to_provider(self, provider):
        """
        Transfer fields like self.name or self.owner or the provider object.
        """

        if self._field_spec is None:
            # this is for types like Set() that have unrestricted parameters
            for (k,v) in self.kwargs.items():
                setattr(provider, k, v)
        else:
            for (k, spec) in self._field_spec.fields.items():
                value = getattr(self, k)
                setattr(provider, k, value)

    # ---------------------------------------------------------------

    def resolve_provider_fields(self, provider):

        for (k, spec) in self._field_spec.fields.items():
            value = getattr(provider, k)
            if issubclass(type(value), Lookup) and not spec.lazy:
                value = value.evaluate(provider.resource)
            setattr(provider, k, value)

    # ---------------------------------------------------------------

    def context(self):
        return self._context

    # ---------------------------------------------------------------

    def set_context(self, value):
        self._context = value

    # ---------------------------------------------------------------

    def template(self, msg):
        return Template.from_string(msg, self)

    # ---------------------------------------------------------------

    def template_file(self, path):
        return Template.from_file(path, self)

    # ---------------------------------------------------------------

    def __str__(self):
        str_name = ""
        if 'name' in self.kwargs:
            str_name = self.__class__.__name__ + ": %s" % self.kwargs['name']
        else:
            str_name = self.__class__.__name__
        return str_name

   # ---------------------------------------------------------------

    def do_plan(self):
        """
        Ask a resource for the provider, and then see what the planned actions should be.
        The planned actions are kept on the provider object. We don't need to obtain the plan.
        Return the provider.
        """

        from opsmop.callbacks.callbacks import Callbacks

        # ask the resource for a provider instance
        provider = self.provider()

        if provider.skip_plan_stage():
            return provider
        
        # tell the context object we are about to run the plan stage.
        Callbacks().on_plan(provider)
        # compute the plan
        provider.plan()
        # copy the list of planned actions into the 'to do' list for the apply method
        # on the provider
        provider.commit_to_plan()

        return provider

    # ---------------------------------------------------------------

    def do_apply(self, provider):
        """
        Once a provider has a plan generated, see if we need to run the plan.
        """

        from opsmop.callbacks.callbacks import Callbacks

        # some simple providers - like Echo, do not have a planning step
        # we will always run the apply step for them. For others, we will only
        # run the apply step if we have computed a plan
        if not provider.has_planned_actions():
            if not provider.skip_plan_stage():
                return Result(provider=provider, changed=False, data=None)
                
        # indicate we are about take some actions
        Callbacks().on_apply(provider)
        # take them
        result = provider.apply()
        Callbacks().on_taken_actions(provider, provider.actions_taken)
            
        # all Provider apply() methods need to return Result objects or raise
        # exceptions
        assert issubclass(type(result), Result)

        # the 'register' feature saves results into variable scope
        resource = provider.resource
        
        # determine if there was a failure
        fatal = False
        cond = resource.failed_when
        if cond is not None:
            if issubclass(type(cond), Lookup):
                fatal = cond.evaluate(resource)
                result.reason = cond
            elif callable(cond):
                fatal = cond(result)
            else:
                fatal = cond
        elif result.fatal:
            fatal = True
        result.fatal = fatal
        result.changed = provider.has_changed()
        # TODO: eliminate the actions class
        if result.changed:
            result.actions = [ x.do for x in provider.actions_taken ]
        else:
            result.actions = []

        Callbacks().on_result(provider, result)

        return result

    # ---------------------------------------------------------------

    def do_simulate(self, provider):
        """
        This is the version of apply() that runs in CHECK mode.
        """
        return provider.apply_simulated_actions()
