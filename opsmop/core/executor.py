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

import time

from opsmop.callbacks.callbacks import Callbacks
from opsmop.callbacks.common import CommonCallbacks
from opsmop.callbacks.event_stream import EventStreamCallbacks
from opsmop.callbacks.replay import ReplayCallbacks
from opsmop.client.user_defaults import UserDefaults
from opsmop.core.collection import Collection
from opsmop.core.context import APPLY, CHECK, VALIDATE, Context
from opsmop.core.errors import OpsMopStop
from opsmop.core.result import Result
from opsmop.core.role import Role
from opsmop.core.roles import Roles
from opsmop.inventory.host import Host
from opsmop.lookups.lookup import Lookup
from opsmop.push.batch import Batch
from opsmop.push.connections import ConnectionManager

# ---------------------------------------------------------------

class Executor(object):

    __slots__ = [ '_policies', '_tags', '_push', '_local_host', 'connection_manager' ]

    # ---------------------------------------------------------------

    def __init__(self, policies, local_host=None, tags=None, push=False):

        """
        The Executor runs a list of policies in either CHECK, APPLY, or VALIDATE modes
        """
  
        assert type(policies) == list
        self._policies = policies
        self._tags = tags
        self._push = push
        if local_host is None:
            local_host = Host("127.0.0.1")
        self._local_host = local_host
        self.connection_manager = None

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
        apply runs .plan() and then () provider methods and will actually
        make changes, as opposed to check(), which is a simulation.
        """
        self.run_all_policies(mode=APPLY)

    # ---------------------------------------------------------------

    def run_all_policies(self, mode=None):
        """
        Runs all policies in the specified mode
        """
        Context().set_mode(mode)
        for policy in self._policies:     
            if self._push:
                self.connection_manager = ConnectionManager(policy)
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
            Context().set_role(role)
            if not self._push:
                self.process_local_role(policy, role)
            else:
                self.process_remote_role(policy, role)
        Callbacks().on_complete(policy)

    # ---------------------------------------------------------------

    def validate_role(self, role):
        """
        Validates inputs for one role
        """

        def validate(resource):
            return resource.validate
        
        # resources and handlers must be processed seperately
        # the validate method will raise exceptions when problems are found
        original_mode = Context().mode()
        Context().set_mode(VALIDATE)
        role.walk_children(items=role.get_children('resources'), which='resources', fn=validate, tags=self._tags)
        role.walk_children(items=role.get_children('handlers'), which='handlers', fn=validate)
        if original_mode:
            Context().set_mode(original_mode)

    # ---------------------------------------------------------------

    def compute_max_hostname_length(self, hosts):
        hostname_length = 0
        for host in hosts:
            length = len(host.display_name())
            if length > hostname_length:
               hostname_length = length
        Callbacks().set_hostname_length(hostname_length)

    # ---------------------------------------------------------------

    def connect_to_all_hosts(self, hosts, role, max_workers):
        batch = Batch(hosts, batch_size=200)
        def host_connector(host):
            Context().set_host(host)
            self.connection_manager.connect(host, role)
        batch.apply_async(host_connector, max_workers=max_workers)

    # ---------------------------------------------------------------

    def run_roles_on_all_hosts(self, hosts, policy, role, batch_size):
        def role_runner(host):
            mode = Context().mode()
            self.connection_manager.remotify_role(host, policy, role, mode)
        batch = Batch(hosts, batch_size=batch_size)
        batch.apply(role_runner)

    # ---------------------------------------------------------------

    def process_summary(self, hosts):
        failures = Context().host_failures()
        failed_hosts = [ f for f in failures.keys() ]
        changed_hosts = [ h for h in hosts if h.actions() ]
        
        if len(changed_hosts):
            ReplayCallbacks().on_host_changed_list(hosts)

        if len(failed_hosts):
            ReplayCallbacks().on_terminate_with_host_list(failed_hosts)
            raise OpsMopStop()

    # ---------------------------------------------------------------

    def process_remote_role(self, policy, role):
        """
        Processes one role in any mode
        """

        import dill

        self.connection_manager.announce_role(role)
        hosts = role.inventory().hosts()
        self.connection_manager.add_hosts(hosts)

        batch_size = role.serial()
        max_workers = UserDefaults.max_workers()

        self.compute_max_hostname_length(hosts)
        self.connect_to_all_hosts(hosts, role, max_workers)
        self.connection_manager.prepare_for_role(role)
        self.run_roles_on_all_hosts(hosts, policy, role, batch_size)
        self.connection_manager.event_loop()
        self.process_summary(hosts)

    # ---------------------------------------------------------------

    def process_local_role(self, policy=None, role=None):

        host = self._local_host

        Context().set_host(host)

        role.pre()
        # set up the variable scope - this is done later by walk_handlers for lower-level objects in the tree
        policy.attach_child_scope_for(role)
        # tell the callbacks we are in validate mode - this may alter or quiet their output
        Callbacks().on_validate()
        # always validate the role in every mode (VALIDATE, CHECK ,or APPLY)
        self.validate_role(role)
        # skip the role if we need to
        if not role.conditions_true():
            Callbacks().on_skipped(role)
            return
        # process the tree for real for non-validate modes
        if not Context().is_validate():
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
        Callbacks().on_begin_role(role)
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
        Callbacks().on_begin_handlers()
        def execute_handler(handler):
            handler.pre()
            result = self.execute_resource(host=host, resource=handler, handlers=True)
            handler.post()
            return result
        role.walk_children(items=role.get_children('handlers'), which='handlers', fn=execute_handler, tags=self._tags)

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
        Callbacks().on_plan(provider)
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
        Callbacks().on_apply(provider)
        # take them
        result = provider.apply()
        if not handlers:
            # let the callbacks now we have taken some actions
            Callbacks().on_taken_actions(provider, provider.actions_taken)
            
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
        result.changed = provider.has_changed()
        # TODO: eliminate the actions class
        if result.changed:
            result.actions = [ x.do for x in provider.actions_taken ]
        else:
            result.actions = []

        # tell the callbacks about the result
        Callbacks().on_result(provider, result)

        # if there was a failure, handle it
        # (common callbacks should abort execution)
        #if fatal:
        #    Callbacks().on_fatal(provider, result)

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
            Context().add_signal(host, resource.signals)
            # tell the callbacks that a signal occurred
            Callbacks().on_signaled(resource, resource.signals)

    # ---------------------------------------------------------------

    def execute_resource(self, host, resource, handlers=False):
        """
        This handles the plan/apply intercharge for a given resource in the resource tree.
        It is called recursively via walk_children to run against all resources.
        """
        assert host is not None

        # we only care about processing leaf node objects
        if issubclass(type(resource), Collection):
            return

        # if in handler mode we do not process the handler unless it was signaled
        if handlers and not Context().has_seen_any_signal(host, resource.all_handles()):
            Callbacks().on_skipped(resource, is_handler=handlers)
            return

        # tell the callbacks we are about to process a resource
        # they may use this to print information about the resource
        Callbacks().on_resource(resource, handlers)

        # plan always, apply() only if not in check mode, else assume
        # the plan was executed.
        provider = self.do_plan(resource)
        assert provider is not None
        if Context().is_apply():
            self.do_apply(host, provider, handlers)
        else: # is_check
            self.do_simulate(host, provider)

        # if anything has changed, let the callbacks know about it
        self.signal_changes(host=host, provider=provider, resource=resource)
