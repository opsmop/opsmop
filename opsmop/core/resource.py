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

    def set_scope(self, scope):
        self._scope = scope

    def split_common_kwargs(self, kwargs):
        common = dict()
        original = dict()
        for (k,v) in kwargs.items():
            if k in COMMON_FIELDS:
                common[k] = v
            else:
                original[k] = v
        return (original, common)

    def scope(self):
        assert self._scope is not None
        return self._scope

    def set_variables(self):
        """ A method that can be defined on any resource class to provide extra variables to templating """
        return dict()

    def get_children(self, method=None):
        return None

    def validate(self):
        pass

    def update_variables(self, variables):
        """
        This is called by the executor.  It mixes in variables from higher scopes
        allowing local variables to win.
        """
        self.scope().update_variables(variables)

    def update_parent_variables(self, variables):
        self.scope().update_parent_variables(variables)

    def get_variables(self):
        return self.scope().variables()

    def deeper_scope(self):
        return self.scope().deeper()

    def conditions_true(self, context):

        from opsmop.lookups.eval import Eval 
        from opsmop.lookups.lookup import Lookup

        when = self.when
        if when is None:
            return True
        if type(when) == str:
            res = Eval(self.when).evaluate(self)
            return res
        elif issubclass(type(cond), Lookup):
            return cond.evaluate(self)
        else:
            return cond
        

