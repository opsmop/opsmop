from opsmop.conditions.condition import Condition
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.filetests import FileTests
from opsmop.core.errors import ValidationError

class FileTest(Condition):

    """
    A Condition is the declarative representation of a conditional that is fed to a "when" clause.
    They are fed in an instance of the facts object.
    condition.evaluate() facts will return true or false.
    """

    def fields(self):
        return Fields(
            present = Field(kind=str, default=None),
            absent = Field(kind=str, default=None),
        )

    def evaluate(self):

        # FIXME: this should use a core module called FileTests that can be shared with providers
        # and this will also simplify providers.file.File

        if not self.present and not self.absent:
            raise ValidationError("expecting exists or absent for FileTest")

        truth = []
        if self.present:
            truth.append(FileTests(self.present).exists())

        if self.absent:
            truth.append(not FileTests(self.absent).exists())

        return all(x for x in truth)

    def __str__(self):
        # FIXME: this is a little basic but ok for now.
        if self.present and self.absent:
            return "<FileTest>"
        elif self.present:
            return "<FileTest: %s is present>" % self.present
        elif self.absent:
            return "<FileTest: %s is absent>" % self.absent
        return "<FileTest>"
