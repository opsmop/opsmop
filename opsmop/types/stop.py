
from opsmop.types.type import Type
from opsmop.core.fields import Fields
from opsmop.core.field import Field

class Stop(Type):

    def __init__(self, msg, *args, **kwargs):
        self.create(msg=msg, **kwargs)

    def fields(self):
        return Fields(
            msg = Field(kind=str, allow_none=False, help="string to print")
        )

    def skip_plan_stage(self):
        return True

    def validate(self):
        pass

    def default_provider(self):
        from opsmop.providers.stop import Stop
        return Stop
