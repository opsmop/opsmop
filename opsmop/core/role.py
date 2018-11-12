
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.resource import Resource
from opsmop.core.resources import Resources
from opsmop.core.handlers import Handlers

class Role(Resource):

    """
    A role is a collection of resources, handlers, and variables.  A Site policy can
    contain more than one one role.
    
    For an example see demo/content.py
    """


    def fields(self):
        return Fields(
            name = Field(kind=str, default=None),
            variables = Field(kind=dict, loader=self.set_variables),
            resources = Field(kind=list, of=Resource, loader=self.set_resources),
            handlers  = Field(kind=dict, of=Resource, loader=self.set_handlers),
        )

    def set_variables(self):
        return dict()

    def set_resources(self):
        return Resources()

    def set_handlers(self):
        return Handlers()
