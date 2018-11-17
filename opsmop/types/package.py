
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.types.type import Type
from opsmop.core.facts import Facts

class Package(Type):

    """
    Represents a software package
    """

    def __init__(self, name=None, **kwargs):
        self.setup(name=name, **kwargs)

    def fields(self):
        return Fields(
            self,
            name = Field(kind=str, help="the name of the package to install"),
            version = Field(kind=str, default=None, help="what version to install"),
            latest = Field(kind=bool, default=False, help="if true, upgrade the package regardless of version"),
            absent = Field(kind=bool, default=False, help="if true, remove the package")
        )

    def validate(self):
        # FIXME: latest and absent are incompatible, as are version and absent
        pass

    def get_provider(self, method):
        if method == 'brew':
            from opsmop.providers.package.brew import Brew
            return Brew
        raise ValidationError("unsupported provider: %s" % method)

    def default_provider(self):
        return Facts.default_package_manager()
