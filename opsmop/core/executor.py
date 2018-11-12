from opsmop.core.visitor import Visitor
from opsmop.client.facts import Facts
from opsmop.core.result import Result
from opsmop.core.errors import ProviderError
from opsmop.conditions.var import V

# WARNING: this file is kind of a mess at the moment, but largely works.
# once stabilized, it will get cleaned up lots.

# FIXME: we need a Context object to keep from passing so many params to each
# method.

class Executor(object):

    def __init__(self, policy, callbacks):
        """
        Given a policy and a callback class, the executor can be used as the launching
        point for all operations.  For more API-centric evaluation, supply a callback
        that produces a minimum of output, or even no output.
        """
        self.policy = policy
        self.callbacks = callbacks

        self.signals = []
        
        self.all = []
        self.successful = []
        self.unchanged = []
        self.changed = []

    # ==========================================================================
    # BEGIN CLI ENTRY POINTS

    def show(self):
        """
        Dump the JSON representation of the policy.
        This is relatively low level output of an internal data structure
        """
        data = self.policy.to_dict()
        self.callbacks.on_local_show(self.policy, data)

    def apply(self):
        """
        Apply (execute) the local policy, making any required
        changes.
        """
        self.callbacks.set_dry_run(False)
        self._run(dry_run=False)

    def check(self):
        """
        Apply (execute) the local policy, but only the planning steps.
        Share information about what resources would execute their apply
        stages. This is a dry-run mode.
        """
        self.callbacks.set_dry_run(True)
        self._run(dry_run=True)
    
    #============================================================================
    # MAIN LOOP

    def _run(self, dry_run=True):
        """
        The _run method contains high-level tree traversal code that walks the
        resources. Whether apply stages are executed is based on whether dry_run
        is set.
        """

        facts = Facts()
        visitor = Visitor(self.policy, facts)

        self.signals = []

        self.callbacks.on_resources_start(self.policy)

        visitor = Visitor(self.policy, None)
        V.set_variables(self.policy.variables)
        for item in visitor.walk_resources():
            resource = item
            resource.set_variables(V.all_variables())
            resource.validate()
            self.callbacks.on_validated(resource)

        for item in visitor.walk_handlers():
            resource = item
            resource.set_variables(V.all_variables())
            resource.validate()
            self.callbacks.on_validated(resource, handler=True)

        for item in visitor.walk_resources():
            resource = item
            resource.set_facts(facts)
            resource.set_variables(V.all_variables())
            self.execute_resource(resource, facts, dry_run=dry_run)

        self.callbacks.on_handlers_start(self.policy)

        for item in visitor.walk_handlers():
            resource = item           
            resource.set_facts(facts)
            resource.set_variables(V.all_variables())
            if resource.handles in self.signals:
                self.execute_resource(resource, facts, dry_run=dry_run, handlers=True)

        self.callbacks.on_complete(self.policy)
        return

    # FIXME: this isn't used yet

    def validate_resources(self):

        """
        Check resources for internal consistency.
        Validation does not use facts about the system
        """
        

        
    def execute_resource(self, resource, facts, dry_run=True, handlers=False):
        """
        While walking the resources is overseen by the _run method,
        this method is called on each individual resource, computing
        the plan() stages and if neccessary the apply() stages, which
        happens in non-dry-run modes.  This method is somewhat long
        because there are a wide variety of callback events, many of
        which may perform no action, but are included to allow
        flexibility.
        """


        self.callbacks.on_resource_begin(self.policy, resource)
        conditions = resource.get_condition_stack()
        for cond in conditions:
            if not cond.evaluate(facts):
                self.callbacks.on_skipped(self.policy, resource, cond)
                return

        # ask the resource if any changes are needed.  This operation
        # may take some time as it may need to execute some commands.
        provider = resource.provider(facts)
        if handlers:
            self.callbacks.on_actions_handler_begin(self.policy, resource, provider)
        provider.set_callbacks(self.callbacks)
        resource.copy_fields_to_provider(provider)
        provider.plan(facts)

        self.callbacks.on_actions_apply_begin(self.policy, resource, provider, provider.actions_planned)
        # approve actions - FIXME: this should probably be a method
        # technically this will allow selective ignoring of some action types
        # from the CLI or API in the future. A method like "provider.commit_to_plan()" seems good
        provider.actions = provider.actions_planned
        if not dry_run:
            # result here is really the stack of all CLI results -
            # FIXME: is this needed?  Or can we just have a generic return self.ok() method?
            # if we change this, we can eliminate the -1 stuff below
            result = provider.apply(facts)
            if result is None:
                raise ProviderError(provider, "provider %s did not return a value")
            self.callbacks.on_result(self.policy, resource, provider, result, handler=handlers)
            if provider.register is not None:
                new_vars = dict()
                new_vars[provider.register] = result
                V.update_variables(new_vars)


        else:
            # FIXME: this should be a method like provider.apply_simulated()
            provider.actions_taken = provider.actions_planned

        # the result of calling provider.apply is probably going to be a list of results
        # so this means we need to deal with answers differently

        if provider.has_changed():

            self.changed.append(resource)

            if resource.signals:
                self.signals.append(resource.signals)
                self.callbacks.on_signal_flagged(self.policy, resource, resource.signals)

        self.callbacks.on_actions_apply_end(self.policy, resource, provider, provider.actions_taken, dry_run=dry_run, handler=handlers)
        self.successful.append(resource)

