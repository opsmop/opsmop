
from opsmop.types.type import Type
from opsmop.core.fields import Fields
from opsmop.core.field import Field

class Stop(Type):

    def __init__(self, msg, *args, **kwargs):
        kwargs['msg'] = msg
        super().__init__(self, *args, **kwargs)

    def fields(self):
        return Fields(
            msg = Field(kind=str, allow_none=False, help="string to print")
        )

    def validate(self):
        pass

    def default_provider(self):
        from opsmop.providers.stop import Stop
        return Stop
