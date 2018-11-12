

from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.resource import Resource
from opsmop.core.role import Role

class Policy(Resource):

    """
    A policy is a top level object representing a configuration of a particular type of Thing, where Thing is usually
    a computer system with a particular purpose, or part thereof.

    Fields are as follows:

    id - this is the 'remote' name of the policy, and is required to upload the policy OR apply it to a remote system
    (there is an additional namespace for uploads called environment that is specified only on the CLI)
    variables - optionally, variables can be defined on this policy at a top level
    roles - describes what this policy configures
    """ 

    def fields(self):
        return Fields(
            name = Field(kind=str, default=None),
            variables = Field(kind=dict, loader=self.set_variables),
            roles = Field(kind=list, of=Role, loader=self.set_roles)
        )

    def set_variables():
        return dict()
        
    def set_roles():
        return []



