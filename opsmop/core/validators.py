import os

from opsmop.core.errors import ValidationError


class Validators(object):

    def __init__(self, resource):
        self.resource = resource

    def mutually_exclusive(self, fields):
        values = [ f for f in fields if getattr(self.resource, f) ]
        if len(values) > 1:
            raise ValidationError(self.resource, "fields are mutually exclusive: %s" % fields)

    def path_exists(self, path):
        if path is None:
            return False
        # FIXME use the FileTest module, don't duplicate this here
        path = os.path.expandvars(os.path.expanduser(path))
        if not os.path.exists(path):
            raise ValidationError(self.resource, "path does not exist: %s" % path)
