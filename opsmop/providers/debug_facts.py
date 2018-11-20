from opsmop.providers.provider import Provider
from opsmop.lookups.lookup import Lookup

class DebugFacts(Provider):

    def quiet(self):
        return True

    def verb(self):
        return "debugging constant facts..."

    def skip_plan_stage(self):
        return True
 
    def apply(self):
        
        # fact_instances return a dictionary of fact
        # instances such as:
        # dict(
        #     UserFacts: UserFacts
        #     Platform: Platform
        #     FileTest: FileTest
        # )

        context = self.resource.fact_context()

        for (k,v) in context.items():

            # for each fact instance, print a header
            # and then show the contant facts in
            # each (the facts that don't take)
            # parameters

            self.echo("---")
            self.echo("Facts Class: %s" % k)
            for (k2, v2) in v.constants().items():
                self.echo("  %s => %s" % (k2, v2))
            self.echo("note: other methods may exist that take parameters")

        return self.ok()