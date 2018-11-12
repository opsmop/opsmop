from opsmop.conditions.condition import Condition
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.filetests import FileTests

class FileExists(Condition):

    """
    A Condition is the declarative representation of a conditional that is fed to a "when" clause.
    They are fed in an instance of the facts object.
    condition.evaluate() facts will return true or false.
    """

    def __init__(self, var):
        super(var=var)

    def fields(self):
        return Fields(
            var = Field(kind=str),
        )

    def evaluate(self, facts):
        self.tests = FileTests(self.var)
        return self.tests.exists()
