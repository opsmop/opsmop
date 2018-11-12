from jinja2 import Environment, BaseLoader, FileSystemLoader, StrictUndefined
# FIXME: facts does not belong in client, it belongs in core.
from opsmop.client.facts import Facts
# FIXME: this is not EXACTLY a condition and should be moved to core?


class FactLookup(object):

    def __init__(self, facts):
        self.facts = facts

    def __getattr__(self, field):
        f = getattr(self.facts, field)
        return f()

class VariableLookup(object):

    def __init__(self, variables, facts):
        self.variables = variables

    def __getattr__(self, field):
        return self.variables.get(field)

class Template(object):

    @classmethod
    def _get_context(cls, resource):
        variable_lookup = VariableLookup(resource.variables, resource.facts)
        fact_lookup = FactLookup(resource.facts)
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
