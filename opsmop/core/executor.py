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

from opsmop.core.collection import Collection
from opsmop.core.context import Context, VALIDATE, APPLY, CHECK
from opsmop.core.result import Result
from opsmop.lookups.lookup import Lookup
from opsmop.inventory.host import Host
from opsmop.callbacks.callbacks import Callbacks

# ---------------------------------------------------------------

class Executor(object):

    __slots__ = [ '_policies', '_tags', '_local' ]

    # ---------------------------------------------------------------

    def __init__(self, policies, tags=None, local=True):

        """
        The Executor runs a list of policies in either CHECK, APPLY, or VALIDATE modes
        """
  
        assert type(policies) == list
        self._policies = policies
        self._tags = tags
        self._local = local

    # ---------------------------------------------------------------

    def validate(self):
        """
        Validate runs the .validate() method on every resource to check for argument consistency.
        This can catch inconsistent arguments and missing files
        """
        self.run_all_policies(mode=VALIDATE)

    # ---------------------------------------------------------------

    def check(self):
        """
        check runs the .plan() method on every resource tree and reports what resources would
        be changed, but does not make changes.  This is a dry-run mode.
        """
        self.run_all_policies(mode=CHECK)

    # ---------------------------------------------------------------

    def apply(self):
        """
        apply runs .plan() and then .apply() provider methods and will actually
        make changes, as opposed to check(), which is a simulation.
        """
        self.run_all_policies(mode=APPLY)

    # ---------------------------------------------------------------

    def run_all_policies(self, mode=None):
        """
        Runs all policies in the specified mode
        """
        Context.set_mode(mode)
        for policy in self._policies:     
            self.run_policy(policy=policy)


    # ---------------------------------------------------------------

    def run_policy(self, policy=None):
        """
        Runs one specific policy in VALIDATE, CHECK, or APPLY mode
        """
        # assign a new top scope to the policy object.
        policy.init_scope()
        roles = policy.get_roles()
        for role in roles.items:
            self.process_role(policy, role)
        Callbacks.on_complete(policy)

    # ---------------------------------------------------------------

    def validate_role(self, role):
        """
        Validates inputs for one role
        """

        def validate(resource):
            return resource.validate
        
        # resources and handlers must be processed seperately
        # the validate method will raise exceptions when problems are found
        original_mode = Context.mode()
        Context.set_mode(VALIDATE)
        role.walk_children(items=role.get_children('resources'), which='resources', fn=validate, tags=self._tags)
        role.walk_children(items=role.get_children('handlers'), which='handlers', fn=validate)
        if original_mode:
            Context.set_mode(original_mode)

    # ---------------------------------------------------------------

    def process_role(self, policy, role):
        """
        Processes one role in any mode
        """


        if self._local:
            hosts = [ Host("127.0.0.1") ]
        else:
            hosts = role.inventory().hosts()

        for host in hosts:
            self.process_role_for_host(host, policy, role)

    def process_role_for_host(self, host, policy, role):

        Context.set_host(host)

        if host.name == "127.0.0.1":

            self.process_role_internal(host, policy, role, local=True)

        else:

            # FIXME: IMPLEMENT / BOOKMARK
            # here's where we would call the remote version.
            # which is just a wrapper around the same function

            # be sure to set Context and Callback objects up correctly
            # and then copy over signals from Contexts returns when done.

            raise exceptions.NotImplementedError()

    def process_role_internal(self, host, policy, role, local=True):
        
        if not local:
            # FIXME: not implemented
            self.use_remote_callbacks()
        
        role.pre()
        # set up the variable scope - this is done later by walk_handlers for lower-level objects in the tree
        policy.attach_child_scope_for(role)
        # tell the callbacks we are in validate mode - this may alter or quiet their output
        Callbacks.on_validate()
        # always validate the role in every mode (VALIDATE, CHECK ,or APPLY)
        self.validate_role(role)
        # skip the role if we need to
        if not role.conditions_true():
            Callbacks.on_skipped(role)
            return
        # process the tree for real for non-validate modes
        if not Context.is_validate():
            self.execute_role_resources(host, role)
            self.execute_role_handlers(host, role)
        # run any user hooks
        role.post()


    # ---------------------------------------------------------------

    def execute_role_resources(self, host, role):
        """ 
        Processes non-handler resources for one role for CHECK or APPLY mode
        """
        # tell the context we are processing resources now, which may change their behavior
        # of certain methods like on_resource()
        Callbacks.on_begin_role(role)
        def execute_resource(resource):
            # execute each resource through plan() and if needed apply() stages, but before and after
            # doing so, run any user pre() or post() hooks implemented on that object.
            resource.pre()
            result = self.execute_resource(host=host, resource=resource)
            resource.post()
            return result
        role.walk_children(items=role.get_children('resources'), which='resources', fn=execute_resource, tags=self._tags)

    # ---------------------------------------------------------------

    def execute_role_handlers(self, host, role):
        """
        Processes handler resources for one role for CHECK or APPLY mode
        """
        # see comments for prior method for details
        Callbacks.on_begin_handlers()
        def execute_handler(handler):
            handler.pre()
            result = self.execute_resource(host=host, resource=handler, handlers=True)
            handler.post()
            return result
        role.walk_children(items=role.get_children('handlers'), which='handlers', fn=execute_handler, tags=self._tags)

    # ---------------------------------------------------------------

    def is_collection(self, resource):
        """
        Is the resource a collection?
        """
        return issubclass(type(resource), Collection)

    # ---------------------------------------------------------------

    def do_plan(self, resource):
        """
        Ask a resource for the provider, and then see what the planned actions should be.
        The planned actions are kept on the provider object. We don't need to obtain the plan.
        Return the provider.
        """
        # ask the resource for a provider instance
        provider = resource.provider()

        if provider.skip_plan_stage():
            return provider
        
        # tell the context object we are about to run the plan stage.
        Callbacks.on_plan(provider)
        # compute the plan
        provider.plan()
        # copy the list of planned actions into the 'to do' list for the apply method
        # on the provider
        provider.commit_to_plan()

        return provider

    # ---------------------------------------------------------------

    def do_apply(self, host, provider, handlers):
        """
        Once a provider has a plan generated, see if we need to run the plan.
        If so, also run any actions associated witht he apply step, which mostly means registering
        variables from apply results.
        """

        # some simple providers - like Echo, do not have a planning step
        # we will always run the apply step for them. For others, we will only
        # run the apply step if we have computed a plan
        if (not provider.skip_plan_stage()) and (not provider.has_planned_actions()):
            return False
                
        # indicate we are about take some actions
        Callbacks.on_apply(provider)
        # take them
        result = provider.apply()
        if not handlers:
            # let the callbacks now we have taken some actions
            Callbacks.on_taken_actions(provider, provider.actions_taken)
            
        # all Provider apply() methods need to return Result objects or raise
        # exceptions
        assert issubclass(type(result), Result)

        # the 'register' feature saves results into variable scope
        resource = provider.resource
        if resource.register is not None:
            provider.handle_registration(result)

        # determine if there was a failure
        fatal = False
        cond = resource.failed_when
        if cond is not None:
            if issubclass(type(cond), Lookup):
                fatal = cond.evaluate(resource)
                result.reason = cond
            else:
                fatal = cond
        elif result.fatal:
            fatal = True
        result.fatal = fatal

        # tell the callbacks about the result
        Callbacks.on_result(provider, result)

        # if there was a failure, handle it
        # (common callbacks should abort execution)
        if fatal:
            Callbacks.on_fatal(provider, result)

        return True

    # ---------------------------------------------------------------

    def do_simulate(self, host, provider):
        """
        This is the version of apply() that runs in CHECK mode.
        """
        provider.apply_simulated_actions()

    # ---------------------------------------------------------------

    def signal_changes(self, host=None, provider=None, resource=None):
        """
        If any events were signaled, add them to the context here.
        """    
        assert host is not None
        if not provider.has_changed():
            return
        if resource.signals:
            # record the list of all events signaled while processing this role
            Context.add_signal(host, resource.signals)
            # tell the callbacks that a signal occurred
            Callbacks.on_signaled(resource, resource.signals)

    # ---------------------------------------------------------------

    def execute_resource(self, host, resource, handlers=False):
        """
        This handles the plan/apply intercharge for a given resource in the resource tree.
        It is called recursively via walk_children to run against all resources.
        """
        assert host is not None
        # we only care about processing leaf node objects
        if self.is_collection(resource):
            return

        # if in handler mode we do not process the handler unless it was signaled
        if handlers and not Context.has_seen_any_signal(host, resource.all_handles()):
            Callbacks.on_skipped(resource, is_handler=handlers)
            return

        # tell the callbacks we are about to process a resource
        # they may use this to print information about the resource
        Callbacks.on_resource(resource, handlers)

        # plan always, apply() only if not in check mode, else assume
        # the plan was executed.
        provider = self.do_plan(resource)
        assert provider is not None
        if Context.is_apply():
            self.do_apply(host, provider, handlers)
        else: # is_check
            self.do_simulate(host, provider)

        # if anything has changed, let the callbacks know about it
        self.signal_changes(host=host, provider=provider, resource=resource)
