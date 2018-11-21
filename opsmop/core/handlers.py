from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.resource import Resource
from opsmop.core.resources import Resources

class Handlers(Resources):

    def __init__(self, **kwargs):
        handlers = []
        for (k,v) in kwargs.items():
            v.handles = k
            handlers.append(v)
        self.setup(items=handlers)

    def fields(self):
        return Fields(
            self,
            items = Field(kind=list, of=Resource),
        )
