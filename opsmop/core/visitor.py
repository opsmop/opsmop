from opsmop.core.resource import Resource
from opsmop.core.collection import Collection
from opsmop.core.policy import Policy
from opsmop.core.context import Context
from opsmop.core.facts import Facts

MODE_RESOURCES = "resources"
MODE_HANDLERS = "handlers"

# FIXME: refactor

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
        self.context = context

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

        # FIXME: does this pay attention to signals?  Are we calling it correctly in Executor?

        """
        Generic traversal code for resources OR handlers
        """

        variables = self.policy.variables
        condition = self.policy.when
        roles = self.policy.roles
            
        # conditions are stored as we go, building up a array of conditions in order
        # the same is true of variables
        condition_stack = []
        if condition:
            # FIXME: verify this is being used
            condition_stack.append(condition)
        
        # FIXME: the variable system should operate a bit more like a stack, and clear off
        # when popping out of a depth level.

        for role in roles.items:
            self.context.on_role(role)
            Facts.update_variables(role.variables)
            if mode in [ MODE_RESOURCES ]:
                for resource in role.resources.items:
                    for x in self._walk_items(resource, mode, condition_stack):
                         yield x
            if mode in [ MODE_HANDLERS  ] :
                for handler in role.handlers.items:
                    for x in self._walk_items(handler, mode, condition_stack):
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

    def _walk_items(self, obj, mode, conditions):
        """
        Actual traversal code for the object tree.
        This handles recursion into nested resources
        """

        # FIXME: this may need some work to make sure variable trees work as expected
        # FIXME: AND ALSO conditions!!!

        ot = type(obj)

        conditions = conditions[:]

        if issubclass(ot, Resource):
            if obj.when:
                conditions.append(obj.when)

        if issubclass(ot, Collection):
            for x in obj.items:
                for recursed in self._walk_items(x, mode, conditions):
                    yield recursed

        elif type(obj) == list:
            for x in obj:
                for recursed in self._walk_items(x, mode, conditions):
                    yield recursed
            

        else:
            # this is the return for each step of self.walk_resources or self.walk_handlers
            # it is only defined here.
            obj.set_condition_stack(conditions)
            yield obj

        return
