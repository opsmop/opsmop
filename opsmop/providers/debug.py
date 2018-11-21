from opsmop.lookups.lookup import Lookup
from opsmop.providers.provider import Provider


class Debug(Provider):

    def quiet(self):
        return True

    def verb(self):
        return "debugging..."

    def skip_plan_stage(self):
        return True
 
    def apply(self):
        
        variables = self.resource.get_variables()

        len1 = len(self.variable_names)
        len2 = len(self.evals.items())
        if len1 == 0 and len2 == 0:
            for (k, v) in variables.items():
                self.echo("%s = %s" % (k, v))

        for vname in self.variable_names:
            if vname in variables:
                self.echo("%s = %s" % (vname, variables[vname]))
            else:
                self.echo("%s is not defined" % vname)

        for (k, expr) in self.evals.items():
            actual = expr
            if issubclass(type(expr), Lookup):
                 actual = expr.evaluate(self.resource)
            self.echo("%s => %s" % (k, actual))
          
        return self.ok()
