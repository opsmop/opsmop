
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

    
    key-value arguments are available after the resource declaration, like:
    Collection(*resource_list, when=is_os_x)
    """

    def __init__(self, *args, **kwargs):
        self.setup(items=args, **kwargs)

    def fields(self):
        return Fields(
            self,
            items = Field(kind=list, of=Resource),
        )
