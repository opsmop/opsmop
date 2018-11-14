
class Fields(object):

    """
    In order to keep resource management clean there is a bit of automatic behind the scenes.
    A Fields specification is used to validate all object types have valid parameters in the opsmop DSL,
    but also is heavily used in serializing and deserializing objects.

    Additionally, we automatically add some certain fields to EVERY object type.
    """

    __slots = [ 'fields' ]
    COMMON_FIELDS = [ 'when', 'signals', 'handles', 'method', 'register', 'ignore_errors' ]

    def __init__(self, **fields):

        """
        Construct a fields object. 
        While each Resource can define their own fields, certain fields are always added.

        when - a conditional to decide if the resource is to be executed.  For collections, this condition
        is applied to the whole collection (FIXME) before traversing any element in the collection.

        handles - the name of a signal that handlers can use when triggered by 'notify'.  Assigning
        'handles' to something that is not a handler has no effect.

        notify - the name of a signal that triggers a handler

        method - used on any resource to explicitly select a provider class rather than using
        the default provider figured out by the resource.  For an example see opsmop.types.package.Package

        register - saves the result to a variable, regardless of type

        ignore_errors - if the return is a fatal result object, ignore it anyway
        """

        self.fields = fields

        from opsmop.core.field import Field
        from opsmop.core.resource import Resource
        from opsmop.conditions.condition import Condition

        self.fields['when'] = Field(kind=Condition, default=None)
        self.fields['signals'] = Field(kind=list, of=Resource, default=None)
        self.fields['handles'] = Field(kind=str, default=None)
        self.fields['method'] = Field(kind=str, default=None)
        self.fields['register'] = Field(kind=str, default=None)
        self.fields['ignore_errors'] = Field(kind=bool, default=False)

    def find_unexpected_keys(self, obj):

        """
        Called by Resource code to verify no fields were passed in that were not in the field specification.
        """

        for (k,v) in obj.kwargs.items():
            if k.startswith("!"):
                continue
            if k not in self.fields:
                raise Exception("%s: parameter is not understood, %s" % (self, k))

    def load_parameters(self, obj):

        """
        Loads all values from a field spec into a resource object, applying any defaults
        and type checks required by the field spec.  This means the values stored in object
        member variables will be ultimately different than what is passed in by the constructor
        in some cases. See the Field class for details, or any resource such as opsmop.types.package.Package
        for an example of a field specification.
        """

        for (k,field) in self.fields.items():
            field.load(obj, k)