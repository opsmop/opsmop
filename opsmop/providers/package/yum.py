from opsmop.providers.package.package import Package

class Yum(Package):

    """
    Manages yum packages
    """
    
    def plan(self):
        raise NotImplementedError()

    def apply(self):
        raise NotImplementedError()

        