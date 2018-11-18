from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.types.type import Type

class DebugFacts(Type):

    def __init__(self, *args, **kwargs):
        self.setup(**kwargs)

    def fields(self):
        return Fields(
            self
        )

    def default_provider(self):
        from opsmop.providers.debug_facts import DebugFacts
        return DebugFacts