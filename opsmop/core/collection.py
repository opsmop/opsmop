
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.resource import Resource

class Collection(Resource):

    """
    A collection is a type of resources that can contain other Resources.

    Example:

    Collection(
        Resource(...),
        Resource(...)
    )

    OR

    Collection(*resource_list)

    OR (because of the way the deserializer works)

    Collection(items=resource_list)

    are all equivalent.
    
    key-value arguments are available after the resource declaration, like:

    Collection(*resource_list, when=is_os_x)
    """

    def __init__(self, *args, **kwargs):
        # the previous comment for usage
        self.kwargs = kwargs
        if not 'items' in kwargs:
            self.kwargs['items'] = args
        self.field_spec = self.fields()
        self.field_spec.find_unexpected_keys(self)
        self.field_spec.load_parameters(self)

    def fields(self):
        return Fields(
            items = Field(kind=list, of=Resource),
        )
