from opsmop.providers.provider import Provider
from opsmop.core.template import Template
from opsmop.conditions.var import V
from opsmop.conditions.deferred import Deferred

class Set(Provider):

    def plan(self, facts):
        self.needs('set')

        # we can update all values that are not deferred variables
        # in the plan stage but others need to wait.
        temp_items = dict()
        for (k,v) in self.items.items():
            if not issubclass(type(v), Deferred):
                temp_items[k] = v
        V.update_variables(temp_items)

    def apply(self, facts):

        self.do('set')

        new_items = dict()
        for (k,v) in self.items.items():
            if issubclass(type(v), Deferred):
                v = v.evaluate(facts)
            new_items[k] = v
            self.callbacks.indent_echo("%s => %s" % (k,v))
        V.update_variables(new_items)
        return self.ok()
        

