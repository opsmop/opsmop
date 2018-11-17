from opsmop.core.resource import Resource
from opsmop.core.collection import Collection
from opsmop.core.handlers import Handlers
from opsmop.core.policy import Policy
from opsmop.core.context import Context
from opsmop.core.scope import Scope

MODE_RESOURCES = "resources"
MODE_HANDLERS = "handlers"

class Visitor(object):

    """
    The visitor is a class that walks a policy tree, providing an iterator
    that yields every resource.

    This doesn't make much sense used by itself. See Executor() 
    for how this is used in the context of making a CLI entry point for
    the opsmop main program.
    
    Visitor only walks resources, it does not manipulate them. For that,
    see Executor.
    """

    __slots__ = [ 'policy', 'context' ]

    def __init__(self, policy=None, context=None):
        assert issubclass(type(policy), Policy)
        assert issubclass(type(context), Context)
        self.policy = policy
        self.policy._scope = Scope.for_top_level(self.policy)
        self.context = context
        self.policy.update_variables(self.policy.variables)

    def walk_resources(self):
        """
        Return an iterator across all resources, returning (resource, truth, variables)
        as a tuple for each.  Truth is whether all conditions assigned along the way
        are true, and variables is the merger of variables evaluated along the way.
        """
        return self._walk(mode=MODE_RESOURCES)

    def walk_handlers(self):
        """
        Similar to walk_resources, but for handlers (which are also just resources)
        """
        return self._walk(mode=MODE_HANDLERS)

    def _walk(self, mode='resources'):
        """
        Generic traversal code for resources OR handlers
        """

        variables = self.policy.variables
        condition = self.policy.when
        roles = self.policy.roles
            
        # FIXME: conditions are stored as we go, building up a array of conditions in order
        # this could be simplified by using scopes like with variables.

        condition_stack = []
        if condition:
            condition_stack.append(condition)

        for role in roles.items:
            self.policy.child_scope(role)
            self.context.on_role(role)

            if mode == MODE_RESOURCES:
                for resource in role.resources.items:
                    role.child_scope(resource)
                    results = []
                    for x in self._walk_items(role, resource, mode, condition_stack, results):
                        yield x
            if mode == MODE_HANDLERS:
                for handler in role.handlers.items:
                    role.child_scope(handler)
                    results = []
                    for x in self._walk_items(role, handler, mode, condition_stack, results):
                        yield x
        return

    def _flatten_variables(self, variable_list):
        """
        Used to convert the array of variables in a last-wins precedence order.
        """
        results = dict()
        for variables in variable_list:
            results.update(variables)
        return results

    def get_children(self, obj):
        if issubclass(type(obj), Collection):
            return obj.items
        else:
            return []

    def _walk_items(self, parent, obj, mode, conditions, results):
        """
        Actual traversal code for the object tree.
        This handles recursion into nested resources
        """
        if type(obj) == list:
            for x in obj:
                self._walk_items(parent, x, mode, conditions, results)
            return results

        conditions = conditions[:]
        if obj.when:
            conditions.append(obj.when)
        parent.child_scope(obj)
        
        if not issubclass(type(obj), Collection):
            results.append(obj)

        children = self.get_children(obj)
        for child in children:
            self._walk_items(obj, child, mode, conditions, results)
        return results
