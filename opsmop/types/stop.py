
from opsmop.types.type import Type
from opsmop.core.fields import Fields
from opsmop.core.field import Field

class Stop(Type):

    def __init__(self, msg, *args, **kwargs):
        self.setup(msg=msg, **kwargs)

    def fields(self):
        return Fields(
            self,
            msg = Field(kind=str, allow_none=False, help="string to print")
        )

    def validate(self):
        pass

    def default_provider(self):
        from opsmop.providers.stop import Stop
        return Stop
