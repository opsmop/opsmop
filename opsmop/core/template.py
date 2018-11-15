from jinja2 import Environment, BaseLoader, FileSystemLoader, StrictUndefined
from jinja2.nativetypes import NativeEnvironment
from opsmop.core.facts import Facts
from opsmop.core.resource import Resource

facts = Facts()

class FactLookup(object):

    def __init__(self):
        pass

    def __getattr__(self, field):
        f = getattr(facts, field)
        return f()

class Template(object):

    @classmethod
    def _get_context(cls, resource):
        assert(type(resource), Resource)
        fact_lookup = FactLookup()
        context = resource.get_variables()
        context["F"] = fact_lookup
        return context

    @classmethod
    def from_string(cls, msg, resource):
        assert(type(msg), str)
        assert(type(resource), Resource)
        j2 = Environment(loader=BaseLoader, undefined=StrictUndefined).from_string(msg)
        context = cls._get_context(resource)
        return j2.render(context)
        
    @classmethod
    def from_file(cls, path, resource):
        assert(type(path), str)
        assert(type(resource), Resource)
        loader = FileSystemLoader(searchpath="./")
        env = Environment(loader=loader, undefined=StrictUndefined)
        template = env.get_template(path)
        context = cls._get_context(resource)
        return template.render(context)

    @classmethod
    def native_eval(cls, msg, resource):
        assert(type(msg), str)
        assert(type(resource), Resource)
        msg = "{{ %s }}" % msg
        j2 = Environment(loader=BaseLoader, undefined=StrictUndefined).from_string(msg)
        context = cls._get_context(resource)
        result = j2.render(context)
