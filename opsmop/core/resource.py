
class Resource(object):

    """
    A Resource is the base class for nearly all object types - including Collections - in OpsMop.
    It is heavily powered by the Field() class to implement defaults and type checks of fields
    that are passed in to constructors.
    """

    def __init__(self,  *args, **kwargs):
        self.kwargs = kwargs
        self.facts = None
        self._variables = dict()
        self.condition_stack = []
        self.field_spec = self.fields()
        self.field_spec.find_unexpected_keys(self)
        self.field_spec.load_parameters(self)

    def variables(self):
        return self._variables
 
    def set_variables(self, variables):
        assert type(variables) == dict
        self._variables = variables       

    def fields(self):
        """
        Subclasses MUST override this method to define the Fields specification for the object.
        """
        raise NotImplementedError()

   


