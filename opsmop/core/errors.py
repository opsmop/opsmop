class OpsMopError(Exception):

    def __init__(self, msg):
        self.msg = msg

class ValidationError(OpsMopError):
    
    def __init__(self, resource, msg):
        self.resource = resource
        self.msg = msg

class ProviderError(OpsMopError):

    def __init__(self, provider, msg):
        self.resource = provider.resource
        self.provider = provider
        self.msg = msg







