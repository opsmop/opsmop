from opsmop.core.facts import Facts
from opsmop.core.template import Template as CoreTemplate
from opsmop.lookups.lookup import Lookup

class Template(Lookup):

    """
    T() is a deferred lookup that evaluates a template at runtime, allowing variables
    established by Set() to be used. While some providers (like Echo) will template
    arguments automatically, most arguments in OpsMop must be explicitly templated
    with T. In the future T may also support some additional options.
    """

    def __init__(self, expr):
        super().__init__()
        self.expr=expr

    def evaluate(self, resource):
        return CoreTemplate().from_string(self.expr, resource)

    def __str__(self):
        return "T: <'%s'>" % self.expr

T = Template