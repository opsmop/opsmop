
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.errors import ValidationError
from opsmop.types.type import Type

class Echo(Type):

    """
    Represents a debug statement
    """

    def __init__(self, msg, *args, **kwargs):
        self.create(msg=msg, **kwargs)

    def fields(self):
        return Fields(
            msg = Field(kind=str, allow_none=False, help="string to print")
        )

    def validate(self):
        pass

    def default_provider(self):
        from opsmop.providers.echo import Echo
        return Echo

