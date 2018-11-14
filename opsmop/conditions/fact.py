from opsmop.conditions.condition import Condition
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.facts import Facts
from opsmop.conditions.deferred import Deferred

facts = Facts()

class DeferredVariable(Deferred):

    """
    A Condition is the declarative representation of a conditional that is fed to a "when" clause.
    They are fed in an instance of the facts object.
    condition.evaluate() facts will return true or false.
    """

    def __init__(self, arg):
        Condition.__init__(self, var=arg)

    def fields(self):
        return Fields(
            fact = Field(kind=str),
        )

    def evaluate(self):
        return getattr(facts, self.fact)()

    def __call__(self):
        def value():
            return self.evaluate()
        return Deferred(value)

class FType(type):

    def __getattr__(cls, name):
        if getattr(facts, name, None) is None:
            raise AttributeError
        return DeferredFact(name)

class F(object, metaclass=FType):

    pass