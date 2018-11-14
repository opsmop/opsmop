from opsmop.conditions.condition import Condition
from opsmop.core.fields import Fields
from opsmop.core.field import Field
from opsmop.core.facts import Facts

facts = Facts()

class Deferred(Condition):

    def __init__(self, fn, *args, **kwargs):
        kwargs['fn'] = fn
        super().__init__(*args, **kwargs)
    
    def fields(self):
        return Fields(
            fn = Field(),
        )

    def evaluate(self):
        result = self.fn()
        return result

    # FIXME: we will need to implement a lot more than just ___add__
    # can we make this more generic?

    def __add__(self, other):
        global facts

        def my_add():
            nonlocal other
            if issubclass(type(other), Condition):
                other = other.evaluate()
            return self.evaluate() + other

        return Deferred(my_add)
        

