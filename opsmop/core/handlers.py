

from opsmop.core.resource import Resource
from opsmop.core.collection import Collection

class Handlers(Collection):

    """
    A Handlers object is a basic collection of resources, just like Resources() but is different
    that it is represented as a dictionary instead of a list.  The keys of the dictionary are the
    names of the signals that the handler responds to.  For an example, see demo/content.py
    in the source tree.
    """

    def __init__(self, *args, **kwargs):

        # normally Collection objects take lists, but Handlers is hacked a tiny amount to provide
        # some syntactic sugar so it can take a dict.
        
        handlers = []
        if 'items' in kwargs:
            handlers = kwargs['items']
        else:
            for (k,v) in kwargs.items():
                if (k != 'items') and issubclass(type(v), Resource):
                    v.handles = k
                    handlers.append(v)

        self.kwargs = {}
        self.kwargs['items'] = handlers
        self.field_spec = self.fields()
        self.field_spec.find_unexpected_keys(self)
        self.field_spec.load_parameters(self)

