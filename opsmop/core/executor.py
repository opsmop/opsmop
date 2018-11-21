from opsmop.core.result import Result
from opsmop.core.context import Context
from opsmop.core.policy import Policy
from opsmop.core.scope import Scope
from opsmop.lookups.eval import Eval
from opsmop.lookups.lookup import Lookup
from opsmop.core.collection import Collection

# ---------------------------------------------------------------

# Run mode constants.

CHECK='check'
APPLY='apply'
VALIDATE='validate'

# ---------------------------------------------------------------

class Executor(object):

    __slots__ = [ '_policies', '_callbacks' ]

    # ---------------------------------------------------------------

    def __init__(self, policies=None, callbacks=None):

        """
        The Executor runs a list of policies in either CHECK, APPLY, or VALIDATE modes
        """
  
        assert type(policies) == list
        assert type(callbacks) == list
        self._policies = policies
        self._callbacks = callbacks

    # ---------------------------------------------------------------

    def validate(self):
        """
        Validate runs the .validate() method on every resource to check for argument consistency.
        This can catch inconsistent arguments and missing files
        """
        return self.run_all_policies(mode=VALIDATE)

    # ---------------------------------------------------------------

    def check(self):
        """
        check runs the .plan() method on every resource tree and reports what resources would
        be changed, but does not make changes.  This is a dry-run mode.
        """
        return self.run_all_policies(mode=CHECK)

    # ---------------------------------------------------------------

    def apply(self):
        """
        apply runs .plan() and then .apply() provider methods and will actually
        make changes, as opposed to check(), which is a simulation.
        """
        return self.run_all_policies(mode=APPLY)

    # ---------------------------------------------------------------

    def run_all_policies(self, mode):
        """
        Runs all policies in the specified mode
        """

        contexts = []
        context = None

        for policy in self._policies:
            # the context holds some types of state, such as signalled events
            # and is cleared between each policy execution
            context = Context(callbacks=self._callbacks)
            # actual running of the policy here:
            self.run_policy(policy=policy, context=context, mode=mode)
            contexts.append(context)

        return contexts

    # ---------------------------------------------------------------

    def run_policy(self, policy=None, context=None, mode=None):
        """
        Runs one specific policy in VALIDATE, CHECK, or APPLY mode
        """
        
        assert issubclass(type(policy), Policy)
        assert issubclass(type(context), Context)
        assert mode in [ 'validate', 'check', 'apply' ]

        # assign a new top scope to the policy object.
        policy.init_scope(context)

        roles = policy.get_roles()
        # this is a Roles object, not a list
        for role in roles.items:
            self.process_role(policy, role, context=context, mode=mode)
        
        context.on_complete(policy)

    # ---------------------------------------------------------------

    def validate_role(self, role, context=None):
        """
        Validates inputs for one role
        """

        def validate(resource):
            return resource.validate
        
        # resources and handlers must be processed seperately
        # the validate method will raise exceptions when problems are found
        role.walk_children(items=role.get_children('resources'), context=context, which='resources', fn=validate, mode=VALIDATE)
        role.walk_children(items=role.get_children('handlers'), context=context, which='handlers', fn=validate, mode=VALIDATE)

    # ---------------------------------------------------------------

    def process_role(self, policy, role, context=None, mode=None):
        """
        Processes one role in any mode
        """
        # run any user hooks
        role.pre()
        # set up the variable scope - this is done later by walk_handlers for lower-level objects in the tree
        policy.attach_child_scope_for(role)
        # tell the callbacks we are in validate mode - this may alter or quiet their output
        context.on_validate()
        # always validate the role in every mode (VALIDATE, CHECK ,or APPLY)
        self.validate_role(role, context=context)
        # skip the role if we need to
        if not role.conditions_true(context):
            context.on_skipped(role)
            return
        # process the tree for real for non-validate modes
        if mode != VALIDATE:
            self.execute_role_resources(role, context=context, mode=mode)
            self.execute_role_handlers(role, context=context, mode=mode)
        # run any user hooks
        role.post()

    # ---------------------------------------------------------------

    def execute_role_resources(self, role, context=None, mode=None):
        """ 
        Processes non-handler resources for one role for CHECK or APPLY mode
        """
        # tell the context we are processing resources now, which may change their behavior
        # of certain methods like on_resource()
        context.on_begin()
        def execute_resource(resource):
            # execute each resource through plan() and if needed apply() stages, but before and after
            # doing so, run any user pre() or post() hooks implemented on that object.
            resource.pre()
            result = self.execute_resource(resource=resource, context=context, mode=mode)
            resource.post()
            return result
        role.walk_children(items=role.get_children('resources'), context=context, which='resources', fn=execute_resource, mode=mode)

    # ---------------------------------------------------------------

    def execute_role_handlers(self, role, context=None, mode=None):
        """
        Processes handler resources for one role for CHECK or APPLY mode
        """
        # see comments for prior method for details
        context.on_begin_handlers()
        def execute_handler(handler):
            handler.pre()
            result = self.execute_resource(resource=handler, context=context, mode=mode, handlers=True)
            handler.post()
            return result
        role.walk_children(items=role.get_children('handlers'), context=context, which='handlers', fn=execute_handler, mode=mode)

    # ---------------------------------------------------------------

    def is_collection(self, resource):
        """
        Is the resource a collection?
        """
        return issubclass(type(resource), Collection)

    # ---------------------------------------------------------------

    def plan(self, resource, context):
        """
        Ask a resource for the provider, and then see what the planned actions should be.
        The planned actions are kept on the provider object. We don't need to obtain the plan.
        Return the provider.
        """
        # ask the resource for a provider instance
        provider = resource.provider()
        # the provider needs to have access to the context so it can invoke
        # callbacks, such as on_echo()
        provider.set_context(context)

        if not provider.skip_plan_stage():
            # tell the context object we are about to run the plan stage.
            context.on_plan(provider)
            # compute the plan
            provider.plan()
            context.on_planned_actions(provider, provider.actions_planned)
            # copy the list of planned actions into the 'to do' list for the apply method
            # on the provider
            provider.commit_to_plan()

        return provider

    # ---------------------------------------------------------------

    def do_apply(self, provider, context, handlers):
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
        context.on_apply(provider)
        # take them
        result = provider.apply()
        if not handlers:
            # let the callbacks now we have taken some actions
            context.on_taken_actions(provider, provider.actions_taken)
            
        # all Provider apply() methods need to return Result objects or raise
        # exceptions
        assert result is not None
        assert issubclass(type(result), Result)

        # the 'register' feature saves results into variable scope
        if provider.resource.register is not None:
            provider.handle_registration(context=context, result=result)

        # tell the callbacks about the result
        context.on_result(result)
        if result.fatal:
            context.on_fatal(result)

        return True

    # ---------------------------------------------------------------

    def do_simulate(self, provider, context):
        """
        This is the version of apply() that runs in CHECK mode.
        """
        provider.apply_simulated_actions()

    # ---------------------------------------------------------------

    def signal_changes(self, provider, resource=None, context=None):
        """
        If any events were signalled, add them to the context here.
        """
        if not provider.has_changed():
            return
        if resource.signals:
            # record the list of all events signalled while processing this role
            context.add_signal(resource.signals)
            # tell the callbacks that a signal occurred
            context.on_flagged(resource.signals)

    # ---------------------------------------------------------------

    def execute_resource(self, resource=None, context=None, mode=None, handlers=False):
        """
        This handles the plan/apply intercharge for a given resource in the resource tree.
        It is called recursively via walk_children to run against all resources.
        """
        
        assert resource is not None
        assert context is not None
        assert mode in [ CHECK, APPLY, VALIDATE ]
        assert handlers in [ True, False ]

        # we only care about processing leaf node objects
        if self.is_collection(resource):
            return

        # if in handler mode we do not process the handler unless it was signalled
        if handlers and not context.has_seen_any_signal(resource.all_handles()):
            context.on_skipped(resource, is_handler=handlers)
            return

        # tell the callbacks we are about to process a resource
        # they may use this to print information about the resource
        context.on_resource(resource, handlers)

        # plan always, apply() only if not in check mode, else assume
        # the plan was executed.
        provider = self.plan(resource, context)
        assert provider is not None
        if mode == APPLY:
            self.do_apply(provider, context, handlers)
        else:
            self.do_simulate(provider, context)

        # if anything has changed, let the callbacks know about it
        self.signal_changes(provider=provider, resource=resource, context=context)




