
from opsmop.core.fields import COMMON_FIELDS

class Resource(object):

    def __init__(self,  *args, **kwargs):
        self.setup(*args, *kwargs)

    def setup(self, **kwargs):
        self.kwargs = kwargs
        self.facts = None
        self.condition_stack = []
        self._variables = dict()
        self._scope = None
        self._field_spec = self.fields()
        self._field_spec.find_unexpected_keys(self)
        self._field_spec.load_parameters(self)

    def split_common_kwargs(self, kwargs):
        common = dict()
        original = dict()
        for (k,v) in kwargs.items():
            if k in COMMON_FIELDS:
                common[k] = v
            else:
                original[k] = v
        return (original, common)

    def child_scope(self, resource):
        my_scope = resource.scope()
        kid_scope = self._scope.deeper_scope_for(resource)
        resource._scope = kid_scope
        return kid_scope

    def scope(self):
        return self._scope

    def set_variables(self):
        """ A method that can be defined on any resource class to provide extra variables to templating """
        return dict()

    def update_variables(self, variables):
        """
        This is called by the executor.  It mixes in variables from higher scopes
        allowing local variables to win.
        """
        self._scope.update_variables(variables)

    def update_parent_variables(self, variables):
        self._scope.update_parent_variables(variables)

    def get_variables(self):
        variables = self._scope.variables()
        return variables

    def deeper_scope(self):
        return self._scope.deeper()

    def set_condition_stack(self, stack):
        """ Used by executor code to assign a stack of conditions, all of which must be true to plan or apply the resource """
        self.condition_stack = stack

    def get_condition_stack(self):
        conditions = self.condition_stack[:]
        if self.when:
            conditions.append(self.when)
        return conditions
