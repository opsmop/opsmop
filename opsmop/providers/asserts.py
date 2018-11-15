from opsmop.providers.provider import Provider
from opsmop.core.deferred import Deferred
from opsmop.core.template import Template

class Assert(Provider):

    def quiet(self):
        return True

    def verb(self):
        return "asserting..."

    def skip_plan_stage(self):
        return True
 
    def apply(self):

        failed = False
        for expr in self.evals:
            result = None
            if issubclass(type(expr), Deferred):
                result = expr.evaluate(self.resource)
            elif type(expr) == str:
                result = Template.native_eval(expr, self.resource)
            else:
                restult = expr
            self.echo("%s => %s" % (expr, result))
            if not result:
                failed = True
        
        variables = self.resource.get_variables()
        for (k,v) in self.variable_checks.items():
            if k not in variables:
                self.echo("%s is not defined" % k)
                failed = True
            else:
                actual = variables[k]
                if (v != actual):
                    self.echo("%s is %s (type:%s), should be %s (type:%s)" % (k, v, type(v), actual, type(actual)))
                    failed = True
                else:
                    self.echo("%s is %s" % (k, v))

        if not failed:
            return self.ok()
        else:
            return self.fatal("assertions failed")