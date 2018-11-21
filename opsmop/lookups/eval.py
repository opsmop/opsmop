from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.core.template import Template
from opsmop.lookups.lookup import Lookup


class Eval(Lookup):

    """
    when=Eval("a > b")
    """

    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def evaluate(self, resource):
        return Template.native_eval(self.expr, resource)

    def __str__(self):
        return "Eval: <'%s'>" % self.expr
