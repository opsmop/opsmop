from opsmop.providers.provider import Provider
from opsmop.core.template import Template
from opsmop.conditions.deferred import Deferred

class Set(Provider):

    def plan(self):
        self.needs('set')

        # we can update all values that are not deferred variables
        # in the plan stage but others need to wait.
        temp_items = dict()
        for (k,v) in self.items.items():
            if not issubclass(type(v), Deferred):
                temp_items[k] = v
        self.facts().update_variables(temp_items)

    def verb(self):
        return "setting..."

    def skip_plan_stage(self):
        return True

    def apply(self):

        self.do('set')

        new_items = dict()
        for (k,v) in self.items.items():
            if issubclass(type(v), Deferred):
                v = v.evaluate()
            new_items[k] = v
            self.echo("%s => %s" % (k,v))
        self.facts().update_variables(new_items)
        #self.context.on_update_variables(new_items)
        return self.ok()
        

