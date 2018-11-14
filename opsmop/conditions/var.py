from opsmop.conditions.condition import Condition
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.conditions.deferred import Deferred
from opsmop.core.facts import Facts

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

    def evaluate(self):
        vars = Facts.variables()
        if not self.var in vars:
            raise AttributeError("no variable found named: %s" % self.var)
        result = vars.get(self.var)
        return result

    def __getattr__(self, name):
        def value():
            return self.evaluate()
        return Deferred(value)


class VType(type):

    def __getattr__(cls, name):
        return DeferredVariable(name)

class V(object, metaclass=VType):
    pass
  