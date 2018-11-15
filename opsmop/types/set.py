

from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.types.type import Type

class Set(Type):

    def __init__(self, *args, **kwargs):
        (original, common) = self.split_common_kwargs(kwargs)
        self.setup(extra_variables=original, **common)

    def fields(self):
        return Fields(
            self,
            variables = Field(kind=dict)
        )

    def default_provider(self):
        from opsmop.providers.set import Set
        return Set
