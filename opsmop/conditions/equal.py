from opsmop.conditions.condition import Condition
from opsmop.core.field import Field
from opsmop.core.fields import Fields

class Equal(Condition):

    """
    A Condition is the declarative representation of a conditional that is fed to a "when" clause.
    They are fed in an instance of the facts object.
    condition.evaluate() facts will return true or false.
    """

    def __init__(self, a, b):
        super().__init__(a=a, b=b)

    def fields(self):
        return Fields(
            a = Field(),
            b = Field()
        )

    def evaluate(self):
        return self.get_value(self.kwargs['a']) == self.get_value(self.kwargs['b'])

def model():
    return Equal