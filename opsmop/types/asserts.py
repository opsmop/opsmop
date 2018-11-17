from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.types.type import Type

class Asserts(Type):

    def __init__(self, *args, **kwargs):
        (original, common) = self.split_common_kwargs(kwargs)
        self.setup(evals=args, variable_checks=original, **common)

    def fields(self):
        return Fields(
            self,
            evals = Field(kind=list),
            variable_checks = Field(kind=dict)
        )

    def default_provider(self):
        from opsmop.providers.asserts import Asserts
        return Asserts