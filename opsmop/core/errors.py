class OpsMopError(Exception):

    """
    The basis for all types of OpsMop Errors, this one really should not be used directly.
    """

    __slots__ = [ 'msg' ]

    def __init__(self, msg):
        self.msg = msg

class ValidationError(OpsMopError):

    """
    This is the type of error that gets called when a resource has invalid arguments.
    """

    __slots__ = [ 'resource', 'msg' ]
    
    def __init__(self, resource, msg):
        self.resource = resource
        self.msg = msg

class ProviderError(OpsMopError):

    """
    This error *may* be raised by a provider for certain internal issues, but in general
    provider apply methods should return self.error('msg') when available.

    This could be used to raise an error in the plan() stage.
    """

    __slots__ = [ 'provider', 'resource', 'msg' ]

    def __init__(self, provider, msg):
        self.provider = provider
        self.resource = provider.resource
        self.msg = msg
