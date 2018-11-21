from jinja2 import BaseLoader, Environment, FileSystemLoader, StrictUndefined
from jinja2.nativetypes import NativeEnvironment

from opsmop.core.resource import Resource


class Template(object):

    __slots__ = []

    @classmethod
    def _get_context(cls, resource):
        context = resource.template_context()
        variables = resource.get_variables()
        variables.update(context)
        return variables

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
        j2 = NativeEnvironment(loader=BaseLoader, undefined=StrictUndefined).from_string(msg)
        context = cls._get_context(resource)
        return j2.render(context)
