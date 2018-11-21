from opsmop.core.result import Result
from opsmop.core.context import Context
from opsmop.core.policy import Policy
from opsmop.core.scope import Scope
from opsmop.lookups.eval import Eval
from opsmop.lookups.lookup import Lookup
from opsmop.core.collection import Collection

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

        if len(results):
            context.on_all_policies_complete()

        return results

    def run_policy(self, policy=None, context=None, check=False, apply=False):
        
        assert issubclass(type(policy), Policy)
        assert issubclass(type(context), Context)

        policy.init_scope(context)

        # FIXME: refactor signal handling through context, as also with condition_stack
        signals = []

        def validate(resource):
            return resource.validate

        context.on_validate()
        roles = policy.get_children('')

        for role in roles.items:

            role.pre()

            if not role.conditions_true(context):
                continue

            policy._claim(role)

            # TEMPORARILY DISABLE VALIDATE MODE BECAUSE IT IS TOO SQUEAKY
            #role.walk_children(items=role.get_children('resources'), context=context, mode='resources', fn=validate, check=check, apply=apply)
            #role.walk_children(items=role.get_children('handlers'), context=context, mode='handlers', fn=validate, check=check, apply=apply)

            if (check or apply):
            
                context.on_begin()

                def execute_resource(resource):
                    resource.pre()
                    result = self.execute_resource(resource=resource, context=context, signals=signals, check=check, apply=apply)
                    resource.post()
                    return result
                role.walk_children(items=role.get_children('resources'), context=context, mode='resources', fn=execute_resource, check=check, apply=apply)

                context.on_begin_handlers()

                def execute_handler(handler):
                    handler.pre()
                    result = self.execute_resource(resource=handler, context=context, signals=signals, check=check, apply=apply, handlers=True)
                    handler.post()
                    return result
                role.walk_children(items=role.get_children('handlers'), context=context, mode='handlers', fn=execute_handler, check=check, apply=apply)

            role.post()

        context.on_complete(policy)

    # FIXME: can be broken into smaller functions

    def execute_resource(self, resource=None, context=None, check=False, apply=False, handlers=False, signals=None):
        
        assert resource is not None
        assert context is not None

        if issubclass(type(resource), Collection):
            # don't print anything for collections
            return


        if handlers:
            handlers = resource.all_handlers()
            matched = set(handlers).intersection(set(signals))
            if not len(matched):
                context.on_skipped(resource, is_handler=handlers)
                return

        context.on_resource(resource, handlers)

        if not check and not apply:
            return

        provider = resource.provider()
        provider.set_context(context)
        
        context.on_plan(provider)

        if not provider.skip_plan_stage():
            provider.plan()
            context.on_planned_actions(provider, provider.actions_planned)
            provider.commit_to_plan()

        if apply:

            if not provider.skip_plan_stage() and len(provider.actions_planned) == 0:
                return
            context.on_apply(provider)
            result = provider.apply()
            if not handlers:
                context.on_taken_actions(provider, provider.actions_taken)
            
            assert result is not None
            assert issubclass(type(result), Result)

            if resource.register is not None:
                va = dict()
                va[provider.register] = result
                context.on_update_variables(va)
                provider.resource.update_parent_variables(va)

            context.on_result(result)
            if result.fatal:
                context.on_fatal(result)

        else:
            provider.apply_simulated_actions()

        if provider.has_changed():
            if resource.signals:
                context.on_flagged(signals)
                signals.append(resource.signals)


