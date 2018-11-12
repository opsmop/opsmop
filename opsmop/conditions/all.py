from opsmop.conditions.condition import Condition
from opsmop.core.field import Field
from opsmop.core.fields import Fields

class All(Condition):

    """
    A Condition is the declarative representation of a conditional that is fed to a "when" clause.
    They are fed in an instance of the facts object.
    condition.evaluate() facts will return true or false.
    """

    def __init__(self, *args):
        super().__init__(conditions=args)

    def fields(self):
        return Fields(
            conditions = Field(kind=list, of=Condition),
        )

    def is_grouping(self):
        return True

    def evaluate(self, facts):
        computed = [ x.evaluate(facts) for x in self.conditions ]
        for x in computed:
            if not x:
                return False
        return True
