
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.types.file import File

class Directory(File):

    """
    Represents a software package
    """

    def __init__(self, name=None, **kwargs):
        self.setup(name=name, **kwargs)
        self.directory = True

   