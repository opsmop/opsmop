

from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.resource import Resource
from opsmop.core.role import Role
from opsmop.core.scope import Scope
from opsmop.core.collection import Collection

class Policy(Collection):

    def __init__(self, **kwargs):
        (original, common) = self.split_common_kwargs(kwargs)
        self.setup(extra_variables=original, **common)

    def init_scope(self, context):
        self.set_scope(Scope.for_top_level(self))
        self.context = context
        self.update_variables(self.variables)

    def fields(self):
        return Fields(
            self,
            name = Field(kind=str, default=None),
            variables = Field(kind=dict, loader=self.set_variables),
            roles = Field(kind=list, of=Role, loader=self.set_roles)
        )

    def set_variables(self):
        return dict()
        
    def set_roles(self):
        raise Exception("Policy class must implement set_roles")

    def get_children(self, mode):
        return self.roles



