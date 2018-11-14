from jinja2 import Environment, BaseLoader, FileSystemLoader, StrictUndefined
from opsmop.core.facts import Facts

facts = Facts()

class FactLookup(object):

    def __init__(self):
        pass

    def __getattr__(self, field):
        f = getattr(facts, field)
        return f()

class VariableLookup(object):

    def __init__(self):
        pass

    def __getattr__(self, field):
        print("F=%s" % Facts.variables())
        return Facts.variables().get(field)

class Template(object):

    @classmethod
    def _get_context(cls, resource):
        #print("V=",Facts.variables())
        variable_lookup = VariableLookup()
        fact_lookup = FactLookup()
        return dict(
            F = fact_lookup,
            V = variable_lookup
        )

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
