from opsmop.conditions.condition import Condition
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.conditions.deferred import Deferred
from opsmop.client.facts import Facts

_variables = dict()
facts = Facts()

class DeferredVariable(Deferred):

    """
    A Condition is the declarative representation of a conditional that is fed to a "when" clause.
    They are fed in an instance of the facts object.
    condition.evaluate() facts will return true or false.
    """

    def __init__(self, arg):
        self.arg = arg
        Condition.__init__(self, var=arg)

    def fields(self):
        return Fields(
            var = Field(kind=str),
        )

    def evaluate(self, facts):
        if not self.var in _variables:
            raise AttributeError("no variable found named: %s" % self.var)
        result = _variables.get(self.var)
        return result

    def __getattr__(self, name):
        def value():
            return self.evaluate(facts)
        return Deferred(value)


class VType(type):

    def __getattr__(cls, name):
        return DeferredVariable(name)

class V(object, metaclass=VType):

    @classmethod
    def set_variables(self, variables):
        global _variables
        _variables = variables

    @classmethod
    def update_variables(self, variables):
        _variables.update(variables)

    @classmethod
    def all_variables(self):
        return _variables.copy()
  