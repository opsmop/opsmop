from opsmop.providers.package.package import Package

class Yum(Package):

    """
    Manages yum packages
    """
    
    def plan(self, facts):
        raise NotImplementedError()

    def apply(self, facts):
        raise NotImplementedError()

        