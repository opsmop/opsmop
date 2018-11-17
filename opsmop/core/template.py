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
        return Template.from_string(self.expr, resource)

    def __str__(self):
        return "T: <'%s'>" % self.expr

class Template(object):

    @classmethod
    def _get_context(cls, resource):
        context = resource.get_variables()
        context["Facts"] = Facts
        return context

    @classmethod
    def from_string(cls, msg, resource):
        j2 = Environment(loader=BaseLoader, undefined=StrictUndefined).from_string(msg)
        context = cls._get_context(resource)
        return j2.render(context)
        
    @classmethod
    def from_file(cls, path, resource):
        loader = FileSystemLoader(searchpath="./")
        env = Environment(loader=loader, undefined=StrictUndefined)
        template = env.get_template(path)
        context = cls._get_context(resource)
        return template.render(context)

    @classmethod
    def native_eval(cls, msg, resource):
        msg = "{{ %s }}" % msg
        j2 = Environment(loader=BaseLoader, undefined=StrictUndefined).from_string(msg)
        context = cls._get_context(resource)
        result = j2.render(context)
