from opsmop.providers.provider import Provider
from opsmop.lookups.lookup import Lookup
from opsmop.facts.facts import Facts

class DebugFacts(Provider):

    def quiet(self):
        return True

    def verb(self):
        return "debugging constant facts..."

    def skip_plan_stage(self):
        return True
 
    def apply(self):
        
        fact_output = Facts.constants()

        for (k,v) in Facts.constants().items():
            self.echo("%s = %s" % (k, v))
          
        return self.ok()