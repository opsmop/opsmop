from jinja2 import Environment, BaseLoader, FileSystemLoader, StrictUndefined
from jinja2.nativetypes import NativeEnvironment
from opsmop.core.facts import Facts
from opsmop.core.resource import Resource
from opsmop.core.deferred import Deferred

class T(Deferred):

    """
    T() is a deferred that evaluates a template at runtime, allowing variables
    established by Set() to be used. While some providers (like Echo) will template
    arguments automatically, most arguments in OpsMop must be explicitly templated
    with T. In the future T may also support some additional options.
    """

    def __init__(self, expr):
        super().__init__()
        self.expr=expr

    def evaluate(self, resource):
        return Template().from_string(self.expr, resource)

    def __str__(self):
        return "T: <'%s'>" % self.expr

class Template(object):

    def _get_context(self, resource, recursive_stop=None):

        from opsmop.core.eval import Eval

        self._variables = resource.get_variables()

        #for (k, v) in self._variables.items():
        #    if (v != recursive_stop) and (issubclass(type(v), Eval)):
        #        context[v] = v.evaluate(self) 

        return self._variables

    def from_string(self, msg, resource):
        j2 = Environment(loader=BaseLoader, undefined=StrictUndefined).from_string(msg)
        context = self._get_context(resource)
        return j2.render(context)
        
    def from_file(self, path, resource):
        loader = FileSystemLoader(searchpath="./")
        env = Environment(loader=loader, undefined=StrictUndefined)
        template = env.get_template(path)
        context = self._get_context(resource)
        return template.render(context)

    def native_eval(self, msg, resource):
        msg = "{{ %s }}" % msg
        j2 = Environment(loader=BaseLoader, undefined=StrictUndefined).from_string(msg)
        context = self._get_context(resource)
        return j2.render(context)
