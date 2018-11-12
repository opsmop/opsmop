
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.errors import ValidationError
from opsmop.core.validators import Validators
from opsmop.types.type import Type

class File(Type):

    """
    Represents a software package
    """

    def __init__(self, name=None, *args, **kwargs):
        kwargs['name'] = name
        super().__init__(*args, **kwargs)

    def fields(self):
        return Fields(
            name = Field(kind=str, help="path to the DESTINATION file"),
            from_file = Field(kind=str, default=None, help="use this file as source data"),
            from_template = Field(kind=str, default=None, help="use this template as source data"),
            from_content = Field(kind=str, default=None, help="use this string as source data"),
            owner = Field(kind=str, default=None, help="owner name"),
            group = Field(kind=str, default=None, help="group name"),
            mode = Field(kind=int, default=None, help="file mode, in octal (no strings)"),
            absent = Field(kind=bool, default=False, help="if true, delete the file/directory"),
            directory = Field(kind=bool, default=False, help="if true, look for a directory, not a file."),
            overwrite = Field(kind=bool, default=True, help="if false, existing files will not be copied over"),
        )

    def validate(self):
        v = Validators(self)
        v.mutually_exclusive(['from_file', 'from_template', 'from_content'])
        v.mutually_exclusive(['directory', 'from_file'])
        v.mutually_exclusive(['directory', 'from_template'])
        v.mutually_exclusive(['directory', 'from_content'])
        v.path_exists(self.from_file)
        v.path_exists(self.from_template)

    def default_provider(self, facts):
        from opsmop.providers.file import File
        return File

def model():
    return Package