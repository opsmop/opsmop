from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.types.type import Type

class Debug(Type):

    def __init__(self, *args, **kwargs):
        (original, common) = self.split_common_kwargs(kwargs)
        self.setup(variable_names=args, evals=original, **common)

    def fields(self):
        return Fields(
            self,
            evals = Field(kind=dict),
            variable_names = Field(kind=list)
        )

    def default_provider(self):
        from opsmop.providers.debug import Debug
        return Debug