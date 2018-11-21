class Result(object):

    """
    Result represents the return result from a command execution *OR* a application of a provider,
    in which case there should be an array of results (FIXME?)   
    """

    __slots__ = [ 'rc', 'provider', 'resource', 'data', 'fatal', 'message', 'data' ]

    def __init__(self, provider=None, changed=True, message=None, rc=None, data=None, fatal=False):

        """
        A result can be constructed with many parameters, most of which have reasonable defaults:

        provider - a reference to the provider object (required)
        resource - a reference to the resource the provider is executing (required)
        rc - the return code of any CLI command
        data - the output of a CLI command, or any structured data for use with 'register'
        fatal - a flag that indicates the result should probably end the program, but it is up to the callback code
        """
        assert provider is not None
        self.provider = provider
        self.resource = provider.resource
        self.rc = rc
        self.data = data
        self.fatal = fatal
        self.message = message

    def is_ok(self):
        return not self.fatal

    def __str__(self):
        rc_msg = ""
        msg = ""
        if self.message is not None:
            msg = ", %s" % self.message
        if self.rc is not None:
            rc_msg = ", rc=%s" % self.rc
        if self.is_ok():
            return "ok%s%s" % (rc_msg, msg)
        else:
            return "fatal%s%s" % (rc_msg, msg)
