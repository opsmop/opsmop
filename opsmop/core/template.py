from jinja2 import Environment, BaseLoader, FileSystemLoader, StrictUndefined
from jinja2.nativetypes import NativeEnvironment
from opsmop.core.facts import Facts
from opsmop.core.resource import Resource

class Template(object):

    def _get_context(self, resource, recursive_stop=None):

        self._variables = resource.get_variables()
        self._variables["Facts"] = Facts

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
