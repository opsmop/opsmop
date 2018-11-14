

from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.types.type import Type

class Set(Type):

    def __init__(self, *args, **kwargs):
        new_dict = dict(
            items = kwargs.copy()
        )
        super().__init__(*args, **new_dict)

    def fields(self):
        return Fields(
            items = Field(kind=dict),
        )

    def default_provider(self):

        from opsmop.providers.set import Set
        return Set
