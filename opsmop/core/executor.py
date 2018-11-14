from opsmop.core.visitor import Visitor
from opsmop.core.facts import Facts
from opsmop.core.result import Result
from opsmop.core.context import Context
from opsmop.core.policy import Policy

facts = Facts()

class Executor(object):

    def __init__(self, policies=None, callbacks=None):

        """
        The executor provides methods for, well, executing a  list of policies.
        It is not used directly, and leverages the Visitor() class to walk the resource tree.
        For top-level usage, see Api.py
        """
  
        assert type(policies) == list
        assert type(callbacks) == list

        self._policies = policies
        self._callbacks = callbacks


    def validate(self):
        """
        Validate runs the .validate() method on every resource to check for argument consistency.
        Items like missing files are also checked at this time.
        """
        return self.run_all_policies(self._policies, check=False, apply=False)

    def check(self):
        """
        check runs the .plan() method on every resource tree and reports what resources would
        be changed, but does not make changes.  This is dry-run mode.
        """
        return self.run_all_policies(self._policies, check=True, apply=False)

    def apply(self):
        """
        apply runs .plan() and then .apply() to run the planned actions.
        """
        return self.run_all_policies(self._policies, check=True, apply=True)

    def run_all_policies(self, policies, check=False, apply=False):
        """
        any .py file fed into the cli can contain a list of policies.
        This will run all of them.  The result is a list of contexts
        and then a final call to all_policies_complete on the last context
        object.
        """
        assert policies is not None

        results = []
        context = None
        for policy in self._policies:
            context = Context(callbacks=self._callbacks)
            for cb in self._callbacks:
                cb.context = context
            self.run_policy(policy=policy, context=context, check=check, apply=apply)
            results.append(context)
        if context:
            context.on_all_policies_complete()
        return results

    def run_policy(self, policy=None, context=None, check=False, apply=False):
        
        assert issubclass(type(policy), Policy)
        assert issubclass(type(context), Context)

        signals = []

        visitor = Visitor(policy=policy, context=context)
        Facts.update_variables(policy.variables)

        for resource in visitor.walk_resources():
            resource.validate()

        for resource in visitor.walk_handlers():
            resource.validate()

        for resource in visitor.walk_resources():
            self.execute_resource(resource=resource, context=context, signals=signals, check=check, apply=apply)
            
        for resource in visitor.walk_handlers():
            if resource.handles in signals:
                self.execute_resource(resource=resource, context=context, signals=signals, check=check, apply=apply, handlers=True)

        context.on_complete(policy)


    def conditions_true(self, context, resource):
        assert resource is not None
        stack = resource.condition_stack
        context.on_conditions(stack)
        return all(cond.evaluate() for cond in stack)


    def execute_resource(self, resource=None, context=None, check=False, apply=False, handlers=False, signals=None):
        
        assert resource is not None
        assert context is not None

        context.on_resource(resource, handlers)

        if not check and not apply:
            return

        if not self.conditions_true(context, resource):
            context.on_skipped(resource)
            return

        # print(type(resource))
        provider = resource.provider()
        provider.set_context(context)

        context.on_plan(provider)

        if not provider.skip_plan_stage():
            provider.plan()
            context.on_planned_actions(provider, provider.actions_planned)
            provider.commit_to_plan()

        if apply:

            context.on_apply(provider)
            result = provider.apply()
            if not handlers:
                context.on_taken_actions(provider, provider.actions_taken)
            
            assert result is not None
            assert issubclass(type(result), Result)

            if provider.register is not None:
                va = dict()
                va[provider.register] = result
                context.on_update_variables(va)
                Facts.update_variables(va)

            context.on_result(result)
            if result.fatal:
                context.on_fatal(result)

        else:
            provider.apply_simulated_actions()

        if provider.has_changed():
            if resource.signals:
                context.on_flagged(signals)
                signals.append(resource.signals)


