from opsmop.core.resource import Resource

class Lookup():

    """
    A representation of a condition that is fed to a "when" clause.
    condition.evaluate(resource) facts will return true or false.
    """

    def __init__(self):
        pass

    def evaluate(self, resource):
        raise NotImplementedError()
