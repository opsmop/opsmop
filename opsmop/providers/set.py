from opsmop.core.template import Template
from opsmop.lookups.lookup import Lookup
from opsmop.providers.provider import Provider


class Set(Provider):

    def plan(self):
        self.needs('set')
        self.copy_variables()

    def copy_variables(self):
        temp_items = dict()
        for (k,v) in self.extra_variables.items():
            if issubclass(type(v), Lookup):
                temp_items[k] = v.evaluate(self.resource)
            else:
                temp_items[k] = v
            self.echo("%s = %s" % (k,temp_items[k]))
        self.resource.update_parent_variables(temp_items)

    def verb(self):
        return "setting..."

    def skip_plan_stage(self):
        return True

    def apply(self):
        self.do('set')
        # we run this again so that any registered variables can be erased if so desired
        self.copy_variables()
        return self.ok()
